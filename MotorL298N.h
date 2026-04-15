#ifndef MOTOR_L298N_H
#define MOTOR_L298N_H

#include <Arduino.h>

class MotorL298N {
  private:
    uint8_t  _in1, _in2, _ena, _res;
    uint32_t _freq;
    int      _currentPct    = 0;
    int      _targetPct     = 0;
    int      _rampInterval  = 50;   // ms between ramp steps
    int      _rampStep      = 1;    // % change per step
    unsigned long _lastRampTime = 0;

    void _writePWM(int pct) {
      int maxDuty = (1 << _res) - 1;
      ledcWrite(_ena, map(pct, 0, 100, 0, maxDuty));
    }

  public:
    MotorL298N(uint8_t in1, uint8_t in2, uint8_t ena, uint32_t freq, uint8_t res)
      : _in1(in1), _in2(in2), _ena(ena), _freq(freq), _res(res) {}

    void begin() {
      pinMode(_in1, OUTPUT);
      pinMode(_in2, OUTPUT);
      ledcAttach(_ena, _freq, _res);
      hardBrake();
    }

    // Tune ramp speed. Default: 1% per 50ms = 5s to reach 100%.
    // Example: setRamp(20, 2) = 2% per 20ms = 1s ramp.
    void setRamp(int intervalMs, int stepPct = 1) {
      _rampInterval = max(intervalMs, 1);
      _rampStep     = constrain(stepPct, 1, 100);
    }

    void setSpeed(int targetPct, bool forward = true) {
      _targetPct = constrain(targetPct, 0, 100);
      digitalWrite(_in1, forward ? HIGH : LOW);
      digitalWrite(_in2, forward ? LOW : HIGH);

      // If starting from rest, immediately write a kickstart PWM instead of waiting
      // for the first update() call. This prevents missed starts when update() is
      // delayed by WiFi or I2C operations stalling the loop.
      if (_currentPct == 0 && _targetPct > 0) {
        _currentPct = min(_targetPct, 30);  // kick to 30% (or target if lower)
        _writePWM(_currentPct);
      }
    }

    // Soft stop: ramps down to 0 via update()
    void stop() {
      _targetPct = 0;
    }

    // Hard stop: cuts PWM and direction pins immediately
    void hardBrake() {
      _targetPct  = 0;
      _currentPct = 0;
      ledcWrite(_ena, 0);
      digitalWrite(_in1, LOW);
      digitalWrite(_in2, LOW);
    }

    // Returns current PWM level (0–100%)
    int getSpeed() const { return _currentPct; }

    // True if motor is spinning or still ramping down
    bool isRunning() const { return _currentPct > 0 || _targetPct > 0; }

    void update() {
      if (_currentPct == _targetPct) return;

      if (millis() - _lastRampTime >= (unsigned long)_rampInterval) {
        _lastRampTime = millis();

        if (_currentPct < _targetPct) _currentPct = min(_currentPct + _rampStep, _targetPct);
        else                          _currentPct = max(_currentPct - _rampStep, _targetPct);

        _writePWM(_currentPct);

        if (_currentPct == 0) {
          digitalWrite(_in1, LOW);
          digitalWrite(_in2, LOW);
        }
      }
    }
};

#endif
