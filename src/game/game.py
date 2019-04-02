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
LEFT_MOTOR_OFFSET = 0.98
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
    arm_servo.set_position(0)

    wheels.turn_left(20) # in degrees
    
    arm_servo.set_position(0.35) # 0.4 makes the plow touch the table (don't set it to more than this)
    
    wheels.drive(100) # in mm
    wheels.turn_left(70)

    print '**** Step 1 done ****'

# Drive over with the cube to the burning buildings
def step_2_drive_over_to_buildings():
    print '**** Step 2: Drive over to buildings'

    arm_servo.set_position(0.35) # TEMPORARY

    # # "Swoop around" to get the fire truck along the way 
    # wheels.drive(350)
    # # wheels.turn_left(10)
    # # wheels.drive(200)
    # # wheels.turn_right(60)
    # # wheels.drive(100)
    # return

    wheels.drive(350)
    wheels.turn_right(45)
    wheels.drive(250)
    wheels.turn_right(45)
    wheels.drive(250)
    wheels.turn_left(105)


    print '**** Step 2 done ****'

# Store which building is burning so we know which building is safe later on 
burning_building = None
FIRST = 0; SECOND = 1

# Check which building is the burning one, and dispense the cube in front of it
def step_3_put_cube_in_burning_building():
    print '**** Step 3: Put firefighter in burning building **'
    global burning_building

    # drive up to the building and leave the cube there
    def dispense_object():
        wheels.drive(50)
        wheels.drive(100, direction=motor.BACKWARD)

    class ObjectIsAtSecondBuilding(Exception): pass

    with _camera.camera(color='yellow') as camera:
        try:
            # make sure that both a yellow AND red object is present (the marker
            # is yellow with a red circle in the middle)
            if camera.is_current_object_trackable(should_update=False):
                print 'Yellow marker successfully detected'

                camera.change_color_to('red')

                if camera.is_current_object_trackable(should_update=False):
                    print 'Red marker successfully detected'
                    print 'Object is at first building!'
                    burning_building = FIRST

                    dispense_object()

                    # Move to the center black line from the first building
                    wheels.turn_right(230)
                    wheels.drive(50)
                else:
                    raise ObjectIsAtSecondBuilding()
            else:
                raise ObjectIsAtSecondBuilding()
        except ObjectIsAtSecondBuilding:
            print 'Object is at second building!'
            burning_building = SECOND

            # Move to the second building
            wheels.turn_right(45)
            wheels.drive(250)

            dispense_object()

            # Move to the center black line from the second building 
            wheels.drive(100, direction=motor.BACKWARD)
            wheels.turn_right(130)

    print '**** Step 3 done ****'

def run():
    print '**** Running game ****'

    reset()
 
    step_1_get_firefighter()
    step_2_drive_over_to_buildings()
    step_3_put_cube_in_burning_building()
    w.msleep(0) # TODO: Wait for the Create to get out of the way before continuing
    # TODO: Step 4

    finish()

    print '**** Game done ***'