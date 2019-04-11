# -*- coding: utf-8 -*-

try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo
from src.helpers.create import create as _create

# Set up motor/servo

servo.SERVO_MIN_POSITION = 98

guide_motor = motor.motor(port=0, speed=1.0)
arm_servo = servo.servo(port=3, speed=1.0)

# Set up Create 

create = _create.create(speed=150)

def reset():
    print '**** Resetting ****'

    arm_servo.set_position(0.5)

    print '**** Resetting done ****'

def finish():
    print '**** Finishing ****'

    arm_servo.set_position(0.5)

    print '**** Done finishing ****'

# Give up ¯\_(ツ)_/¯
def step_1_give_up():
    # Drive up to the center of the board
    # We're going to write a Create library eventually so we don't 
    # have to do this mess :)
    VEL = 225
    w.create_spin_CCW(VEL)
    w.msleep(1200)
    w.create_stop()
    w.create_drive_straight(VEL)
    w.msleep(2750)
    w.create_stop()
    w.create_spin_CW(VEL)
    w.msleep(1000)
    w.create_stop()
    w.create_drive_straight(VEL)
    w.msleep(2000)
    w.create_stop()
    w.create_spin_CW(VEL)
    w.msleep(500)
    w.create_stop()
    w.create_drive_straight(VEL)
    w.msleep(3000)
    w.create_stop()
    w.msleep(2000) 

    # Spin around in circles forever
    w.create_spin_CW(50)

    def write(bytes):
        for byte in bytes:
            w.create_write_byte(byte)

    # Play a song :)
    write([
        140, 0, 13,

        48, 16,
        62, 16,
        64, 16,
        65, 16,

        67, 16,
        69, 16,
        71, 16,
        69, 16,

        67, 16,
        65, 16,
        64, 16,
        62, 16,
        
        48, 16,
    ])

    while True:
        write([141, 0]); w.msleep(1650)

def run():
    print '**** Running game ****'

    reset()
    
    step_1_give_up()

    finish()
