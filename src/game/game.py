try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo
from src.helpers.cameras import camera as _camera

# Set up motors/servos

left_motor = motor.motor(port=1, speed=1.0)
right_motor = motor.motor(port=3, speed=1.0)
wheels = motor.wheel_group(left_motor, right_motor)

arm_servo = servo.servo(port=3, speed=0.7)

def reset():
    print '**** Resetting servos ***'

    arm_servo.set_position(0.2)

    print '**** Resetting done ****'

def finish():
    print '**** Finishing procedure ****'

    arm_servo.set_position(0.2)

    print '**** Done finishing ****'

# Step 1: Grab the firefighter on the edge of the starting block
def step_1_get_firefighter():
    print '**** Step 1: Get the firefighter ****'

    # From the starting box, turn and face the firefighter cube. Put the plow down and drive it over
    # to the firefighter cube so the cube is in the plow

    wheels.turn_left(20) # in degrees
    arm_servo.set_position(0.35) # 0.4 makes the plow touch the table (don't set it to more than this)
    wheels.drive(500) # in mm

    # Drive over to the burning buildings

    for _ in range(3):
        wheels.drive(2000)
        wheels.turn_left(15)

    wheels.turn_left(50)
    wheels.drive(1000)

    # Dispense the cube in the burning building

    with _camera.camera(color='yellow') as camera:
        if camera.object_is_present() and camera.is_current_object_trackable():
            pass # Dispense the object
        else:
            pass # Move to the second building and dispense it there

    print '**** Step 1 done ****'

def run():
    print '**** Running game ****'

    reset()
    step_1_get_firefighter()
