#include <kipr/botball.h>
#include "motor.hpp"

Motor::Motor(int port, int speed) {
    this->port = port;
    this->speed = speed;
};

void Motor::driveForwardForTime(long ms) {
    motor(this->port, this->speed);
    msleep(ms);
    off(this->port);
}

void Motor::driveForTime(bool direction, long ms) {
    
}
