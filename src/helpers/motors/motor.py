try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor
from src.helpers.functions import map

TICKS_IN_1_MM = 1.0/1.13  # looks weird, but we did the measurement :)

FORWARD = 0
BACKWARD = 1


class motor(base_motor):

  def __wait_until_done(self):
    while not w.get_motor_done(self.port):
      w.msleep(2)

  def __mm_to_ticks(self, mm):
    return TICKS_IN_1_MM * mm

  def move(self, direction, distance, block=False):
    """Moves the motor.

    Arguments:
      direction {int} -- The direction in which to move the motor.
      distance {int} -- The distance to move the motor in mm.
      block {bool} -- Whether to block the thread until finished. (Default: `False`)
    """

    velocity = map(self.speed, 0.0, 1.0, 0, 1000)
    distance_in_ticks = self.__mm_to_ticks(distance)

    print '***', distance, '==>', distance_in_ticks

    w.move_relative_position(self.port, int(velocity), int(-distance_in_ticks if direction == BACKWARD else distance_in_ticks))

    if block:
      w.block_motor_done(self.port)


# Some helper functions

TURN_90_DEGREE_AMOUNT = 9 # amount in mm (sent to the wheel_group.drive method)


class wheel_group(object):
    """Represents a group of two motors representing a left
    and right wheel.
    """

    def __init__(self, left, right):
        self.left_motor = left
        self.right_motor = right

    def drive(self, left_distance, right_distance = None, direction = FORWARD, block = True):
        """
        Drives both motors and blocks (by default) until they finish.

        Amount is in mm. If `right_distance` is omitted then
        `left_distance` is used for both motors.
        """
        self.left_motor.move(direction, left_distance)
        self.right_motor.move(direction, (right_distance if right_distance is not None else left_distance), block=block)

    # Helpers for turning in place

    def turn_90_right(self):
        self.drive(TURN_90_DEGREE_AMOUNT, -TURN_90_DEGREE_AMOUNT)

    def turn_90_left(self):
        self.drive(-TURN_90_DEGREE_AMOUNT, TURN_90_DEGREE_AMOUNT)

    def turn_180_right(self):
        self.drive(TURN_90_DEGREE_AMOUNT * 2, -(TURN_90_DEGREE_AMOUNT * 2))

    def turn_180_left(self):
        self.drive(-(TURN_90_DEGREE_AMOUNT * 2), TURN_90_DEGREE_AMOUNT)
