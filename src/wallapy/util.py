from __future__ import print_function
from sensors import r_button, analog, r_clicked
from motors import ao
from servos import disable_servos
from time import sleep
from threading import Timer
import walla as w
import os
w = w.w

createObject = None


def beep():
    """
    @summary: lets the controller beep
    """

    os.system('aplay /usr/share/beep.wav 2> /dev/null')


def set_digital_output(port, value):
    """
    @summary: sets a digital port to output the given value
    @param port: the port which should output the value
    @type port: number
    @param value: the value to set the port to
    @type value: bool
    """

    w.set_digital_direction(port, 1)
    w.set_digital_value(port, value)


def set_digital_input(port):
    """
    @summary: sets a digital port to receive input
    @param port: the port which should receive input
    @type port: number
    """

    w.digital_output(port, 0)


def wait_for_light(port, create=None):
    """
    @summary: first calibrates the light sensor, then waits until the light is turned on
    @param port: the port on which the sensor is connected
    @type port: number
    """

    ok = 0
    while not ok:
        print("Press R when the light is on")
        if create is not None:
            create.send_command_ASCII('163 127 0 0 0')
        while not r_button():
            print("Current light level is", str(analog(port)), end='\r')
            sleep(0.05)
        l_on = analog(port)
        r_clicked()
        print("Press R when the light is off")
        if create is not None:
            create.send_command_ASCII('163 127 127 0 0')
        while not r_button():
            print("Current light level is", str(analog(port)), end='\r')
            sleep(0.05)
        l_off = analog(port)
        r_clicked()
        mid = l_off - l_on
        if create is not None:
            create.send_command_ASCII('163 127 127 127 0')
        if mid >= 60:
            ok = 1
            print("Calibration successful, difference:", mid)
            while 1:
                if create is not None:
                    create.send_command_ASCII('141 3')
                while analog(port) > mid:
                    pass
                sleep(0.25)
                if analog(port) < mid:
                    if create is not None:
                        create.send_command_ASCII('163 127 127 127 127')
                    return
        else:
            print("Calibration not successful, value difference is not big enough")


def shut_down_in(seconds):
    """
    @summary: lets the bot stop all motors and sensors after the given time
    @param seconds: the time to stop after in seconds
    @type seconds: number
    """

    Timer(seconds, shut_down, ()).start()


def shut_down():
    """
    @summary: lets the controller completely shut down everything(stop motors, servos,...)
    """

    ao()
    disable_servos()
    if createObject is not None:
        createObject.stop_all()


def register_create(create):
    """
    @summary: registers a create connection in order for it to be shut down in shut_down_in
    @param create: the create object to register
    @type create: Create
    """

    global createObject
    createObject = create
