#include <ths_demobot/ths_motor.h>
#include <helpers.h>
#include <kipr/botball.h>
#include <kipr/servo.h>
#include <kipr/motors.h>
#include <kipr/util.h>
#include <algorithm>

using namespace ths_demobot;
using namespace ths_helpers;

ths_basic_motor::ths_basic_motor(int port, float speed) {
    this->port = port;
    this->speed = speed;

	enable_servo(port);
}

void ths_motor::move(ths_motor_direction direction, double time) {
	int speed;
	if (direction == ths_motor_direction::forward)
		speed = this->speed * 100;
	else
		speed = this->speed * -100;

    motor(this->port, speed);
    block_motor_done(this->port);
}

int ths_servo::position() {
	return get_servo_position(this->port);
}

void ths_servo::set_position(double position) {
	// limit the servo range to ~100 in between its actual bounds to avoid breaking the servo
	double mapped_position = map(position, 0.0, 1.0, THS_SERVO_MIN_POSITION, THS_SERVO_MAX_POSITION);
	
	int ticks = this->get_ticks(distance)

	while (this->position() < mapped_position) {
		set_servo_position(this->port, this->position() + 1);
		msleep(ticks);
	}
	msleep(100);
}

int ths_servo::get_ticks(int distance) {
	double x = (1.0 - this->speed);
	return (x <= 0) ? 0 : (int)(distance / (x * THS_BASIC_MOTOR_MAX_TIME));
}

void ths_servo::disable() {
	disable_servo(this->port);
}