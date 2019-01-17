try:
    from __wallaby_local import * # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    from wallaby import * # so it works on actual robot

from helpers import msleep

WHITE_INFARED_L = 2100
BLACK_INFARED_L = 1100
WHITE_INFARED_R = 2700
BLACK_INFARED_R = 2200

SERVO_MIN_POSITION = 850
SERVO_MAX_POSITION = 1650

ROBOT_SPEED = 150
SPIN_SPEED = ROBOT_SPEED / 4

class create:
    """Represents an iRobot Create.
    """

    
    def __init__(self, speed=150):
        """Initializes a Create with the specified parameters.

        Arguments:
            speed {int} -- The speed of the Create in mm/s.
        """


        self.speed = speed
        create_connect()
        
    def turn_right(self, angle):
        """Turns the Create right at the angle specified.
        
        Arguments:
            angle {int} -- The angle to turn.
        """

        self.internal_create.rotate_angle_wait(speed=self.speed, angle=-angle)
        create_spin_CW()

    def turn_left(self, angle):
        """Turns the Create left at the angle specified.
        
        Arguments:
            angle {int} -- The angle to turn.
        """

        self.turn_right(-angle)

    def drive_forward(self, distance):
        """Drives the Create forward for the specified distance.
        
        Arguments:
            distance {int} -- The distance in mm.
        """

        self.internal_create.drive_distance_wait(speed=self.speed, dist=distance)

    def drive_backward(self, distance):
        """Drives the Create backward for the specified distance.
        
        Arguments:
            distance {int} -- The distance in mm.
        """
        self.drive_forward(-distance)

    def follow_line(self, distance):
        print "follow_line", distance
        
        current_distance = 0

        while current_distance < distance:
            cliff_left = w.get_create_lfcliff_amt()
            cliff_right = w.get_create_rfcliff_amt()

            if cliff_left < WHITE_INFARED_L:
                print "TURN RIGHT"
                self.turn_right(10)
            elif cliff_right < WHITE_INFARED_R:
                print "TURN LEFT"
                self.turn_left(10)
            
            self.drive_forward(10)

            # msleep(100)
        
            current_distance += 10

        w.create_stop()