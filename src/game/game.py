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

# Step 1: Grab the ambulance on the right edge of the starting block
def step_1_get_ambulance():
    print '**** Step 1: Get the ambulance ****'

    # From the starting box, turn and face the ambulance. Put the plow down and drive it over
    # to the ambulance so it's in the plow

    arm_servo.set_position(0)

    wheels.turn_right(20) # in degrees
    
    arm_servo.set_position(0.32) # 0.4 makes the plow touch the table (don't set it to more than this)
    
    wheels.drive(280) # in mm
    wheels.turn_left(145)

    print '**** Step 1 done ****'

# Drive over with the ambulance to the burning buildings
def step_2_drive_over_to_buildings():
    print '**** Step 2: Drive over to buildings'

    arm_servo.set_position(0.32) # TEMPORARY

    wheels.drive(1350)

    print '**** Step 2 done ****'

# Store which building is burning so we know which building is safe later on 
burning_building = None
FIRST = 0; SECOND = 1

# Check which building is the safe one, and dispense the ambulance in front of it
def step_3_put_ambulance_in_safe_building():
    print '**** Step 3: Put ambulance in safe building **'
    global burning_building

    arm_servo.set_position(0.32) # TEMPORARY

    # drive up to the building and leave the cube there
    def dispense_object():
        wheels.drive(50)
        wheels.drive(100, direction=motor.BACKWARD)

    # Detect which building is burning and which is safe

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
                    print 'The first building is burning!'
                    burning_building = FIRST
                else:
                    raise ObjectIsAtSecondBuilding()
            else:
                raise ObjectIsAtSecondBuilding()
        except ObjectIsAtSecondBuilding:
            print 'The second buildng is burning!'
            burning_building = SECOND

    # Place the ambulance in the safe building

    if burning_building == FIRST:
        # The second building is the safe one
        wheels.turn_right(45)
        wheels.drive(250)

        dispense_object()

        # Move to the center black line from the second building 
        wheels.drive(100, direction=motor.BACKWARD)
        wheels.turn_right(120)   
        wheels.drive(100)
        wheels.turn_right(45)     
    else:
        # The first building is the safe one
        dispense_object()

        # Move to the center black line from the first building
        wheels.turn_right(245)
        wheels.drive(50)

    print '**** Step 3 done ****'

def run():
    print '**** Running game ****'

    reset()
 
    # step_1_get_ambulance()
    # step_2_drive_over_to_buildings()
    step_3_put_ambulance_in_safe_building()
    # w.msleep(0) # TODO: Wait for the Create to get out of the way before continuing
    # # TODO: Step 4

    finish()

    print '**** Game done ***'