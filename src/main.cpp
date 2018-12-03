#include <ths_demobot.h>
#include <ths_demobot/ths_motor.h>
#include <helpers.h>
#include <stdio.h>

using namespace ths_demobot;

int main() {
	print_botball_logo();

	// test motors

	ths_motor motor = ths_basic_motor(1, 1.0);
	ths_servo servo = ths_basic_motor(2, 1.0);

	motor.move(ths_motor_direction::forward, 2); // this is a blocking method, so we don't have to worry about sleeping!
	servo.set_position(0.8);
	
    return 0;
}