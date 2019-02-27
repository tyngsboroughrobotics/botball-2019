try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo

# Set up motors/servos

left_motor = motor.motor(port=0, speed=1.0)
right_motor = motor.motor(port=1, speed=1.0)
wheels = motor.wheel_group(left_motor, right_motor)

arm_servo = servo.servo(port=3, speed=0.7)

def reset():
    print '**** Resetting servos ***'

    arm_servo.set_position(0)

    print '**** Resetting done ****'

# Step 1: Grab the firefighter on the edge of the starting block
def step_1_get_firefighter():
    print '**** Step 1: Get the firefighter ****'

    wheels.drive(2000) # move forward 20 cm (2000 mm)
    wheels.turn_90_right()
    wheels.drive(1900)

    print '**** Step 1 done ****'

def run():
    print '**** Running game ****'

    reset()
    step_1_get_firefighter()
