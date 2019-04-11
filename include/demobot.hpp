#ifndef _DEMOBOT_H_
#define _DEMOBOT_H_

#define between_analog 1500
#define line 0
#define light 4
#define sonar 5
#define close 2550
#define touch 0
#define untouched 0
#define left_wheel 1
#define right_wheel 3
#define fast 200
#define medium 100
#define slow 10
#define arm 2
#define arm_up 200
#define arm_between 800
#define arm_down 1400
#define claw 1
#define claw_open 1600
#define claw_close 325
#define claw_close_object 275
#define silver 3700
#define top_hat_left 3
#define top_hat_right 1
#define buff 15

void white_board_backwards();
void white_board_forward();
void black_line_forward();
void black_line_backwards();
void follow_line_untouched();
void drive_forward_time();
void drive_backwards_time();
void turn_left();
void turn_right();
void turn_left_fast();
void turn_right_fast();
void follow_line_close();
void follow_line_th_left();
void follow_line_th_right();
void black_line_forward_th();
void black_line_backwards_th();
void white_board_forward_th();
void white_board_backwards_th();
void drive_forward_untouched();
void turn_left_th();
void turn_right_th();
void demo_stay();
void close_up();
void open_down();
void move_ambulance();
void single_firefighter_pickup();
void check_camera();
void right_firetruck();
void left_firetruck();
void left_firefighters();
void right_firefighters();

#endif
