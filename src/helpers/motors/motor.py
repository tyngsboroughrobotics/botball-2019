try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor
from src.helpers.functions import map

TICKS_IN_1_MM = 1.0/1.13  # looks weird, but we did the measurement :)
MAX_MOTOR_SPEED = 1500  # in ticks/second

FORWARD = 0
BACKWARD = 1


class motor(base_motor):

  def __mm_to_ticks(self, mm):
    return TICKS_IN_1_MM * mm * 10

  def __ticks_to_ms(self, ticks):
    h = int((abs(ticks) / self.__get_velocity()))
    print '^^^^', h
    return h

  def __get_velocity(self):
    return int(map(self.speed, 0.0, 1.0, 0, MAX_MOTOR_SPEED))

  def move(self, direction, distance, block=False):
    """Moves the motor.

    Arguments:
      direction {int} -- The direction in which to move the motor.
      distance {int} -- The distance to move the motor in mm.
      block {bool} -- Whether to block the thread until finished. (Default: `False`)
    """

    velocity = self.__get_velocity()
    distance_in_ticks = self.__mm_to_ticks(distance)

    w.mav(self.port, velocity)

    if block:
        w.msleep(self.__ticks_to_ms(distance_in_ticks))
        self.off()

  def off(self):
    w.off(self.port)

def all_motors_off():
    w.ao()


# Some helper functions

TURN_DEGREE_AMOUNT = 1 # amount in mm (sent to the wheel_group.drive method)

class wheel_group(object):
    """Represents a group of two motors representing a left
    and right wheel.
    """

    def __init__(self, left, right, left_offset = 1, right_offset = 1):
        self.left_motor = left
        self.right_motor = right
        self.left_offset = left_offset
        self.right_offset = right_offset

    def drive(self, left_distance, right_distance = None, direction = FORWARD, block = True, offset = True):
        """
        Drives both motors and blocks (by default) until they finish.

        Amount is in mm. If `right_distance` is omitted then
        `left_distance` is used for both motors.

        If you don't `block`, then you're responsible for calling `off()` 
        on the motors you drive!
        """

        ld = left_distance
        rd = right_distance if right_distance is not None else left_distance

        if offset:
            ld *= self.left_offset
            rd *= self.right_offset

        self.left_motor.move(direction, ld)
        self.right_motor.move(direction, rd, block=block)

    # Helpers for turning in place

    def turn_right(self, degrees, block = True):
        self.drive(TURN_DEGREE_AMOUNT * degrees, -TURN_DEGREE_AMOUNT * degrees, offset=False, block=block)

    def turn_left(self, degrees, block = True):
        self.turn_right(-degrees, block=block)
