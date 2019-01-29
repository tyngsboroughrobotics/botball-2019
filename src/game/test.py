try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from src.helpers.motors import motor
from src.helpers.motors.servo import servo
from src.helpers.create.create import create as _create
from src.helpers.cameras.camera import camera as _camera

# Test motors

def test_motors():
    motor0 = motor.motor(port=0, speed=1.0)
    motor0.move(motor.FORWARD, distance=2, block=True)

def test_servos():
    servo0 = servo(port=0, speed=0.95)
    servo0.set_position(0.0)
    servo0.set_position(1.0)
    servo0.set_position(0.0)

def test_create():
    create = _create()
    create.drive_forward(100)

def test_cameras():
    with _camera(color='green', debug=True) as camera:
        while True:
            if camera.is_current_object_trackable():
                camera.distance_to_current_object(obj_height_mm=48, should_update=False)
            
            print
