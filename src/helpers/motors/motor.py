try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor

FORWARD = 0
BACKWARD = 1


class motor(base_motor):

  def move(self, direction, distance, block=False):
    """Moves the motor.

    Arguments:
      direction {int} -- The direction in which to move the motor.
      distance {int} -- The distance to move the motor in mm.
      block {bool} -- Whether to block the thread until finished. (Default: `False`)
    """

    velocity = map(self.speed, 0.0, 1.0, 0, 1000)

    w.move_relative_position(self.port, int(velocity), int(-distance if direction == BACKWARD else distance))

    if block:
      time_to_sleep = NotImplemented # TODO: FINISH THIS!
      w.msleep(int(time_to_sleep))
