try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo
from src.helpers.cameras import camera as _camera

# Set up motors/servos

# the right motor veers off a bit, so we make the left wheel a bit slower
# to have the robot move in a straight line
LEFT_MOTOR_OFFSET = 0.96
RIGHT_MOTOR_OFFSET = 1

left_motor = motor.motor(port=1, speed=1.0)
right_motor = motor.motor(port=3, speed=1.0) 
wheels = motor.wheel_group(
    left_motor, right_motor, 
    left_offset=LEFT_MOTOR_OFFSET, right_offset=RIGHT_MOTOR_OFFSET
)

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
    w.msleep(500)
    arm_servo.set_position(0.35) # 0.4 makes the plow touch the table (don't set it to more than this)
    wheels.drive(100) # in mm
    w.msleep(500)
    wheels.turn_left(70)
    w.msleep(500)

    print '**** Step 1 done ****'

# Drive over with the cube to the burning buildings
def step_2_drive_over_to_buildings():
    print '**** Step 2: Drive over to buildings'

    arm_servo.set_position(0.35) # TEMPORARY

    wheels.drive(350); w.msleep(500)
    wheels.turn_right(45); w.msleep(500)
    wheels.drive(250); w.msleep(500)
    wheels.turn_right(45); w.msleep(500)
    wheels.drive(250); w.msleep(500)
    wheels.turn_left(90); w.msleep(500)


    print '**** Step 2 done ****'

# Check which building is the burning one, and dispense the cube in front of it
def step_3_put_cube_in_burning_building():
    print '**** Step 3: Put firefighter in burning building **'

    with _camera.camera(color='yellow') as camera:
        if camera.object_is_present() and camera.is_current_object_trackable():
            pass # Dispense the object
        else:
            pass # Move to the second building and dispense it there

    print '**** Step 3 done ****'

def run():
    print '**** Running game ****'

    # reset()
 
    step_1_get_firefighter()

    # finish()

    print '**** Game done ***'