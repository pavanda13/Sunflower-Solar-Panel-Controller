#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

/* ================= OLED ================= */
#define OLED_SDA      21
#define OLED_SCL      22
#define OLED_ADDR     0x3C
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT  64
#define OLED_RESET     -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

/* ================= WIFI AP ================= */
const char* ssid     = "ESP32_SOLAR";
const char* password = "12345678";

WiFiServer server(5000);
WiFiClient client;

/* ================= BUTTONS ================= */
#define BTN_FORWARD      32   // servo forward toggle
#define BTN_REVERSE      33   // servo reverse toggle
#define BTN_PANEL_OPEN   27   // DC motor — open panel
#define BTN_PANEL_CLOSE  26   // DC motor — close panel

constexpr unsigned long DEBOUNCE = 200;

// Each button gets its own timer — pressing one won't block the others
unsigned long lastFwdBtn        = 0;
unsigned long lastRevBtn        = 0;
unsigned long lastPanelOpenBtn  = 0;
unsigned long lastPanelCloseBtn = 0;

/* ================= DATA ================= */
char  timeStr[9]     = "--:--:--";
float voltage        = 0;
float current        = 0;
float power          = 0;
float batteryVoltage = 0;

/* ================= HELPERS ================= */
void sendCmd(const char* cmd) {
  if (client && client.connected()) {
    client.println(cmd);
    Serial.print("Sent: ");
    Serial.println(cmd);
  }
}

void updateDisplay() {
  display.clearDisplay();

  display.setCursor(0, 0);
  display.println("SOLAR RECEIVER");

  display.setCursor(0, 12);
  display.print("Time: ");
  display.println(timeStr);

  display.setCursor(0, 24);
  display.print("V: ");
  display.print(voltage, 1);
  display.println(" V");

  display.setCursor(64, 24);
  display.print("B: ");
  display.print(batteryVoltage, 1);
  display.println(" V");

  display.setCursor(0, 40);
  display.print("I: ");
  display.print(current, 2);
  display.println(" A");

  display.setCursor(0, 54);
  display.print("P: ");
  display.print(power, 1);
  display.println(" W");

  display.display();
}

/* ================= SETUP ================= */
void setup() {
  Serial.begin(9600);

  pinMode(BTN_FORWARD,     INPUT_PULLUP);
  pinMode(BTN_REVERSE,     INPUT_PULLUP);
  pinMode(BTN_PANEL_OPEN,  INPUT_PULLUP);
  pinMode(BTN_PANEL_CLOSE, INPUT_PULLUP);

  Wire.begin(OLED_SDA, OLED_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  server.begin();

  Serial.print("AP IP: ");
  Serial.println(WiFi.softAPIP());

  display.setCursor(0, 0);
  display.println("Solar Receiver");
  display.setCursor(0, 12);
  display.println(WiFi.softAPIP());
  display.display();
}

/* ================= LOOP ================= */
void loop() {

  /* ===== ACCEPT CLIENT ===== */
  if (!client || !client.connected()) {
    client = server.available();
  }

  /* ===== RECEIVE SENSOR DATA ===== */
  if (client && client.connected() && client.available()) {
    char buf[64];
    int len = client.readBytesUntil('\n', buf, sizeof(buf) - 1);
    if (len > 0 && buf[len - 1] == '\r') len--;
    buf[len] = '\0';

    Serial.print("Rx: ");
    Serial.println(buf);

    // FORMAT: HH:MM:SS,voltage,current,power,batteryVoltage
    char* tok = strtok(buf, ",");
    if (tok) { strncpy(timeStr, tok, 8); timeStr[8] = '\0'; tok = strtok(NULL, ","); }
    if (tok) { voltage        = atof(tok); tok = strtok(NULL, ","); }
    if (tok) { current        = atof(tok); tok = strtok(NULL, ","); }
    if (tok) { power          = atof(tok); tok = strtok(NULL, ","); }
    if (tok) { batteryVoltage = atof(tok); }

    updateDisplay();
  }

  /* ===== BUTTON CONTROL ===== */

  // Servo forward toggle — solar controller handles on/off state
  if (digitalRead(BTN_FORWARD) == LOW && millis() - lastFwdBtn > DEBOUNCE) {
    lastFwdBtn = millis();
    sendCmd("SERVO_FWD");
  }

  // Servo reverse toggle
  if (digitalRead(BTN_REVERSE) == LOW && millis() - lastRevBtn > DEBOUNCE) {
    lastRevBtn = millis();
    sendCmd("SERVO_REV");
  }

  // DC motor — open panel
  if (digitalRead(BTN_PANEL_OPEN) == LOW && millis() - lastPanelOpenBtn > DEBOUNCE) {
    lastPanelOpenBtn = millis();
    sendCmd("PANEL_OPEN");
  }

  // DC motor — close panel
  if (digitalRead(BTN_PANEL_CLOSE) == LOW && millis() - lastPanelCloseBtn > DEBOUNCE) {
    lastPanelCloseBtn = millis();
    sendCmd("PANEL_CLOSE");
  }
}
