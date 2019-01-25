try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor

FORWARD = 0
BACKWARD = 1


class motor(base_motor):

  def move(self, direction, time):
    """Moves the motor.

    Arguments:
      direction {int} -- The direction in which to move the motor.
      time {float} -- The amount of time to move the motor in seconds.
    """

    velocity = map(self.speed, 0.0, 1.0, 0, 100)
    if direction == BACKWARD:
      velocity = -velocity # negate if backwards

    w.motor(self.port, int(velocity))
    w.msleep(int(time * 1000))
    w.off(self.port)