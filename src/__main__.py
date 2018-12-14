#!/usr/bin/env python2

import wallapy
from motors import *
from helpers import print_botball_logo

print_botball_logo()

# Test motors

motor = motor(port=1, speed=1.0)
servo = servo(port=2, speed=0.7)

motor.move(FORWARD, time=2) # this is a blocking method, so we don't have to worry about sleeping!
servo.set_position(0.8)
