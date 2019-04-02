try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor 
from src.helpers.motors import servo
from src.helpers.create import create as _create

# Set up motor/servo

servo.SERVO_MIN_POSITION = 98

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
    
    arm_servo.set_position(0.15)
    guide_motor.move(motor.FORWARD, 1000)
    arm_servo.set_position(0.05)
    guide_motor.move(motor.BACKWARD, 1000)

    finish()
