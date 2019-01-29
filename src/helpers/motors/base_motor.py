try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.functions import map

MOTOR_MAX_TIME = 5.0
"""This is multiplied by `motor.speed` to achieve the time in
seconds required to move the motor.
"""

class base_motor:
  """The base class for motors and servos. Provides a common initializer for
  both by providing a port and speed value.
  """

  def __init__(self, port, speed):
    """Creates a new base_motor.

    Arguments:
      port {int} -- The GPIO port of the motor. See Wallaby documentation for details.
      speed {float} -- The speed of the motor. 0.0 is the slowest, 1.0 is the fastest.
    """

    self.port = port
    self.speed = speed
