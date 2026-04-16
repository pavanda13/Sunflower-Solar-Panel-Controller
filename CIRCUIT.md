# Circuit Diagram — Sunflower Solar Panel Controller

> To draw a graphical schematic, import these connections into [EasyEDA](https://easyeda.com) or [Fritzing](https://fritzing.org).

---

## Full Wiring Overview

```
                         ┌──────────────────────────────────────────┐
                         │                 ESP32                    │
                         │                                          │
              ┌──────────┤ GPIO18          GPIO25 ──────────────────┼──► Servo Signal
              │  ┌───────┤ GPIO16          GPIO34 ──┐               │
              │  │  ┌────┤ GPIO17 (PWM)    GPIO35 ──┼──┐            │
              │  │  │    │                 GPIO32 ──┼──┼──┐         │
              │  │  │    │                 GPIO13 ──┼──┼──┼──┐      │
              │  │  │    │                 GPIO14 ──┼──┼──┼──┼──┐   │
              │  │  │    │                          │  │  │  │  │   │
              │  │  │    │   3.3V ─────────────────┼──┼──┼──┼──┼───┼── Sensors VCC
              │  │  │    │   GND ──────────────────┼──┼──┼──┼──┼───┼── Common GND
              │  │  │    └──────────────────────────┼──┼──┼──┼──┼───┘
              │  │  │                               │  │  │  │  │
              │  │  │        Panel Voltage Divider ─┘  │  │  │  │
              │  │  │        ACS712 Current Sensor ─────┘  │  │  │
              │  │  │        Battery Voltage Divider ───────┘  │  │
              │  │  │        DS3231 SDA ────────────────────────┘  │
              │  │  │        DS3231 SCL ─────────────────────────────┘
              │  │  │
              ▼  ▼  ▼
      ┌────────────────────┐
      │       L298N        │
      │  IN1  IN2  ENA     │
      │                    │
      │  OUT1 ──── OUT2 ───┼──── DC Motor (+ / -)
      │                    │
      │  12V ──────────────┼──── 12V Power Supply (+)
      │  GND ──────────────┼──── Common GND
      │  5V  (optional) ───┼──── ESP32 VIN (if no separate 5V regulator)
      └────────────────────┘
```

---

## Component Wiring Tables

### 1. L298N Motor Driver → ESP32

| L298N Pin | ESP32 Pin | Notes |
|-----------|-----------|-------|
| IN1 | GPIO 18 | Motor direction A |
| IN2 | GPIO 16 | Motor direction B |
| ENA | GPIO 17 | PWM speed control |
| GND | GND | Common ground |
| 5V (out) | VIN | Can power ESP32 (if L298N has onboard 5V reg) |
| 12V (in) | — | Connect to 12V motor supply |

### L298N → DC Motor

| L298N Pin | DC Motor |
|-----------|----------|
| OUT1 | Motor terminal + |
| OUT2 | Motor terminal − |

---

### 2. Servo Motor → ESP32

| Servo Wire | ESP32 Pin | Notes |
|------------|-----------|-------|
| Signal (orange/yellow) | GPIO 25 | PWM 50 Hz |
| VCC (red) | 5V | Use external 5V — do NOT power from ESP32 3.3V |
| GND (brown/black) | GND | Common ground |

> **Note:** Servo draws high current on startup. Use a dedicated 5V regulator or the L298N's 5V output, not the ESP32's 3.3V pin.

---

### 3. DS3231 RTC Module → ESP32

| DS3231 Pin | ESP32 Pin | Notes |
|------------|-----------|-------|
| VCC | 3.3V | |
| GND | GND | |
| SDA | GPIO 13 | Non-default I2C — `Wire.begin(14, 13)` |
| SCL | GPIO 14 | Non-default I2C |
| SQW | — | Not used |
| 32K | — | Not used |

---

### 4. Panel Voltage Sensor (Voltage Divider) → ESP32

Measures solar panel output voltage (0–25V range with 5:1 divider).

```
Solar Panel (+) ──── R1 (40kΩ) ──┬──── R2 (10kΩ) ──── GND
                                  │
                               GPIO 34 (VOLT_PIN)
```

| Connection | Value |
|------------|-------|
| R1 | 40 kΩ |
| R2 | 10 kΩ |
| Output pin | GPIO 34 |
| Max input voltage | 25V (VOLT_RATIO = 5.0) |

---

### 5. Battery Voltage Sensor (Voltage Divider) → ESP32

Measures system battery voltage (0–25V range with 5:1 divider).

```
Battery (+) ──── R1 (40kΩ) ──┬──── R2 (10kΩ) ──── GND
                              │
                           GPIO 32 (BATT_PIN)
```

| Connection | Value |
|------------|-------|
| R1 | 40 kΩ |
| R2 | 10 kΩ |
| Output pin | GPIO 32 |
| Max input voltage | 25V (BAT_RATIO = 5.0) |

---

### 6. ACS712 Current Sensor → ESP32

Measures solar panel output current.

```
Solar Panel (+) ──► [ACS712 IP+] ──► [ACS712 IP-] ──► Load (+)
```

| ACS712 Pin | ESP32 / Connection |
|------------|-------------------|
| VCC | 5V |
| GND | GND |
| OUT | GPIO 35 (CURR_PIN) |
| IP+ | From solar panel (+) |
| IP− | To load (+) |

> **Module:** ACS712-30A (sensitivity = 0.066 V/A, zero = ~2.5V auto-calibrated on boot).

---

## Power Supply

```
                   ┌──────────────┐
  12V Battery ────►│   12V Rail   │──► L298N 12V, Motor
                   └──────┬───────┘
                          │
                   ┌──────▼───────┐
                   │  5V Reg      │──► Servo VCC, ACS712 VCC
                   │ (L298N 5V   │
                   │  or LM7805) │
                   └──────┬───────┘
                          │
                   ┌──────▼───────┐
                   │  ESP32 VIN  │
                   │  (3.3V out) │──► DS3231 VCC, Voltage Dividers
                   └─────────────┘
```

| Rail | Powers |
|------|--------|
| 12V | DC motor via L298N |
| 5V | ESP32, Servo, ACS712 |
| 3.3V (from ESP32) | DS3231 RTC, voltage divider sense lines |

---

## Common GND

All components **must share a common GND**:
- ESP32 GND
- L298N GND
- Servo GND
- ACS712 GND
- DS3231 GND
- Voltage divider R2 bottom
- Power supply GND

---

## GPIO Summary

| GPIO | Function | Component |
|------|----------|-----------|
| 13 | I2C SDA | DS3231 RTC |
| 14 | I2C SCL | DS3231 RTC |
| 16 | Motor IN2 | L298N |
| 17 | Motor ENA (PWM) | L298N |
| 18 | Motor IN1 | L298N |
| 25 | Servo PWM | Servo motor |
| 32 | ADC — Battery voltage | Voltage divider |
| 34 | ADC — Panel voltage | Voltage divider |
| 35 | ADC — Panel current | ACS712 |
