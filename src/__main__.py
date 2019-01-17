#!/usr/bin/env python2
try:
    import __wallaby_local as __wallaby # for VSCode support
except ImportError: 
    import imp; __wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py') # so it works on actual robot

from motors import *
from create import create
from cameras import camera
from helpers import print_botball_logo

print_botball_logo()

# Test motors
'''
motor = motor(port=1, speed=1.0)
servo0 = servo(port=0, speed=0.95)

# motor.move(FORWARD, time=2) # this is a blocking method, so we don't have to worry about sleeping!
servo0.set_position(0.0)
servo0.set_position(1.0)
'''
# Test create
'''
create = create()
create.drive_forward(100)
# create.follow_line(1000)

servo0.set_position(0.0) # ALWAYS DO THIS at the end!

create().follow_line(1000)
'''
# Test cameras

with camera(color='green', debug=True) as camera:
    while True:
        if camera.is_current_object_trackable():
            camera.distance_to_current_object(obj_height_mm=48, should_update=False)
        
        print
