try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

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
        w.create_connect()
        
    def turn_right(self, angle):
        """Turns the Create right at the angle specified.
        
        Arguments:
            angle {int} -- The angle to turn.
        """

        # self.internal_create.rotate_angle_wait(speed=self.speed, angle=-angle)
        # w.create_spin_CW() # TODO: FINISH

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

        # TODO: FINISH
        # self.internal_create.drive_distance_wait(speed=self.speed, dist=distance)

    def drive_backward(self, distance):
        """Drives the Create backward for the specified distance.
        
        Arguments:
            distance {int} -- The distance in mm.
        """
        self.drive_forward(-distance)
