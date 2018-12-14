import walla as w
w = w.w


def disable_servo(port):
    """
    @summary: disables a servo
    @param port: the port of the servo
    @type port: number
    """

    w.disable_servo(port)


def disable_servos():
    """
    @summary: disables all servos
    """

    w.disable_servos()


def enable_servo(port):
    """
    @summary: enables a servo
    @param port: the port of the servo
    @type port: number
    """

    w.enable_servo(port)


def enable_servos():
    """
    @summary: enables all servos
    """

    w.enable_servos()


def is_servo_enabled(port):
    """
    @summary: determines if a servo is enabled
    @param port: the port of the servo
    @type port: number
    @return: if the servo is enabled
    @rtype: bool
    """

    return w.get_servo_enabled(port)


def get_servo_position(port):
    """
    @summary: gets the current position of a servo
    @param port: the port of the servo
    @type port: number
    @return: the current position of the servo between 0 and 2047
    @rtype: number
    """

    return w.get_servo_position(port)


def set_servo_position(port, pos):
    """
    @summary: sets the position of a servo
    @param port: the port of the servo
    @type port: number
    @param pos: the position to set the servo to
    @type pos: number
    """

    w.set_servo_position(port, pos)
