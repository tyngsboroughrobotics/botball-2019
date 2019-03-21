try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor
from src.helpers.functions import map

TICKS_IN_1_MM = 1.0/1.13  # looks weird, but we did the measurement :)
TICKS_PER_SECOND = 818  # also our own measurement because 1000/1500 tps is way too much

FORWARD = 0
BACKWARD = 1

MOTOR_MSLEEP_TIME = 300  # in ms


class motor(base_motor):

  def __mm_to_ticks(self, mm):
    return TICKS_IN_1_MM * mm * 10

  def velocity(self):
    return int(map(self.speed, 0.0, 1.0, 0, TICKS_PER_SECOND))

  def __ticks_to_ms(self, ticks):
    print 'self.speed =', self.speed
    print 'velocity =', abs(self.velocity())
    print 'TPS/velocity =', abs(TICKS_PER_SECOND / self.velocity())
    print 'ticks*(TPS/v) =', abs(ticks * (TICKS_PER_SECOND / self.velocity()))

    return abs(int(ticks * (TICKS_PER_SECOND / self.velocity())))

  def move(self, direction, distance, block=True, sleep=True):
    """Moves the motor.

    Arguments:
      direction {int} -- The direction in which to move the motor.
      distance {int} -- The distance to move the motor in mm.
      block {bool} -- Whether to block the thread until finished. (Default: `True`)
                      If you don't block the thread, you are responsible for calling
                      `off()` on the motor!
      sleep {bool} -- Whether to sleep for a little while (~500ms) after the motor
                      finishes driving. You should probably keep this set to `True`
                      unless you have a sleep somewhere else in the program, because
                      not sleeping will cause the motor to sometimes finish too early.
                      (not fun to debug)
    """

    velocity = self.velocity()
    if direction == BACKWARD:
      velocity *= -1

    w.mav(self.port, velocity)

    if block:
      distance_in_ticks = self.__mm_to_ticks(distance)
      ms = self.__ticks_to_ms(distance_in_ticks)

      w.msleep(ms)
      w.off(self.port)

    if sleep:
      w.msleep(MOTOR_MSLEEP_TIME)

# Some helper functions

TURN_DEGREE_AMOUNT = 0.85 # amount in mm (sent to the wheel_group.drive method)

class wheel_group(object):
    """Represents a group of two motors representing a left
    and right wheel.
    """

    def __init__(self, left, right, left_offset = 1, right_offset = 1):
        self.left_motor = left
        self.right_motor = right
        self.left_offset = left_offset
        self.right_offset = right_offset

        self.left_motor.speed *= left_offset
        self.right_motor.speed *= right_offset

    def drive(self, left_distance, right_distance = None, left_direction = FORWARD, right_direction = None, block = True, sleep = True, offset = True):
        """
        Drives both motors and blocks (by default) until they finish.
        Amount is in mm. If `right_distance` is omitted then
        `left_distance` is used for both motors.
        If you don't `block`, then you're responsible for calling `off()` 
        on the motors you drive!
        See `motor.move` for documentation on the `sleep` parameter.
        """

        ld = left_distance
        rd = right_distance if right_distance is not None else left_distance

        ldir = left_direction
        rdir = right_direction if left_direction is not None else left_direction

        if offset:
            ld *= self.left_offset
            rd *= self.right_offset

        self.left_motor.move(ldir, ld, block=False, sleep=False)
        self.right_motor.move(rdir, rd, block=block, sleep=False)

        if block:
          w.off(self.left_motor.port)

        if sleep:
          w.msleep(MOTOR_MSLEEP_TIME)

    # Helpers for turning in place

    def turn_right(self, degrees, block = True, sleep = True):
        self.drive(TURN_DEGREE_AMOUNT * degrees, left_direction=BACKWARD, right_direction=FORWARD, offset=False, sleep=sleep, block=block)

    def turn_left(self, degrees, block = True, sleep = True):
        self.turn_right(-degrees, block=block, sleep=sleep)
