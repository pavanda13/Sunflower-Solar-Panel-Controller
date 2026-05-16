# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sunflower Solar Panel Controller — a two-ESP32 system that autonomously opens a solar panel at sunrise, tracks the sun with a servo every 15 minutes, and retracts the panel at sunset. A second ESP32 acts as a wireless OLED dashboard with 4 physical control buttons.

## Build & Flash

This is an Arduino project. Use the Arduino IDE or `arduino-cli`:

```bash
# Install dependencies (one-time)
arduino-cli lib install "RTClib" "ESP32Servo" "Adafruit GFX Library" "Adafruit SSD1306"

# Compile + flash controller unit (adjust port)
arduino-cli compile --fqbn esp32:esp32:esp32 SOLAR_CONREOLLER.ino
arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 SOLAR_CONREOLLER.ino

# Compile + flash remote unit
arduino-cli compile --fqbn esp32:esp32:esp32 controller_unit.ino
arduino-cli upload -p /dev/ttyUSB1 --fqbn esp32:esp32:esp32 controller_unit.ino
```

## File Map

| File | Flashed to | WiFi role |
|------|-----------|-----------|
| `SOLAR_CONREOLLER.ino` | Controller ESP32 — motor, servo, sensors, RTC | Station (client) |
| `controller_unit.ino` | Remote ESP32 — OLED display, 4 buttons | Access Point (`192.168.4.1:5000`) |
| `MotorL298N.h` | Included by controller only | — |

## System Architecture

```
Remote unit (AP, 192.168.4.1:5000)          Controller (Station)
  ┌─────────────────────────────┐              ┌─────────────────────────────────┐
  │ OLED — Panel V, I, W, Batt  │   commands   │ L298N → DC motor (open/close)   │
  │ 4 hold-to-run buttons       │ ──────────► │ Servo → sun tracking            │
  │                             │  CSV/100ms   │ ACS712 current sensor           │
  │                             │ ◄──────────  │ Voltage dividers (panel + batt) │
  └─────────────────────────────┘              │ DS3231 RTC — open/close schedule│
                                               └─────────────────────────────────┘
```

## Communication Protocol

**Controller → Remote** every 100 ms (TCP CSV):
```
HH:MM:SS,voltage,current,power,batteryVoltage
08:42:15,18.34,2.10,38.51,12.67
```

**Remote → Controller** on button press/release (plain string over TCP):

| Command | Trigger | Effect |
|---------|---------|--------|
| `SERVO_FWD` | Hold button 1 | Servo rotates forward |
| `SERVO_REV` | Hold button 2 | Servo rotates reverse |
| `SERVO_STOP` | Release button 1 or 2 | Servo stops |
| `PANEL_OPEN` | Hold button 3 | Motor opens panel (only if `MOTOR_IDLE`) |
| `PANEL_CLOSE` | Hold button 4 | Motor closes panel (only if `MOTOR_IDLE`) |
| `MOTOR_STOP` | Release button 3 or 4 | Motor stops |
| `RESET` | Emergency | Halts everything, clears all state flags |

**Adding a new button** requires only one line in the `buttons[]` array in `controller_unit.ino` — no other code changes needed.

## Motor State Machine

```
MOTOR_IDLE ──(schedule or PANEL_OPEN/CLOSE)──► MOTOR_OPENING / MOTOR_CLOSING
                                                        │ after duration
                                                   MOTOR_IDLE  ← sets opened/closed flag

MOTOR_IDLE ──(PANEL_OPEN/CLOSE)──► MOTOR_MANUAL ──(MOTOR_STOP or 30s timeout)──► MOTOR_IDLE
```

- New commands are **only accepted from `MOTOR_IDLE`** — prevents double-triggering.
- `opened`/`closed` flags are set **after** the motor physically finishes, not on command issue.
- `MOTOR_MANUAL` has a 30-second safety cutoff (`MANUAL_TIMEOUT`) in case WiFi drops before `MOTOR_STOP` arrives.
- `RESET` performs emergency stop and advances `opened`/`closed` to prevent the scheduler re-triggering on the same minute.

## MotorL298N API (`MotorL298N.h`)

Custom soft-ramp PWM driver. Default: 1% per 50 ms = ~5 s to reach 100%. On `setSpeed()`, a 30% kickstart is applied immediately to overcome static friction before the ramp begins.

```cpp
motorA.begin();               // call AFTER servo.attach() — see LEDC note below
motorA.setSpeed(100, true);   // 100% forward, kicks to 30% immediately then ramps
motorA.setSpeed(100, false);  // 100% reverse
motorA.stop();                // soft stop — ramps down via update()
motorA.hardBrake();           // instant PWM cut — use for timed stops and RESET
motorA.setRamp(20, 2);        // 2% per 20ms = ~1s ramp
motorA.update();              // must be called every loop iteration to drive the ramp
```

Use `hardBrake()` for timed auto-stops (when `motorStopAt` elapses). `stop()` only sets the target to 0; the ramp-down window leaves `motorState` in limbo.

## Critical Hardware Constraints

**LEDC channel conflict:** `servo.attach()` must be called before `motorA.begin()`. Both use the ESP32 LEDC peripheral; `ESP32Servo` claims channels first-come-first-served — reversing order breaks motor PWM.

**Non-default I2C:** DS3231 RTC uses GPIO 13 (SDA) and GPIO 14 (SCL). `Wire.begin(14, 13)` is required.

**WiFi reconnect only during `MOTOR_IDLE`:** `client.connect()` blocks up to 500 ms. Calling it during a motor run stalls `motorA.update()` and breaks the PWM ramp. Never move the reconnect block outside the `motorState == MOTOR_IDLE` guard.

**GPIO 34, 35, 32 are input-only** on ESP32 — used for ADC only, no `pinMode(OUTPUT)`.

## Servo Control

Continuous-rotation servo: `write(0)` = reverse, `write(90)` = stop, `write(180)` = forward.

Priority applied every loop: **manual command > auto-track pulse > stop**.

Auto-tracking fires every 15 minutes while panel is open, for `SERVO_TRACK_DURATION` ms (auto-calculated from `SERVO_RPM` and `SERVO_TRACK_REVS`). Cancelled immediately when panel closes.

## Key Tunable Constants (`SOLAR_CONREOLLER.ino`)

| Constant | Default | Purpose |
|----------|---------|---------|
| `OPEN_DURATION` | 4000 ms | Motor run time to fully open panel |
| `CLOSE_DURATION` | 4000 ms | Motor run time to fully close panel |
| `SERVO_TRACK_INTERVAL` | 15 min | Time between auto sun-tracking pulses |
| `SERVO_RPM` | 120.0 | Measured servo speed — adjust to match hardware |
| `SERVO_TRACK_REVS` | 4.0 | Revolutions per tracking pulse |
| `VOLT_RATIO` / `BAT_RATIO` | 5.0 | Voltage divider ratio (R1=40 kΩ, R2=10 kΩ) |
| `ACS_SENS` | 0.066 V/A | ACS712-30A sensitivity |

`ACS_OFFSET` is auto-calibrated on every boot by averaging 500 ADC samples. Ensure no load is connected during the ~1 s boot calibration window.

## Test Mode

```cpp
bool testMode = false;  // SOLAR_CONREOLLER.ino
```

When `true`, the morning-open schedule fires every loop without waiting for the RTC time — useful for bench testing motor movement. **Must be `false` for deployment.**

## Sensor Pins

- `VOLT_PIN` GPIO 34 — solar panel output voltage
- `CURR_PIN` GPIO 35 — solar panel output current (ACS712-30A)
- `BATT_PIN` GPIO 32 — battery voltage

All three measure **panel output**, not motor current.
