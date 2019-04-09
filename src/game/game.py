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

    wheels.turn_right(7.5) # in degrees
    
    arm_servo.set_position(0.32) # 0.4 makes the plow touch the table (don't set it to more than this)
    
    wheels.drive(280) # in mm
    wheels.turn_left(140)

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
        # The second building is the safe one; drive up to it 
        # before dispensing
        wheels.turn_right(45)
        wheels.drive(250)
        
    # drive up to the building and dispense the ambulance there
    wheels.drive(50)
    wheels.drive(100, direction=motor.BACKWARD)

    print '**** Step 3 done ****'

def step_4_pickup_firetruck():
    print '**** Step 4: Pickup the firetruck ****'

    arm_servo.set_position(0.32) # TEMPORARY

    if burning_building == FIRST:
        # Turn around and grab the firetruck cube
        wheels.drive(530, direction=motor.BACKWARD)
        wheels.turn_right(135)
        wheels.drive(240)

        # Drive up to the building
        wheels.turn_left(200)
        wheels.drive(500)

        # Move to the black line and wait
        pass
    else:
        # Turn around and grab the firetruck cube
        wheels.turn_left(245)
        wheels.drive(380)

        # Drive up to the building
        wheels.turn_left(242)
        wheels.drive(700)
        wheels.drive(350, direction=motor.BACKWARD)

        # Turn around to the black line and wait
        wheels.turn_right(180)

    print '**** Step 4 done ****'

def run():
    print '**** Running game ****'

    reset()
 
    step_1_get_ambulance()
    step_2_drive_over_to_buildings()
    step_3_put_ambulance_in_safe_building()
    # global burning_building
    # burning_building = FIRST 
    step_4_pickup_firetruck()

    finish()

    print '**** Game done ***'
