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
#define SERVO_PIN  25

/* ================= CALIBRATION ================= */
constexpr float ADC_SCALE = 3.3f / 4095.0f;
float VOLT_RATIO = 5.0f;
float BAT_RATIO  = 5.0f;
float ACS_OFFSET = 2.5f;
float ACS_SENS   = 0.066f;

/* ================= TIMINGS ================= */
constexpr uint32_t OPEN_DURATION        = 4000;            // ms — panel open run time
constexpr uint32_t CLOSE_DURATION       = 4000;            // ms — panel close run time
constexpr uint32_t SERVO_TRACK_INTERVAL = 15UL * 60 * 1000;  // 15 min between tracking pulses
constexpr float    SERVO_RPM            = 120.0f;            // your servo's speed — measure and adjust
constexpr float    SERVO_TRACK_REVS     = 4.0f;              // revolutions per tracking pulse
constexpr uint32_t SERVO_TRACK_DURATION =                    // auto-calculated from RPM
  (uint32_t)((SERVO_TRACK_REVS / SERVO_RPM) * 60000.0f);    // = 4000 ms at 60 RPM
constexpr uint32_t SEND_INTERVAL        = 100;             // ms between data transmissions

/* ================= MOTOR STATE ================= */
// Motor is only allowed to start from IDLE, preventing re-trigger during a run
enum MotorState { MOTOR_IDLE, MOTOR_OPENING, MOTOR_CLOSING, MOTOR_MANUAL };
MotorState    motorState = MOTOR_IDLE;
unsigned long motorStopAt = 0;

/* ================= FLAGS ================= */
bool opened   = false;
bool closed   = false;
bool testMode = false;

/* ================= SERVO ================= */
Servo      servo;
MotorL298N motorA(IN1, IN2, ENA, 20000, 8);

bool servoForward = false;
bool servoReverse = false;

unsigned long lastServoTrack   = 0;   // millis() when last tracking pulse started
unsigned long servoTrackStopAt = 0;   // 0 = not tracking

/* ================= DATA SEND / RECONNECT ================= */
unsigned long lastSendMs      = 0;
unsigned long lastReconnectMs = 0;
unsigned long lastRTCread     = 0;
DateTime      cachedTime;

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

  /* Cache RTC — I2C read every 1s instead of every 10ms (100x less overhead) */
  if (millis() - lastRTCread >= 1000) {
    cachedTime  = rtc.now();
    lastRTCread = millis();
  }
  DateTime& now = cachedTime;

  /* ===== RECEIVE COMMAND ===== */
  if (client.connected() && client.available()) {
    char buf[32];
    int len = client.readBytesUntil('\n', buf, sizeof(buf) - 1);
    if (len > 0 && buf[len - 1] == '\r') len--;  // strip \r
    buf[len] = '\0';

    if (strcmp(buf, "SERVO_FWD") == 0) {
      servoForward = true;
      servoReverse = false;
      Serial.println("Servo: FORWARD");

    } else if (strcmp(buf, "SERVO_REV") == 0) {
      servoReverse = true;
      servoForward = false;
      Serial.println("Servo: REVERSE");

    } else if (strcmp(buf, "SERVO_STOP") == 0) {
      servoForward = false;
      servoReverse = false;
      Serial.println("Servo: STOP");

    } else if (strcmp(buf, "MOTOR_FWD") == 0 || strcmp(buf, "PANEL_OPEN") == 0) {
      if (motorState == MOTOR_IDLE) {
        motorA.setSpeed(100, true);
        motorState = MOTOR_MANUAL;
        Serial.println("Motor: MANUAL FORWARD");
      }

    } else if (strcmp(buf, "MOTOR_REV") == 0 || strcmp(buf, "PANEL_CLOSE") == 0) {
      if (motorState == MOTOR_IDLE) {
        motorA.setSpeed(100, false);
        motorState = MOTOR_MANUAL;
        Serial.println("Motor: MANUAL REVERSE");
      }

    } else if (strcmp(buf, "MOTOR_STOP") == 0) {
      if (motorState == MOTOR_MANUAL) {
        motorA.stop();
        motorState = MOTOR_IDLE;
        Serial.println("Motor: MANUAL STOP");
      }

    } else if (strcmp(buf, "RESET") == 0) {
      // Emergency stop — halts everything and resets all state flags
      motorStopAt    = 0;
      motorState     = MOTOR_IDLE;
      servoTrackStopAt = 0;
      servoForward   = false;
      servoReverse   = false;
      opened         = false;
      closed         = false;
      motorA.hardBrake();
      Serial.println("System: RESET");
    }
  }

  /* ===== MOTOR SCHEDULE ===== */
  // Only allow a new command when motor has fully completed its previous run.
  // This prevents testMode or rapid time-checks from re-triggering during a run.
  if (motorState == MOTOR_IDLE) {

    if ((testMode || (now.hour() == 1 && now.minute() == 42)) && !opened) {
      motorA.setSpeed(100, true);
      motorStopAt = millis() + OPEN_DURATION;
      motorState  = MOTOR_OPENING;
      Serial.println("Motor: OPENING");
    }
    else if ((now.hour() == 1 && now.minute() == 44) && !closed) {
      motorA.setSpeed(100, false);
      motorStopAt = millis() + CLOSE_DURATION;
      motorState  = MOTOR_CLOSING;
      Serial.println("Motor: CLOSING");
    }
  }

  /* ===== MOTOR AUTO-STOP ===== */
  // Flags are set HERE (after the run), not when the trigger fires.
  // This matches physical reality — the panel is open/closed only after the motor finishes.
  if (motorStopAt && millis() >= motorStopAt) {
    motorA.stop();
    motorStopAt = 0;

    if (motorState == MOTOR_OPENING) {
      opened = true;
      closed = false;
      lastServoTrack = millis();  // start 15-min timer when panel opens
      Serial.println("Motor: OPEN done");
    } else if (motorState == MOTOR_CLOSING) {
      closed  = true;
      opened  = false;
      servoTrackStopAt = 0;  // cancel any active tracking pulse
      Serial.println("Motor: CLOSE done");
    }

    motorState = MOTOR_IDLE;
  }

  /* ===== AUTO SERVO TRACKING (every 15 min while panel is open) ===== */
  if (opened && !servoForward && !servoReverse) {
    if (!servoTrackStopAt && millis() - lastServoTrack >= SERVO_TRACK_INTERVAL) {
      servoTrackStopAt = millis() + SERVO_TRACK_DURATION;
      lastServoTrack   = millis();
      Serial.println("Servo: auto-track");
    }
  }
  if (servoTrackStopAt && millis() >= servoTrackStopAt) {
    servoTrackStopAt = 0;
  }

  /* ===== SERVO CONTROL ===== */
  // Priority: manual command > auto-track > stop
  if (servoForward)          servo.write(180);  // manual forward
  else if (servoReverse)     servo.write(0);    // manual reverse
  else if (servoTrackStopAt) servo.write(180);  // auto sun-track pulse (adjust direction if needed)
  else                       servo.write(90);   // stop

  /* ===== WIFI RECONNECT ===== */
  // Only attempt while motor is idle — client.connect() blocks for up to 500ms,
  // which would prevent motorA.update() from running and stall the PWM ramp.
  if (!client.connected() && motorState == MOTOR_IDLE) {
    if (millis() - lastReconnectMs >= 5000) {
      lastReconnectMs = millis();
      client.connect(receiverIP, receiverPort, 500);  // 500ms timeout max
    }
  }

  /* ===== SENSOR READ + SEND (every 100 ms) ===== */
  if (millis() - lastSendMs >= SEND_INTERVAL) {
    lastSendMs = millis();

    float voltage = analogRead(VOLT_PIN) * ADC_SCALE * VOLT_RATIO;
    if (voltage < 0.5f) voltage = 0;

    float batteryVoltage = analogRead(BATT_PIN) * ADC_SCALE * BAT_RATIO;
    if (batteryVoltage < 0.5f) batteryVoltage = 0;

    float current = (analogRead(CURR_PIN) * ADC_SCALE - ACS_OFFSET) / ACS_SENS;
    if (current < 0.05f) current = 0;

    float power = voltage * current;

    if (client.connected()) {
      client.printf("%02d:%02d:%02d,%.2f,%.2f,%.2f,%.2f\n",
                    now.hour(), now.minute(), now.second(),
                    voltage, current, power, batteryVoltage);
    }
  }

  delay(10);  // 10 ms loop — gives motorA.update() enough resolution for smooth ramping
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
