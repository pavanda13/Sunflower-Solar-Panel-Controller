#ifndef MOTOR_L298N_H
#define MOTOR_L298N_H

#include <Arduino.h>

class MotorL298N {
  private:
    uint8_t _in1, _in2, _ena, _res;
    uint32_t _freq;
    int _currentPct = 0;
    int _targetPct = 0;
    unsigned long _lastRampTime = 0;
    int _rampInterval = 50; 

  public:
    MotorL298N(uint8_t in1, uint8_t in2, uint8_t ena, uint32_t freq, uint8_t res) 
      : _in1(in1), _in2(in2), _ena(ena), _freq(freq), _res(res) {}

    void begin() {
      pinMode(_in1, OUTPUT);
      pinMode(_in2, OUTPUT);
      ledcAttach(_ena, _freq, _res);
      hardBrake(); // Start fully stopped
    }

    void setSpeed(int targetPct, bool forward = true) {
      _targetPct = constrain(targetPct, 0, 100);
      digitalWrite(_in1, forward ? HIGH : LOW);
      digitalWrite(_in2, forward ? LOW : HIGH);
    }

    // SOFT STOP: Simply sets target to 0 and lets update() handle the ramp down
    void stop() {
      _targetPct = 0;
    }

    // HARD STOP: Immediate stop bypassing the ramp
    void hardBrake() {
      _targetPct = 0;
      _currentPct = 0;
      ledcWrite(_ena, 0);
      digitalWrite(_in1, LOW);
      digitalWrite(_in2, LOW);
    }

    void update() {
      if (_currentPct != _targetPct) {
        if (millis() - _lastRampTime >= _rampInterval) {
          if (_currentPct < _targetPct) _currentPct++;
          else _currentPct--;

          int maxDuty = (1 << _res) - 1;
          int duty = map(_currentPct, 0, 100, 0, maxDuty);
          ledcWrite(_ena, duty);
          
          _lastRampTime = millis();

          // Fully cut power when ramp reaches 0 to prevent humming
          if (_currentPct == 0) {
            digitalWrite(_in1, LOW);
            digitalWrite(_in2, LOW);
          }
        }
      }
    }
};

#endif