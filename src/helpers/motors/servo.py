try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from base_motor import base_motor

SERVO_MIN_POSITION = 300
"""The minimum position allowed to safely move a servo.
"""

SERVO_MAX_POSITION = 1947
"""The maximum position allowed to safely move a servo.
"""


class servo(base_motor):

  def __init__(self, port, speed):
    """Creates a new servo and enables it.

    Arguments:
      port {int} -- The GPIO port of the servo. See Wallaby documentation for details.
      speed {float} -- The speed of the servo. 0.0 is the slowest, 1.0 is the fastest.
    """

    base_motor.__init__(self, port, speed)
    self.real_position = 0

  def set_position(self, position):
    """Sets the servo position.

    Arguments:
      position {float} -- Specify a value between 0.0 and 1.0, where
      0.0 is the leftmost position and 1.0 is the rightmost.
    """
    self.enable()

    initial_pos = self.real_position

	  # limit the servo range to ~100 in between its actual bounds to avoid breaking the servo
    mapped_position = int(map(position, 0.0, 1.0, SERVO_MIN_POSITION, SERVO_MAX_POSITION))

    difference = mapped_position - initial_pos
    sign = 1 if difference >= 0 else -1
    distance = abs(difference)
    ticks = self.__get_ticks()

    x = 0
    while x < distance:
      self.__update_position(initial_pos + (sign * x))
      w.msleep(ticks)
      x += 1
    
    w.msleep(100) # just wait a little bit longer for the servo to finish
    self.disable()

  def __update_position(self, position): 
    w.set_servo_position(self.port, int(position))
    self.real_position = position

  def position(self):
    """The current position of this servo, mapped to between 0.0 and 1.0.

    Returns:
      float -- The position (between 0.0 and 1.0).
    """

    return map(self.real_position, SERVO_MIN_POSITION, SERVO_MAX_POSITION, 0.0, 1.0)

  def enable(self):
    """Enables the servo on the robot.
    """

    w.enable_servo(self.port)

  def disable(self):
    """Disbles the servo on the robot.
    """

    w.disable_servo(self.port)

  def __get_ticks(self):
    """Returns the amount of time spent between each increment of the servo
    position, based on `self.speed`.

    Returns:
      int -- The amount of time in milliseconds.
    """

    return int(map(1.0 - self.speed, 0.0, 1.0, 0.0, 5.0))
