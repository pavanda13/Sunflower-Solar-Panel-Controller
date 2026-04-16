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
constexpr unsigned long DEBOUNCE         = 200;
constexpr unsigned long DISPLAY_INTERVAL = 500;  // ms between display refreshes

struct Button {
  uint8_t       pin;
  const char*   cmdPress;    // sent on press
  const char*   cmdRelease;  // sent on release
  unsigned long lastMs;
  bool          wasPressed;
};

// Add or remove buttons here — no other code needs to change
Button buttons[] = {
  { 32, "SERVO_FWD",   "SERVO_STOP", 0, false },  // hold = servo forward
  { 33, "SERVO_REV",   "SERVO_STOP", 0, false },  // hold = servo reverse
  { 27, "PANEL_OPEN",  "MOTOR_STOP", 0, false },  // hold = motor open
  { 26, "PANEL_CLOSE", "MOTOR_STOP", 0, false },  // hold = motor close
};
constexpr int NUM_BUTTONS = sizeof(buttons) / sizeof(buttons[0]);

/* ================= DATA ================= */
char  timeStr[9]     = "--:--:--";
float voltage        = 0;
float current        = 0;
float power          = 0;
float batteryVoltage = 0;

unsigned long lastDisplayMs = 0;

/* ================= HELPERS ================= */
void sendCmd(const char* cmd) {
  if (client && client.connected()) {
    client.println(cmd);
    Serial.print("Sent: ");
    Serial.println(cmd);
  }
}

void updateDisplay(bool connected) {
  display.clearDisplay();

  display.setCursor(0, 0);
  display.print("SOLAR");
  display.setCursor(68, 0);
  display.println(connected ? "  [LIVE]" : "[NO SIG]");

  display.setCursor(0, 12);
  display.print("Time: ");
  display.println(timeStr);

  display.setCursor(0, 24);
  display.print("V: ");
  display.print(voltage, 1);
  display.print("V");

  display.setCursor(64, 24);
  display.print("B: ");
  display.print(batteryVoltage, 1);
  display.println("V");

  display.setCursor(0, 36);
  display.print("I: ");
  display.print(current, 2);
  display.println("A");

  display.setCursor(0, 48);
  display.print("P: ");
  display.print(power, 1);
  display.println("W");

  display.display();
}

/* ================= SETUP ================= */
void setup() {
  Serial.begin(9600);

  for (auto& b : buttons) pinMode(b.pin, INPUT_PULLUP);

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
  bool connected = client && client.connected();

  /* ===== ACCEPT CLIENT ===== */
  if (!connected) {
    client    = server.available();
    connected = client && client.connected();
  }

  /* ===== RECEIVE SENSOR DATA ===== */
  if (connected && client.available()) {
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
  }

  /* ===== DISPLAY (every 500 ms) ===== */
  if (millis() - lastDisplayMs >= DISPLAY_INTERVAL) {
    lastDisplayMs = millis();
    updateDisplay(connected);
  }

  /* ===== BUTTONS ===== */
  for (auto& b : buttons) {
    bool pressed = digitalRead(b.pin) == LOW;

    if (pressed && !b.wasPressed) {
      // Press edge — debounced to ignore noise
      if (millis() - b.lastMs > DEBOUNCE) {
        b.lastMs = millis();
        sendCmd(b.cmdPress);
      }
    } else if (!pressed && b.wasPressed) {
      // Release edge — immediate, no debounce (stop right away)
      sendCmd(b.cmdRelease);
      b.lastMs = millis();
    }

    b.wasPressed = pressed;
  }
}
