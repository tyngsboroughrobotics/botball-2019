#include "ths_demobot/ths_motor.h"
#include <kipr/botball.h>

using namespace ths_demobot;

ths_basic_motor::ths_basic_motor(int port, float speed) {
    this->port = port;
    this->speed = speed;
}

void ths_motor::move(double time) {
    motor(this->port, (int) this->speed);
    block_motor_done(this->port);
}