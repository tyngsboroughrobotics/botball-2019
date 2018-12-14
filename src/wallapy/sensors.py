import walla as w
from time import sleep
from math import atan2, sin, cos, sqrt, pi, atan
w = w.w
magneto_calibration = 0


def r_button():
    """
    @summary: gets the state of the R button
    @return: 1 if the button is pressed, 0 otherwise
    @rtype: bool
    """

    return w.digital(13)


def l_button():
    """
    @summary: gets the state of the L button
    @return: 1 if the button is pressed, 0 otherwise
    @rtype: bool
    """

    return w.digital(12)  # TODO: always return 1 -> wrong code?


def wait_for_r():
    """
    @summary: waits until the R button is pressed
    """

    while not r_button():
        sleep(0.01)


def wait_for_l():
    """
    @summary: waits until the L button is pressed
    """

    while not l_button():
        sleep(0.01)


def r_clicked():
    """
    @summary: waits for the R button to be clicked and released
    """

    wait_for_r()
    while r_button():
        sleep(0.01)


def l_clicked():
    """
    @summary: waits for the L button to be clicked and released
    """

    wait_for_l()
    while l_button():
        sleep(0.01)


def accel_x():
    """
    @summary: gets the value of the accelerometer in its x direction
    @return: the accelerometer value
    @rtype: number
    """

    return w.accel_x()


def accel_y():
    """
    @summary: gets the value of the accelerometer in its y direction
    @return: the accelerometer value
    @rtype: number
    """

    return w.accel_y()


def accel_z():
    """
    @summary: gets the value of the accelerometer in its z direction
    @return: the accelerometer value
    @rtype: number
    """

    return w.accel_z()


def analog(port):
    """
    @summary: gets the sensor value for an analog sensor
    @param port: the port of the sensor
    @type port: number
    @return: the sensor value between 0 and 1023
    @rtype: number
    """

    return w.analog(port)


def analog_et(port):
    """
    @summary: gets the sensor value for an ET sensor
    @param port: the port of the sensor
    @type port: number
    @return: the sensor value between 0 and 1023
    @rtype: number
    """

    return w.analog_et(port)


def analog8(port):
    """
    @summary: gets the sensor value for an analog sensor as an 8-bit integer
    @param port: the port of the sensor
    @type port: number
    @return: the sensor value between 0 and 255
    @rtype: number
    """

    return w.analog8(port)


def digital(port):
    """
    @summary: gets the sensor value for a digital sensor
    @param port: the port of the sensor
    @type port: number
    @return: if the sensor is activated
    @rtype: bool
    """

    return w.digital(port)


def power_level():
    """
    @summary: gets the controller power level
    @return: the power level between 0 and 1000
    @rtype: number
    """

    return w.power_level()


def gyro_x():
    """
    @summary: gets the value of the gyroscope in its x direction
    @return: the gyroscope value
    @rtype: number
    """

    return w.gyro_x()


def gyro_y():
    """
    @summary: gets the value of the gyroscope in its y direction
    @return: the gyroscope value
    @rtype: number
    """

    return w.gyro_y()


def gyro_z():
    """
    @summary: gets the value of the gyroscope in its z direction
    @return: the gyroscope value
    @rtype: number
    """

    return w.gyro_z()


def magneto_x():
    """
    @summary: gets the value of the magnetometer in its x direction
    @return: the magnetometer value
    @rtype: number
    """

    return w.magneto_x()


def magneto_y():
    """
    @summary: gets the value of the magnetometer in its y direction
    @return: the magnetometer value
    @rtype: number
    """

    return w.magneto_y()


def magneto_z():
    """
    @summary: gets the value of the magnetometer in its z direction
    @return: the magnetometer value
    @rtype: number
    """

    return w.magneto_z()


def compass():
    """
    @summary: gets the compass heading of the bot. Magnetometers have to be calibrated in order for this function to work
    @return: the compass value in deg
    @rtype: number
    """

    accx = sensors.accel_x() * 0.00981
    accy = sensors.accel_y() * 0.00981
    accz = sensors.accel_z() * 0.00981
    x = sensors.magneto_x() + get_magneto_calibration_x()
    y = sensors.magneto_y() + get_magneto_calibration_y()
    z = sensors.magneto_z() - get_magneto_calibration_z()
    roll = atan(accy / sqrt(accx * accx + accz * accz))
    pitch = atan(-accx / accz)
    xh = x * cos(pitch) + z * sin(pitch)
    yh = x * sin(roll) * sin(pitch) + y * \
        cos(roll) - z * sin(roll) * cos(pitch)
    heading = atan2(yh, xh) / pi * 180 + 180
    return heading


def compass_x():
    """
    @summary: gets the compass heading while the wallaby is lying flat on the x axis
    @return: the compass heading in deg
    @rtype: number
    """

    y = sensors.magneto_y() + get_magneto_calibration_y()
    z = sensors.magneto_z() + get_magneto_calibration_z()
    return atan2(y, z) / pi * 180


def compass_y():
    """
    @summary: gets the compass heading while the wallaby is lying flat on the y axis
    @return: the compass heading in deg
    @rtype: number
    """

    x = sensors.magneto_x() + get_magneto_calibration_x()
    z = sensors.magneto_z() + get_magneto_calibration_z()
    return atan2(z, x) / pi * 180


def compass_z():
    """
    @summary: gets the compass heading while the wallaby is lying flat on the z axis
    @return: the compass heading in deg
    @rtype: number
    """

    x = sensors.magneto_x() + get_magneto_calibration_x()
    y = sensors.magneto_y() + get_magneto_calibration_y()
    return atan2(y, x) / pi * 180


def get_magneto_calibration():
    """
    @summary: reads the magnetometer calibration from the file
    """

    f = open("/home/root/magnetoCalibrate", "r")
    magneto_calibration = f.readline()
    f.close()
    if not magneto_calibration:
        raise Exception("Magnetometers are not calibrated")


def get_magneto_calibration_x():
    """
    @summary: gets the magnetometer calibration value for the x axis
    @return: the calibration value
    @rtype: number
    """

    if not magneto_calibration:
        get_magneto_calibration()
    return int(magneto_calibration.split(",")[0])


def get_magneto_calibration_y():
    """
    @summary: gets the magnetometer calibration value for the y axis
    @return: the calibration value
    @rtype: number
    """

    if not magneto_calibration:
        get_magneto_calibration()
    return int(magneto_calibration.split(",")[1])


def get_magneto_calibration_z():
    """
    @summary: gets the magnetometer calibration value for the z axis
    @return: the calibration value
    @rtype: number
    """

    if not magneto_calibration:
        get_magneto_calibration()
    return int(magneto_calibration.split(",")[2])


def calibrate_magneto():
    """
    @summary: calibrates the magnetometer. This process only has to be done once and will be saved to a file after completion; however, when the wallaby is moved to another location significantly(eg. other continent), it should be recalibrated
    """

    print "Please lay the wallaby on a flat surface(display facing up) and press the R button; then spin it one complete circle and press the R button again"
    r_clicked()
    print "Calibrating axis"
    x_values = []
    x_values2 = []
    y_values = []
    z_values = []
    while not r_button():
        sleep(0.1)
        x_values.append(magneto_x())
        y_values.append(magneto_y())
    while r_button():
        sleep(0.1)
    print "Now, repeat the same with the wallaby lying on its side(90deg from previous position; text on display going up)"
    r_clicked()
    print "Calibrating axis"
    while not r_button():
        sleep(0.1)
        x_values2.append(magneto_x())
        z_values.append(magneto_z())
    while r_button():
        sleep(0.1)
    x_max = max(x_values)
    y_zero = y_values[x_values.index(x_max)]
    x_max = max(x_values2)
    z_zero = z_values[x_values2.index(x_max)]
    z_max = max(z_values)
    x_zero = x_values2[z_values.index(z_max)]
    print "Calibrated:", x_zero, y_zero, z_zero
    f = open("/home/root/magnetoCalibrate", "w")
    f.write(str(-x_zero))
    f.write(",")
    f.write(str(-y_zero))
    f.write(",")
    f.write(str(-z_zero))
    f.close()
