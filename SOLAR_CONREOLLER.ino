#include <WiFi.h>
#include <Wire.h>
#include "RTClib.h"
#include <ESP32Servo.h>
#include "MotorL298N.h"

/* ================= WIFI ================= */
const char* ssid         = "ESP32_SOLAR";
const char* password     = "12345678";
const char* receiverIP   = "192.168.4.1";
const int   receiverPort = 5000;

WiFiClient client;

/* ================= RTC ================= */
RTC_DS3231 rtc;

/* ================= PINS ================= */
#define VOLT_PIN   34
#define CURR_PIN   35
#define BATT_PIN   32
#define IN1        18
#define IN2        16
#define ENA        17
#define SERVO_PIN  26

/* ================= CALIBRATION ================= */
constexpr float ADC_SCALE = 3.3f / 4095.0f;
float VOLT_RATIO = 5.0f;
float BAT_RATIO  = 5.0f;
float ACS_OFFSET = 2.5f;
float ACS_SENS   = 0.066f;

/* ================= TIMINGS ================= */
constexpr uint32_t OPEN_DURATION  = 12000;
constexpr uint32_t CLOSE_DURATION = 12000;

/* ================= STATE ================= */
Servo      servo;
MotorL298N motorA(IN1, IN2, ENA, 20000, 8);

bool servoForward = false;
bool servoReverse = false;
bool opened       = false;
bool closed       = false;
bool testMode     = false;

unsigned long motorStopAt = 0;  // 0 = motor idle

/* ================= SETUP ================= */
void setup() {
  Serial.begin(9600);

  /* Servo first — must claim LEDC channel before motorA.begin() */
  servo.setPeriodHertz(50);
  servo.attach(SERVO_PIN, 500, 2400);
  servo.write(90);  // stop

  motorA.begin();

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  Wire.begin(14, 13);
  rtc.begin();
  if (rtc.lostPower()) rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(200);

  calibrateCurrentSensor();
}

/* ================= LOOP ================= */
void loop() {
  motorA.update();
  DateTime now = rtc.now();

  /* ===== RECEIVE COMMAND ===== */
  if (client.connected() && client.available()) {
    char buf[32];
    int len = client.readBytesUntil('\n', buf, sizeof(buf) - 1);
    if (len > 0 && buf[len - 1] == '\r') len--;  // strip \r
    buf[len] = '\0';

    if (strcmp(buf, "SERVO_FWD") == 0) {
      servoForward = !servoForward;
      servoReverse = false;
      Serial.println(servoForward ? "Servo: FORWARD" : "Servo: STOP");
    } else if (strcmp(buf, "SERVO_REV") == 0) {
      servoReverse = !servoReverse;
      servoForward = false;
      Serial.println(servoReverse ? "Servo: REVERSE" : "Servo: STOP");
    }
  }

  /* ===== SERVO CONTROL ===== */
  servo.write(servoForward ? 180 : servoReverse ? 0 : 90);

  /* ===== MORNING OPEN ===== */
  if ((testMode || (now.hour() == 1 && now.minute() == 42)) && !opened) {
    motorA.setSpeed(100, true);
    motorStopAt = millis() + OPEN_DURATION;
    opened = true;
    closed = false;
  }

  /* ===== EVENING CLOSE ===== */
  if ((now.hour() == 1 && now.minute() == 44) && !closed) {
    motorA.setSpeed(100, false);
    motorStopAt = millis() + CLOSE_DURATION;
    closed = true;
    opened = false;
  }

  /* ===== MOTOR AUTO-STOP ===== */
  if (motorStopAt && millis() >= motorStopAt) {
    motorA.stop();
    motorStopAt = 0;
  }

  /* ===== SENSOR READ ===== */
  float voltage = analogRead(VOLT_PIN) * ADC_SCALE * VOLT_RATIO;
  if (voltage < 0.5f) voltage = 0;

  float batteryVoltage = analogRead(BATT_PIN) * ADC_SCALE * BAT_RATIO;
  if (batteryVoltage < 0.5f) batteryVoltage = 0;

  float current = (analogRead(CURR_PIN) * ADC_SCALE - ACS_OFFSET) / ACS_SENS;
  if (current < 0.05f) current = 0;

  float power = voltage * current;

  /* ===== SEND DATA ===== */
  if (!client.connected()) client.connect(receiverIP, receiverPort);
  if (client.connected()) {
    client.printf("%02d:%02d:%02d,%.2f,%.2f,%.2f,%.2f\n",
                  now.hour(), now.minute(), now.second(),
                  voltage, current, power, batteryVoltage);
  }

  delay(100);
}

/* ===== CURRENT SENSOR CALIBRATION ===== */
void calibrateCurrentSensor() {
  float sum = 0;
  for (int i = 0; i < 500; i++) {
    sum += analogRead(CURR_PIN) * ADC_SCALE;
    delay(2);
  }
  ACS_OFFSET = sum / 500.0f;
}
