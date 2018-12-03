#ifndef MOTOR_H
#define MOTOR_H

#include <kipr/botball.h>

namespace ths_demobot {

    /**
     * This is multiplied by basic_motor::speed to achieve the time in
     * seconds required to move the motor.
     */
    const double THS_BASIC_MOTOR_MAX_TIME = 5.0;

    class ths_basic_motor {
    public:
        /**
         * The GPIO port of the motor. See Wallaby documentation for details.
         */
        int port;

        /**
         * The speed of the motor. 0.0 is the slowest, 1.0 is the fastest.
         */ 
        float speed;

        ths_basic_motor(int port, float speed);
    };

    enum class ths_motor_direction: short {
        forward,
        backward
    };

    class ths_motor: ths_basic_motor {
    public:
        /**
         * Moves the motor forward for the specified amount of time in seconds.
         */
		void move(ths_motor_direction direction, double time);
    };

	const int THS_SERVO_MIN_POSITION = 100;
	const int THS_SERVO_MAX_POSITION = 1947;

    class ths_servo: ths_basic_motor {
    public:
		
		/**
		 * Sets the servo position. Specify a value between 0.0 and 1.0,
		 * where 0.0 is the leftmost position and 1.0 is the rightmost.
		 */
        void set_position(double position);

		int position();

		void disable();

	private:
		int get_ticks(int distance);
    };
}

#endif