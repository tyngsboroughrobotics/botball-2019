#include <kipr/botball.h>
#include "demobot.h"

int main() {
    enable_servos();
    move_ambulance();
    single_firefighter_pickup();
    check_camera();
    if ((get_object_center_x(0, 0) > 0) && (get_object_center_x(0, 0) < 159)) {
        right_firetruck();
        right_firefighters();
    } else {
        left_firetruck();
        left_firefighters();
    }
    camera_close();
    disable_servos();
    return 0;
}

void white_board_backwards() {
    while (analog(line) < between_analog) {
        motor(left_wheel, -medium);
        motor(right_wheel, -medium + buff);
    }
    ao();
}

void white_board_forward() {
    while (analog(line) < between_analog) {
        motor(left_wheel, medium);
        motor(right_wheel, medium - buff);
    }
    ao();
}

void black_line_forward() {
    while (analog(line) > between_analog) {
        motor(left_wheel, medium);
        motor(right_wheel, medium - buff);
    }
    ao();
}

void black_line_backwards() {
    while (analog(line) > between_analog) {
        motor(left_wheel, -medium);
        motor(right_wheel, -medium + buff);
    }
    ao();
}

void follow_line_untouched(int left_speed, int right_speed) {
    while (digital(touch) == untouched) {
        if (analog(line) > between_analog) {
            motor(left_wheel, left_speed);
            motor(right_wheel, right_speed);
        } else {
            motor(right_wheel, left_speed);
            motor(left_wheel, right_speed);
        }
    }
    ao();
}

void drive_forward_time(int speed, int time) {
    motor(left_wheel, speed);
    motor(right_wheel, speed - buff);
    msleep(time);
    ao();
}

void drive_backwards_time(int speed, int time) {
    motor(left_wheel, -speed);
    motor(right_wheel, -speed + buff);
    msleep(time);
    ao();
}

void turn_left(int speed, int time) {
    motor(right_wheel, speed);
    msleep(time);
    ao();
}

void turn_right(int speed, int time) {
    motor(left_wheel, speed);
    msleep(time);
    ao();
}

void turn_left_fast(int speed, int time) {
    motor(left_wheel, -speed);
    motor(right_wheel, speed);
    msleep(time);
    ao();
}

void turn_right_fast(int speed, int time) {
    motor(left_wheel, speed);
    motor(right_wheel, -speed);
    msleep(time);
    ao();
}

void follow_line_close(int left_speed, int right_speed) {
    while (analog(sonar) < close) {
        if (analog(line) > between_analog) {
            motor(left_wheel, left_speed);
            motor(right_wheel, right_speed);
        } else {
            motor(right_wheel, left_speed);
            motor(left_wheel, right_speed);
        }
    }
    ao();
}

void follow_line_th_left(int left_speed, int right_speed) {
    while (analog(top_hat_left) < silver) {
        if (analog(line) > between_analog) {
            motor(left_wheel, left_speed);
            motor(right_wheel, right_speed);
        } else {
            motor(right_wheel, left_speed);
            motor(left_wheel, right_speed);
        }
    }
    ao();
}

void follow_line_th_right(int left_speed, int right_speed) {
    while (analog(top_hat_right) < silver) {
        if (analog(line) > between_analog) {
            motor(left_wheel, left_speed);
            motor(right_wheel, right_speed);
        } else {
            motor(right_wheel, left_speed);
            motor(left_wheel, right_speed);
        }
    }
    ao();
}

void black_line_forward_th() {
    while (analog(top_hat_left) > silver) {
        motor(left_wheel, medium);
        motor(right_wheel, medium - buff);
    }
    ao();
}

void black_line_backwards_th() {
    while (analog(top_hat_left) > silver) {
        motor(left_wheel, -medium);
        motor(right_wheel, -medium + buff);
    }
    ao();
}

void white_board_forward_th() {
    while (analog(top_hat_left) < silver) {
        motor(left_wheel, medium);
        motor(right_wheel, medium - buff);
    }
    ao();
}

void white_board_backwards_th() {
    while (analog(top_hat_left) < silver) {
        motor(left_wheel, -medium);
        motor(right_wheel, -medium - buff);
    }
    ao();
}

void drive_forward_untouched() {
    while (digital(touch) == untouched) {
        motor(left_wheel, medium);
        motor(right_wheel, medium - buff);
    }
    ao();
}

void turn_left_th() {
    while (analog(top_hat_left) < silver) {
        motor(left_wheel, medium);
    }
    ao();
}

void turn_right_th() {
    while (analog(top_hat_right) < silver) {
        motor(right_wheel, medium);
    }
    ao();
}

void demo_stay(int time) {
    ao();
    msleep(time);
}

void open_down() {
    set_servo_position(claw, claw_open);
    demo_stay(250);
    set_servo_position(arm, arm_down);
    demo_stay(500);
}

void close_up() {
    set_servo_position(claw, claw_close);
    demo_stay(500);
    set_servo_position(arm, arm_up);
    demo_stay(250);
}

void move_ambulance() {
    demo_stay(2000);
    drive_forward_time(fast, 1250);
    white_board_backwards();
    black_line_backwards();
}

void single_firefighter_pickup() {
    turn_right_fast(medium, 550);
    drive_forward_time(fast, 750);
    set_servo_position(claw, claw_close);
    demo_stay(500);
    set_servo_position(arm, arm_up);
    turn_left(-fast, 200);
    demo_stay(250);
    turn_left(medium, 1100);
    drive_forward_time(fast, 500);
    white_board_forward();
    drive_forward_time(fast, 50);
    turn_left(medium, 1100);
    follow_line_th_left(fast, slow);
    turn_right_fast(medium, 550);
    follow_line_untouched(fast, slow);
    drive_backwards_time(fast, 500);
    turn_left_fast(medium, 350);
}

void check_camera() {
    camera_open_black();
    demo_stay(1000);
    for (int trial = 0; trial < 15; trial = trial + 1) {
        camera_update();
    }
}

void right_firetruck() {
    printf("I can see the card! /n");
    set_servo_position(arm, arm_down);
    demo_stay(500);
    turn_right(fast, 150);
    set_servo_position(claw, claw_open);
    demo_stay(250);
    set_servo_position(arm, arm_up);
    demo_stay(250);
    drive_backwards_time(fast, 100);
    turn_right(-fast, 150);
    turn_left(fast, 1800);
    drive_forward_untouched();
    demo_stay(500);
    drive_backwards_time(fast, 350);
    set_servo_position(arm, arm_down);
    turn_left(-fast, 1025);
    white_board_forward();
    drive_backwards_time(fast, 50);
    set_servo_position(claw, claw_close);
    demo_stay(500);
    drive_backwards_time(fast, 250);
    set_servo_position(arm, arm_up);
    turn_right_fast(medium, 300);
    demo_stay(250);
    white_board_forward();
    drive_forward_time(fast, 1400);
    turn_left(fast, 1150);
    drive_forward_time(fast, 50);
    set_servo_position(arm, arm_down);
    demo_stay(250);
    set_servo_position(claw, claw_open);
    demo_stay(250);
    set_servo_position(arm, arm_up);
    demo_stay(250);
    turn_left_fast(medium, 775);
    drive_forward_untouched();
    demo_stay(250);
    drive_backwards_time(fast, 500);
    turn_left(-fast, 1200);
    white_board_forward();
    black_line_forward();
    drive_backwards_time(fast, 50);
}

void left_firetruck() {
    printf("Where the card at?\n");
    turn_left(fast, 750);
    set_servo_position(arm, arm_down);
    white_board_forward();
    set_servo_position(claw, claw_open);
    demo_stay(500);
    set_servo_position(arm, arm_up);
    demo_stay(250);
    turn_left(-fast, 750);
}

void left_firefighters() {
    for (int trial = 0; trial < 5; trial = trial + 1) {
        set_servo_position(arm, arm_up);
        set_servo_position(claw, claw_open);
        demo_stay(500);
        follow_line_close(slow, fast);
        set_servo_position(arm, arm_down);
        demo_stay(500);
        turn_left(fast, 50);
        set_servo_position(claw, claw_close);
        demo_stay(500);
        turn_left(-fast, 50);
        white_board_backwards_th();
        turn_right(fast, 1200);
        drive_forward_time(fast, 1000);
        set_servo_position(claw, claw_open);
        demo_stay(250);
        drive_backwards_time(fast, 1009);
        turn_right(-fast, 1200);
        white_board_backwards_th();
    }
}

void right_firefighters() {
    for (int trial = 0; trial < 5; trial = trial + 1) {
        set_servo_position(arm, arm_up);
        set_servo_position(claw, claw_open);
        demo_stay(500);
        follow_line_close(slow, fast);
        set_servo_position(arm, arm_down);
        demo_stay(500);
        turn_left(fast, 150);
        set_servo_position(claw, claw_close_object);
        demo_stay(500);
        white_board_backwards_th();
        demo_stay(250);
        set_servo_position(arm, arm_up);
        drive_backwards_time(fast, 500);
        demo_stay(250);
        turn_right(fast, 1500);
        drive_forward_time(fast, 500);
        follow_line_th_left(fast, slow);
        turn_left(fast, 250);
        follow_line_untouched(fast, slow);
        drive_backwards_time(fast, 250);
        turn_right(-fast, 1100);
        set_servo_position(arm, arm_down);
        demo_stay(500);
        set_servo_position(claw, claw_open);
        turn_right(fast, 300);
        drive_forward_time(fast, 550);
        drive_backwards_time(fast, 600);
        turn_right(-fast, 200);
        set_servo_position(arm, arm_up);
        demo_stay(250);
        turn_left_fast(medium, 850);
        drive_forward_untouched();
        demo_stay(250);
        drive_backwards_time(fast, 700);
        turn_left(-fast, 1075);
        white_board_forward();
        black_line_forward();
        drive_backwards_time(fast, 50);
    }
}
