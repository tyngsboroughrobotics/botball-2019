import sys; sys.path.append('/home/root/Documents/KISS/Default User/ths-botball-2019/')
try:
    from src.__wallaby_local import *  # for VSCode support
except ImportError:
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    from wallaby import *  # so it works on actual robot

between_analog = 1500
line = 0
light = 4
sonar = 5
close = 2550
touch = 0
untouched = 0
left_wheel = 1
right_wheel = 3
fast = 200
medium = 100
slow = 10
arm = 2
arm_up = 200
arm_between = 800
arm_down = 1400
claw = 1
claw_open = 1600
claw_close = 325
claw_close_object = 275
silver = 3700
top_hat_left = 3
top_hat_right = 1
buff = 15

def main():
    enable_servos()
    move_ambulance()
    single_firefighter_pickup()
    check_camera()
    if ((get_object_center_x(0, 0) > 0) and (get_object_center_x(0, 0) < 159)):
        right_firetruck()
        right_firefighters()
    else:
        left_firetruck()
        left_firefighters()

    camera_close()
    disable_servos()
    return 0


def white_board_backwards():
    while (analog(line) < between_analog):
        motor(left_wheel, -medium)
        motor(right_wheel, -medium + buff)

    ao()


def white_board_forward():
    while (analog(line) < between_analog):
        motor(left_wheel, medium)
        motor(right_wheel, medium - buff)

    ao()


def black_line_forward():
    while (analog(line) > between_analog):
        motor(left_wheel, medium)
        motor(right_wheel, medium - buff)

    ao()


def black_line_backwards():
    while (analog(line) > between_analog):
        motor(left_wheel, -medium)
        motor(right_wheel, -medium + buff)

    ao()

def follow_line_untouched(left_speed, right_speed):
    while (digital(touch) == untouched):
        if (analog(line) > between_analog):
            motor(left_wheel, left_speed)
            motor(right_wheel, right_speed)
        else:
            motor(right_wheel, left_speed)
            motor(left_wheel, right_speed)

    ao()


def drive_forward_time(speed, time):
    motor(left_wheel, speed)
    motor(right_wheel, speed - buff)
    msleep(time)
    ao()


def drive_backwards_time(speed, time):
    motor(left_wheel, -speed)
    motor(right_wheel, -speed + buff)
    msleep(time)
    ao()


def turn_left(speed, time):
    motor(right_wheel, speed)
    msleep(time)
    ao()


def turn_right(speed, time):
    motor(left_wheel, speed)
    msleep(time)
    ao()


def turn_left_fast(speed, time):
    motor(left_wheel, -speed)
    motor(right_wheel, speed)
    msleep(time)
    ao()


def turn_right_fast(speed, time):
    motor(left_wheel, speed)
    motor(right_wheel, -speed)
    msleep(time)
    ao()


def follow_line_close(left_speed, right_speed):
    while (analog(sonar) < close):
        if (analog(line) > between_analog):
            motor(left_wheel, left_speed)
            motor(right_wheel, right_speed)
        else:
            motor(right_wheel, left_speed)
            motor(left_wheel, right_speed)

    ao()


def follow_line_th_left(left_speed, right_speed):
    while (analog(top_hat_left) < silver):
        if (analog(line) > between_analog):
            motor(left_wheel, left_speed)
            motor(right_wheel, right_speed)
        else:
            motor(right_wheel, left_speed)
            motor(left_wheel, right_speed)

    ao()


def follow_line_th_right(left_speed, right_speed):
    while (analog(top_hat_right) < silver):
        if (analog(line) > between_analog):
            motor(left_wheel, left_speed)
            motor(right_wheel, right_speed)
        else:
            motor(right_wheel, left_speed)
            motor(left_wheel, right_speed)

    ao()


def black_line_forward_th():
    while (analog(top_hat_left) > silver):
        motor(left_wheel, medium)
        motor(right_wheel, medium - buff)

    ao()


def black_line_backwards_th():
    while (analog(top_hat_left) > silver):
        motor(left_wheel, -medium)
        motor(right_wheel, -medium + buff)

    ao()


def white_board_forward_th():
    while (analog(top_hat_left) < silver):
        motor(left_wheel, medium)
        motor(right_wheel, medium - buff)

    ao()


def white_board_backwards_th():
    while (analog(top_hat_left) < silver):
        motor(left_wheel, -medium)
        motor(right_wheel, -medium - buff)

    ao()


def drive_forward_untouched():
    while (digital(touch) == untouched):
        motor(left_wheel, medium)
        motor(right_wheel, medium - buff)

    ao()


def turn_left_th():
    while (analog(top_hat_left) < silver):
        motor(left_wheel, medium)

    ao()


def turn_right_th():
    while (analog(top_hat_right) < silver):
        motor(right_wheel, medium)

    ao()


def demo_stay(time):
    ao()
    msleep(time)


def open_down():
    set_servo_position(claw, claw_open)
    demo_stay(250)
    set_servo_position(arm, arm_down)
    demo_stay(500)


def close_up():
    set_servo_position(claw, claw_close)
    demo_stay(500)
    set_servo_position(arm, arm_up)
    demo_stay(250)


def move_ambulance():
    demo_stay(2000)
    drive_forward_time(fast, 1250)
    white_board_backwards()
    black_line_backwards()


def single_firefighter_pickup():
    turn_right_fast(medium, 550)
    drive_forward_time(fast, 750)
    set_servo_position(claw, claw_close)
    demo_stay(500)
    set_servo_position(arm, arm_up)
    turn_left(-fast, 200)
    demo_stay(250)
    turn_left(medium, 1100)
    drive_forward_time(fast, 500)
    white_board_forward()
    drive_forward_time(fast, 50)
    turn_left(medium, 1100)
    follow_line_th_left(fast, slow)
    turn_right_fast(medium, 550)
    follow_line_untouched(fast, slow)
    drive_backwards_time(fast, 500)
    turn_left_fast(medium, 350)


def check_camera():
    camera_open_black()
    demo_stay(1000)
    for _ in range(15):
        camera_update()


def right_firetruck():
    print "I can see the card!"
    set_servo_position(arm, arm_down)
    demo_stay(500)
    turn_right(fast, 150)
    set_servo_position(claw, claw_open)
    demo_stay(250)
    set_servo_position(arm, arm_up)
    demo_stay(250)
    drive_backwards_time(fast, 100)
    turn_right(-fast, 150)
    turn_left(fast, 1800)
    drive_forward_untouched()
    demo_stay(500)
    drive_backwards_time(fast, 350)
    set_servo_position(arm, arm_down)
    turn_left(-fast, 1025)
    white_board_forward()
    drive_backwards_time(fast, 50)
    set_servo_position(claw, claw_close)
    demo_stay(500)
    drive_backwards_time(fast, 250)
    set_servo_position(arm, arm_up)
    turn_right_fast(medium, 300)
    demo_stay(250)
    white_board_forward()
    drive_forward_time(fast, 1400)
    turn_left(fast, 1150)
    drive_forward_time(fast, 50)
    set_servo_position(arm, arm_down)
    demo_stay(250)
    set_servo_position(claw, claw_open)
    demo_stay(250)
    set_servo_position(arm, arm_up)
    demo_stay(250)
    turn_left_fast(medium, 775)
    drive_forward_untouched()
    demo_stay(250)
    drive_backwards_time(fast, 500)
    turn_left(-fast, 1200)
    white_board_forward()
    black_line_forward()
    drive_backwards_time(fast, 50)


def left_firetruck():
    print "Where the card at?"
    turn_left(fast, 750)
    set_servo_position(arm, arm_down)
    white_board_forward()
    set_servo_position(claw, claw_open)
    demo_stay(500)
    set_servo_position(arm, arm_up)
    demo_stay(250)
    turn_left(-fast, 750)


def left_firefighters():
    for _ in range(5):
        set_servo_position(arm, arm_up)
        set_servo_position(claw, claw_open)
        demo_stay(500)
        follow_line_close(slow, fast)
        set_servo_position(arm, arm_down)
        demo_stay(500)
        turn_left(fast, 50)
        set_servo_position(claw, claw_close)
        demo_stay(500)
        turn_left(-fast, 50)
        white_board_backwards_th()
        turn_right(fast, 1200)
        drive_forward_time(fast, 1000)
        set_servo_position(claw, claw_open)
        demo_stay(250)
        drive_backwards_time(fast, 1009)
        turn_right(-fast, 1200)
        white_board_backwards_th()


def right_firefighters():
    for _ in range(5):
        set_servo_position(arm, arm_up)
        set_servo_position(claw, claw_open)
        demo_stay(500)
        follow_line_close(slow, fast)
        set_servo_position(arm, arm_down)
        demo_stay(500)
        turn_left(fast, 150)
        set_servo_position(claw, claw_close_object)
        demo_stay(500)
        white_board_backwards_th()
        demo_stay(250)
        set_servo_position(arm, arm_up)
        drive_backwards_time(fast, 500)
        demo_stay(250)
        turn_right(fast, 1500)
        drive_forward_time(fast, 500)
        follow_line_th_left(fast, slow)
        turn_left(fast, 250)
        follow_line_untouched(fast, slow)
        drive_backwards_time(fast, 250)
        turn_right(-fast, 1100)
        set_servo_position(arm, arm_down)
        demo_stay(500)
        set_servo_position(claw, claw_open)
        turn_right(fast, 300)
        drive_forward_time(fast, 550)
        drive_backwards_time(fast, 600)
        turn_right(-fast, 200)
        set_servo_position(arm, arm_up)
        demo_stay(250)
        turn_left_fast(medium, 850)
        drive_forward_untouched()
        demo_stay(250)
        drive_backwards_time(fast, 700)
        turn_left(-fast, 1075)
        white_board_forward()
        black_line_forward()
        drive_backwards_time(fast, 50)
