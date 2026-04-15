# Sunflower Solar Panel Controller — System Documentation

## Overview

A two-device ESP32 system that automatically opens and closes a solar panel like a sunflower — deploying in the morning, tracking the sun throughout the day with a servo motor, and retracting in the evening. A separate remote unit displays live sensor data on an OLED screen and allows manual servo control via two buttons.

---

## System Architecture

```
┌─────────────────────────────────────┐        ┌──────────────────────────────────┐
│        Solar Controller             │        │         Remote Control Unit      │
│         (ESP32 - Client)            │        │          (ESP32 - AP)            │
│                                     │  WiFi  │                                  │
│  DC Motor (L298N) ── Panel motion   │◄──────►│  OLED Display                   │
│  Servo Motor ──────── Sun tracking  │  TCP   │    - Panel Voltage               │
│  Panel Voltage Sensor               │        │    - Panel Current               │
│  Panel Current Sensor        data ──┼───────►│    - Power (W)                   │
│  Battery Voltage Sensor             │        │    - Battery Voltage             │
│  RTC DS3231 ────────── Timekeeping  │        │    - Current Time (RTC)          │
│                                     │◄───────┼── Button 1 (SERVO_FWD)          │
│                                     │commands│── Button 2 (SERVO_REV)          │
└─────────────────────────────────────┘        └──────────────────────────────────┘
```

---

## Device 1 — Solar Controller

### Hardware

| Component | Interface | GPIO Pins |
|---|---|---|
| L298N Motor Driver | Digital + PWM | IN1=18, IN2=16, ENA=17 |
| Servo Motor | PWM (50 Hz) | GPIO 25 |
| Panel Voltage Sensor | ADC | GPIO 34 |
| Panel Current Sensor (ACS) | ADC | GPIO 35 |
| Battery Voltage Sensor | ADC | GPIO 32 |
| RTC DS3231 | I2C | SDA=13, SCL=14 |

### Pin Notes
- GPIO 34, 35, 32 are input-only ADC pins on ESP32
- Servo must be initialized **before** `motorA.begin()` to avoid LEDC channel conflict
- I2C is on non-default pins (SDA=13, SCL=14) — `Wire.begin(14, 13)` required

### WiFi
- Mode: Station (client)
- Connects to: `ESP32_SOLAR` / `12345678`
- Sends data to: `192.168.4.1:5000` over TCP

---

## Device 2 — Remote Control Unit

### Hardware
- ESP32 acting as a WiFi Access Point (`192.168.4.1:5000`)
- OLED display showing live sensor values and time
- 2 push buttons for manual servo control

### Button Behaviour
| Button | Command Sent | Effect |
|---|---|---|
| Button 1 | `SERVO_FWD\n` | Toggle servo forward rotation (press again to stop) |
| Button 2 | `SERVO_REV\n` | Toggle servo reverse rotation (press again to stop) |

---

## Communication Protocol

### Controller → Remote (every 100 ms)

CSV line over TCP:

```
HH:MM:SS,voltage,current,power,batteryVoltage\n
```

| Field | Unit | Source |
|---|---|---|
| HH:MM:SS | time | RTC DS3231 |
| voltage | V | Panel voltage sensor (VOLT_PIN) |
| current | A | Panel current sensor (CURR_PIN) |
| power | W | voltage × current |
| batteryVoltage | V | Battery voltage sensor (BATT_PIN) |

Example:
```
08:42:15,18.34,2.10,38.51,12.67
```

### Remote → Controller (on button press)

Plain string over TCP:

```
SERVO_FWD\n    — toggle servo forward
SERVO_REV\n    — toggle servo reverse
```

---

## Sensor Calibration

| Parameter | Variable | Default | Description |
|---|---|---|---|
| Panel voltage scale | `VOLT_RATIO` | 5.0 | Voltage divider ratio for panel sensor |
| Battery voltage scale | `BAT_RATIO` | 5.0 | Voltage divider ratio for battery sensor |
| ACS zero offset | `ACS_OFFSET` | Auto-calibrated on boot | ADC voltage at 0A |
| ACS sensitivity | `ACS_SENS` | 0.066 V/A | For ACS712-30A module |

`ACS_OFFSET` is automatically calibrated on every boot by averaging 500 ADC samples over 1 second with no load connected.

---

## Panel Behaviour

### DC Motor — Panel Open / Close

The L298N driver controls a DC motor that physically deploys and retracts the solar panel.

| Event | Time (default test) | Direction | Duration |
|---|---|---|---|
| Morning Open | 01:42 | Forward | 4 seconds |
| Evening Close | 01:44 | Reverse | 4 seconds |

**Motor state machine** (`MOTOR_IDLE → MOTOR_OPENING/CLOSING → MOTOR_IDLE`):
- A new motor command is only accepted when state is `MOTOR_IDLE`
- Prevents re-triggering during a run (critical when `testMode = true`)
- `opened` / `closed` flags are set **after** the motor finishes, not when it starts

**Ramping:** Motor ramps 0→100% over ~5 seconds (1% per 50ms) via `MotorL298N::update()` called every loop iteration. A kickstart of 30% PWM is applied immediately on `setSpeed()` to overcome static friction.

### Servo Motor — Sun Tracking

A continuous rotation servo (0=reverse, 90=stop, 180=forward) adjusts the panel angle to track the sun.

| Mode | Trigger | Behaviour |
|---|---|---|
| Auto-track | Every 15 minutes while panel is open | Rotates forward for 2 seconds (4 revolutions at 120 RPM) |
| Manual forward | `SERVO_FWD` command | Rotates forward until toggled off |
| Manual reverse | `SERVO_REV` command | Rotates reverse until toggled off |

**Priority:** Manual command > Auto-track > Stop

Auto-tracking is cancelled when the panel closes.

---

## Key Constants (SOLAR_CONREOLLER.ino)

```cpp
OPEN_DURATION        = 4000 ms    // how long motor runs to fully open panel
CLOSE_DURATION       = 4000 ms    // how long motor runs to fully close panel
SERVO_TRACK_INTERVAL = 15 min     // time between auto sun-tracking pulses
SERVO_RPM            = 120.0      // servo speed — measure and adjust
SERVO_TRACK_REVS     = 4.0        // revolutions per tracking pulse
SERVO_TRACK_DURATION = 2000 ms    // auto-calculated: (4 / 120) × 60000
SEND_INTERVAL        = 100 ms     // data transmission rate to remote
```

---

## MotorL298N Library

Custom class in `MotorL298N.h` for smooth PWM-ramped DC motor control.

```cpp
MotorL298N motorA(IN1, IN2, ENA, freq=20000, resolution=8);

motorA.begin();                    // setup pins and LEDC
motorA.setSpeed(100, true);        // 100% forward — starts ramping up immediately
motorA.setSpeed(100, false);       // 100% reverse
motorA.stop();                     // soft stop — ramps down to 0
motorA.hardBrake();                // instant cut of PWM and direction pins
motorA.setRamp(20, 2);             // 2% per 20ms = 1 second ramp (default: 1% per 50ms)
motorA.getSpeed();                 // returns current PWM % (0–100)
motorA.isRunning();                // true if spinning or still decelerating
motorA.update();                   // call every loop — drives the ramp
```

---

## Loop Architecture

The main loop runs every **10 ms** with non-blocking millis() timers for all operations:

```
loop() [every 10ms]
  ├── motorA.update()          — advance PWM ramp
  ├── RTC cache update         — I2C read every 1s (not every 10ms)
  ├── Receive TCP command      — parse SERVO_FWD / SERVO_REV
  ├── Motor schedule           — trigger open/close if time matches and IDLE
  ├── Motor auto-stop          — cut motor after duration elapses
  ├── Servo auto-track         — 15-min pulse timer
  ├── Servo write              — apply current servo angle
  ├── WiFi reconnect           — retry every 5s, only when MOTOR_IDLE (500ms timeout)
  └── Sensor read + send       — ADC read and TCP send every 100ms
```

**Important:** WiFi `client.connect()` blocks the CPU. It is only attempted when `motorState == MOTOR_IDLE` to prevent it from stalling `motorA.update()` during a panel open/close operation.

---

## Test Mode

```cpp
bool testMode = false;
```

When `true`, the morning open condition fires every loop iteration (ignoring time), useful for bench testing motor movement without waiting for the scheduled time. **Set back to `false` before deployment** — leaving it `true` causes the open/close cycle to repeat rapidly.

---

## File Structure

```
SOLAR_CONREOLLER/
├── SOLAR_CONREOLLER.ino   — main controller firmware
├── MotorL298N.h           — DC motor PWM ramp driver class
└── SYSTEM.md              — this file
```
