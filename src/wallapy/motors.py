import walla as w
import time
from ctypes import c_int, byref
w = w.w

def alloff():
    """
    @summary: turns off all motors
    """

    w.alloff()

def ao():
    """
    @summary: turns off all motors
    """

    alloff()

def bk(port):
    """
    @summary: turns on a motor to full backwards power
    @param port: the port of the motor
    @type port: number
    """

    w.bk(port)

def fd(port):
    """
    @summary: turns on a motor to full power
    @param port: the port of the motor
    @type port: number
    """

    w.fd(port)

def block_motor_done(port):
    """
    @summary: waits until a motor is done moving to its position
    @param port: the port of the motor
    @type port: number
    """

    while not is_motor_done(port):
        time.sleep(0.002)

def bmd(port):
    """
    @summary: waits until a motor is done moving to its position
    @param port: the port of the motor
    @type port: number
    """

    block_motor_done(port)

def is_motor_done(port):
    """
    @summary: determines if a motor is done moving to its position
    @param port: the port of the motor
    @type port: number
    @return: if the motor is done
    @rtype: bool
    """

    return w.get_motor_done(port)

def imd(port):
    """
    @summary: determines if a motor is done moving to its position
    @param port: the port of the motor
    @type port: number
    @return: if the motor is done
    @rtype: bool
    """

    return is_motor_done(port)

def clear_motor_position_counter(port):
    """
    @summary: sets the motor position counter to 0
    @param port: the port of the motor
    @type port: number
    """

    w.clear_motor_position_counter(port)

def freeze(port):
    """
    @summary: freezes a motor
    @param port: the port of the motor
    @type port: number
    """

    w.freeze(port)

def off(port):
    """
    @summary: turns off a motor
    @param port: the port of the motor
    @type port: number
    """

    w.off(port);

def get_motor_position_counter(port):
    """
    @summary: gets the position of a motor
    @param port: the port of the motor
    @type port: number
    @return: the value of the position counter
    @rtype: number
    """

    return w.get_motor_position_counter(port)

def get_m_pos(port):
    """
    @summary: gets the position of a motor
    @param port: the port of the motor
    @type port: number
    @return: the value of the position counter
    @rtype: number
    """

    return get_motor_position_counter(port)

def get_pid_gains(port):
    """
    @summary: gets the PID control values for a motor
    @param port: the port of the motor
    @type port: number
    @return: the PID conrol values
    @rtype: object in the format { 'p': 0, 'i': 0, 'd': 0, 'pd': 0, 'id': 0, 'dd': 0 }
    """
    
    p = c_int()
    i = c_int()
    d = c_int()
    pd = c_int()
    id = c_int()
    dd = c_int()

    w.get_pid_gains(port, byref(p), byref(i), byref(d), byref(pd), byref(id), byref(dd))
    
    retObj = {}
    retObj['p'] = p.value
    retObj['i'] = i.value
    retObj['d'] = d.value
    retObj['pd'] = pd.value
    retObj['id'] = id.value
    retObj['dd'] = dd.value
    return retObj

def set_pid_gains(port, p, i, d, pd, id, dd):
    """
    @summary: sets the PID control values for a motor
    @param port: the port of the motor
    @type port: number
    @param p: the p value
    @type p: number
    @param i: the i value
    @type i: number
    @param d: the d value
    @type d: number
    @param dp: the dp value
    @type dp: number
    @param id: the id value
    @type id: number
    @param dd: the dd value
    @type dd: number
    """

    w.set_pid_gains(port, p, i, d, pd, id, dd)

def move_at_velocity(port, velocity):
    """
    @summary: lets a motor move at a specified velocity using PID
    @param port: the port of the motor
    @type port: number
    @param velocity: the motor power between -1000 and 1000 ticks per second
    @type velocity: number
    """

    w.move_at_velocity(port, velocity)

def mav(port, velocity):
    """
    @summary: lets a motor move at a specified velocity using PID
    @param port: the port of the motor
    @type port: number
    @param velocity: the motor power between -1000 and 1000 ticks per second
    @type velocity: number
    """

    move_at_velocity(port, velocity)

def move(port, percent):
    """
    @summary: lets a motor move at a specified velocity
    @param port: the port of the motor
    @type port: number
    @param percent: the motor power in percent
    @type percent: number
    """

    w.motor(port, percent)

def move_relative_position(port, velocity, pos):
    """
    @summary: lets the motor move to a position relative to the current position
    @param port: the port of the motor
    @type port: number
    @param velocity: how fast to move in 0 to 1000 ticks per second
    @type velocity: number
    @param pos: the position to move to
    @type pos: number
    """

    w.move_relative_position(port, velocity, pos)

def mrp(port, velocity, pos):
    """
    @summary: lets the motor move to a position relative to the current position
    @param port: the port of the motor
    @type port: number
    @param velocity: how fast to move in 0 to 1000 ticks per second
    @type velocity: number
    @param pos: the position to move to
    @type pos: number
    """

    move_relative_position(port, velocity, pos)

def move_to_position(port, velocity, pos):
    """
    @summary: lets the motor move to an absolute position
    @param port: the port of the motor
    @type port: number
    @param velocity: how fast to move in 0 to 1000 ticks per second
    @type velocity: number
    @param pos: the position to move to
    @type pos: number
    """

    w.move_to_position(port, velocity, pos)

def mtp(port, velocity, pos):
    """
    @summary: lets the motor move to an absolute position
    @param port: the port of the motor
    @type port: number
    @param velocity: how fast to move in 0 to 1000 ticks per second
    @type velocity: number
    @param pos: the position to move to
    @type pos: number
    """

    move_to_position(port, velocity, pos)
