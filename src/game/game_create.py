try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo
from src.helpers.create import create as _create

# Set up motor/servo

guide_motor = motor.motor(port=0, speed=1.0)
arm_servo = servo.servo(port=3, speed=1.0)

# Set up Create 

create = _create.create(speed=150)

def reset():
    print '**** Resetting ****'

    arm_servo.set_position(0.5)

    print '**** Resetting done ****'

def finish():
    print '**** Finishing ****'

    arm_servo.set_position(0.5)

    print '**** Done finishing ****'

def run():
    print '**** Running game ****'

    reset()

    create.drive_forward(150)

    finish()
