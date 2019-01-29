try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.cameras.camera import camera as _camera
from src.helpers.motors import motor

OBJECT_TO_FOLLOW_COLOR = 'green'  # red | yellow | green
OBJECT_HEIGHT = 48  # in mm (this is currently representing the little foam blocks)

def follow_object():
    left_motor = motor.motor(port=0, speed=1.0)
    right_motor = motor.motor(port=1, speed=1.0)

    def drive_both_motors(amount):
        left_motor.move(motor.FORWARD, amount)
        right_motor.move(motor.BACKWARD, amount, block=True)

    with _camera(color=OBJECT_TO_FOLLOW_COLOR) as camera:
        previous_distance_to_object = None  # initialize to None; it'll be updated later

        while True:
            if camera.object_is_present() and camera.is_current_object_trackable():

                #### Move robot toward/away from object ####

                distance_to_object = camera.distance_to_current_object(OBJECT_HEIGHT)

                # If it is None, that means that we just started up (so of course there's no change yet).
                # The previous_distance_to_object is initialized if it is.
                if previous_distance_to_object is not None:
                    distance_change = previous_distance_to_object - distance_to_object

                    if abs(distance_change) >= 10:
                        # the object moved; move the robot to follow it

                        amount_to_move = distance_change * 5  # TODO: IMPLEMENT THIS!
                        print '*** amount_to_move =', amount_to_move
                        drive_both_motors(amount_to_move)
                        
                    previous_distance_to_object = distance_to_object
                else:
                    previous_distance_to_object = distance_to_object  # initialize previous_distance_to_object
