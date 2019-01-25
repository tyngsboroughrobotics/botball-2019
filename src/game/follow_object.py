from ..helpers.cameras.camera import camera as _camera
from ..helpers.motors import motor

OBJECT_TO_FOLLOW_COLOR = 'yellow'  # red | yellow | green 
OBJECT_HEIGHT = 48  # in mm (this is currently representing the little foam blocks)

def follow_object():
    left_motor = motor.motor(port=0, speed=1.0)
    right_motor = motor.motor(port=1, speed=1.0)

    def drive_both_motors(amount):
        left_motor.move(motor.FORWARD, amount)
        right_motor.move(motor.BACKWARD, amount, block=True)

    with _camera(color=OBJECT_TO_FOLLOW_COLOR) as camera:
        while True:
            previous_distance_to_object = None  # initialize to None; it'll be updated later

            if camera.object_is_present() and camera.is_current_object_trackable():
                distance_to_object = camera.distance_to_current_object(OBJECT_HEIGHT)

                # If it is None, that means that we just started up (so of course there's no change yet).
                # Rhe previous_distance_to_object is updated below regardless of this check.
                if previous_distance_to_object is not None:
                    distance_change = distance_to_object - distance_to_object

                    if abs(distance_change) >= 5:
                        # the object moved; move the robot to follow it

                        amount_to_move = distance_change * 10  # TODO: IMPLEMENT THIS!
                        drive_both_motors(amount_to_move)

                previous_distance_to_object = distance_to_object
