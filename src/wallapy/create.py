'''
initial c library by Alexander Halbart
all methods ported to python by Manuel Reinsperger
modifications by Lukas Rysavy
'''
# from util import register_create
import serial
import time
import math


def connect():
    """
    @author: Lukas Rysavy
    @summary: creates a new Create object
    @return: the Create object
    @rtype: Create
    """
    cr = Create("/dev/ttyUSB0")
    if cr.connection is None:
        print "Connection failed"
        return -1
    return cr


class Create:
    WHEEL_DIAMETER = 72
    WHEEL_TICKS_PER_REVOLUTION = 508.8
    # sensor packet IDs
    SENSOR_BUMPWHEEL = 7
    SENSOR_WALL = 8
    SENSOR_CLIFF_LEFT = 9
    SENSOR_CLIFF_LEFT_FRONT = 10
    SENSOR_CLIFF_RIGHT_FRONT = 11
    SENSOR_CLIFF_RIGHT = 12
    SENSOR_VIRTUAL_WALL = 13
    SENSOR_OVERCURRENTS = 14
    SENSOR_DIRT_DETECT = 15
    SENSOR_IR_OPCODE = 17
    SENSOR_BUTTONS = 18
    SENSOR_DISTANCE = 19
    SENSOR_ANGLE = 20
    SENSOR_CHARGING_STATE = 21
    SENSOR_VOLTAGE = 22
    SENSOR_CURRENT = 23
    SENSOR_BATTERY_TEMPERATURE = 24
    SENSOR_BATTERY_CHARGE = 25
    SENSOR_BATTERY_CAPACITY = 26
    SENSOR_WALL_SIGNAL = 27
    SENSOR_CLIFF_LEFT_SIGNAL = 28
    SENSOR_CLIFF_LEFT_FRONT_SIGNAL = 29
    SENSOR_CLIFF_RIGHT_FRONT_SIGNAL = 30
    SENSOR_CLIFF_RIGHT_SIGNAL = 31
    SENSOR_CHARGING_SOURCES_AVAILABLE = 34
    SENSOR_OI_MODE = 35
    SENSOR_SONG_NUMBER = 36
    SENSOR_SONG_PLAYING = 37
    SENSOR_NUMBER_OF_STREAM_PACKETS = 38
    SENSOR_VELOCITY = 39
    SENSOR_RADIUS = 40
    SENSOR_VELOCITY_RIGHT = 41
    SENSOR_VELOCITY_LEFT = 42
    SENSOR_ENCODER_COUNTS_LEFT = 43
    SENSOR_ENCODER_COUNTS_RIGHT = 44
    SENSOR_LIGHT_BUMPER = 45
    SENSOR_LIGHT_BUMPER_LEFT = 46
    SENSOR_LIGHT_BUMPER_FRONT_LEFT = 47
    SENSOR_LIGHT_BUMPER_CENTER_LEFT = 48
    SENSOR_LIGHT_BUMPER_CENTER_RIGHT = 49
    SENSOR_LIGHT_BUMPER_FRONT_RIGHT = 50
    SENSOR_LIGHT_BUMPER_RIGHT = 51
    SENSOR_IR_OPCODE_LEFT = 52
    SENSOR_IR_OPCODE_RIGHT = 53
    SENSOR_LEFT_MOTOR_CURRENT = 54
    SENSOR_RIGHT_MOTOR_CURRENT = 55
    SENSOR_MAIN_BRUSH_CURRENT = 56
    SENSOR_SIDE_BRUSH_CURRENT = 57
    SENSOR_STASIS = 58

    SENSOR_SIZE_LIST = '0000001111111111112212212222222121111122222212222221122221'

    ROTATION_RATIO = (242.5 * math.pi) / 360

    connection = None

    def __init__(self, port):
        """
        @author: Manuel Reinsperger
        @summary: connect to Create
        @Sends: 128 Start
                132 Enable full mode
        """
        try:
            self.connection = serial.Serial(port, baudrate=115200, timeout=1)
            self.send_command_ASCII('128')
            self.send_command_ASCII('132')
            # register_create(self)
        except:
            self.connection = None

    def reconnect(self):
        """
        @author: Manuel Reinsperger
        @summary: closes and opens the serial connection and sets full mode
        @sends: 128 132 set full mode
        """
        self.connection.close()
        self.connection.open()
        self.send_command_ASCII('128')
        self.send_command_ASCII('132')

    def reset(self):
        """
        @author: Manuel Reinsperger
        @summary: sends the reset command to the create
        @sends: 7 reset create
        """
        self.send_command_ASCII('7')

    def send_command_ASCII(self, command):
        """
        @author: Manuel Reinsperger
        @summary: take an ASCII string, split it by whitespace and send it via sendCommandRaw
        @args: command (string): command to send
        """
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.send_command_raw(cmd)

    def send_command_raw(self, command):
        """
        @author: Manuel Reinsperger
        @summary: take string interpreted as a byte array and sends it to create
        @args: command (char): command to send
        @return: 1 success, -1 not connected, -2 connection lost
        @rtype: int
        """
        try:
            if self.connection is not None:
                self.connection.write(command)
                return 1
            else:
                return -1
        except serial.SerialException:
            self.connection = None
            return -2

    def stop_all(self):
        """
        @author: Manuel Reinsperger
        @summary: stop the create and close all streams
        @sends: 145 0 0 0 0 stop both motors
        """
        self.send_command_ASCII('150 0')
        self.send_command_ASCII('145 0 0 0 0')

    def float_close(self, a, b, rel_tol=1e-5, abs_tol=0):
        """
        @author: Manuel Reinsperger
        @summary: compares two numbers with a certain allowed margin
        @return: True if close, False if not
        """
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def rotate_callback(self, sensors, static):
        """
        @author: Manuel Reinsperger
        @summary: this is an internal method for use in rotate_angle_wait via poll_sensors and contains the self correcting algorithm
        @return: has reached desired angle (0: no, 1: yes)
        @rtype: int
        """
        if "initRight" not in static:
            # Initialize static variables
            static["initRight"] = static["prevRight"] = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT]
            static["rightOvershoot"] = False

        # Load the last sensor value and set the current to last
        prevRight = static["prevRight"]
        static["prevRight"] = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT]

        # Correct sensor value over- and underflows
        if abs(abs(prevRight) - abs(static["prevRight"])) > 60000:
            # If value jump has been detected correct the initial value for consistency
            static["initRight"] = static["initRight"] + (-65536 if prevRight > static["prevRight"] else 65536)

        # Load old or changed initial value
        initRight = static["initRight"]

        # Load overshoot from previous cycles
        rightOvershoot = static["rightOvershoot"]

        # Calculate the current relative value
        curRight = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT] - initRight

        # Load other static values
        dist = static["dist"]
        realspeed = static["speed"]
        speed = abs(realspeed)

        # Check if close enough to goal to stop
        if self.float_close(abs(curRight), abs(dist), abs_tol=max(speed / 250, 1)):
            # If so stop all motors and tell poll_sensors to terminate
            self.stop_all()
            return 1

        # Set wheel speeds and directions
        # Slows down both directions if overshoots target
        if speed > 0 and dist > 0:
            # Create needs to rotate counter-clockwise
            if curRight < dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inrMod = 1 if not rightOvershoot else 0.2
            else:
                # Create has overshot the angle
                inrMod = -0.2
                # Mark it for further cycles
                static["rightOvershoot"] = True
        else:
            # Create needs to rotate clockwise
            if curRight > dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inrMod = -1 if not rightOvershoot else -0.2
            else:
                # Create has overshot the angle
                inrMod = 0.2
                # Mark it for further cycles
                static["rightOvershoot"] = True

        # Apply the power curve which slows down when coming closer to the goal
        rMod = inrMod * (0.65 * min(pow(float(dist - curRight), 2.0) / pow(speed, 2), 1.0) + 0.35)

        # Calculate the final speed from original speed and modifiers
        rotatespeed = round(realspeed * rMod)

        # Debug logs if debug flag is set
        if ("debug" in static) and static["debug"]:
            print "dist", dist, "initR", initRight, "right", curRight, "rMod" if rMod < 0 else "lMod ", \
                  round(rMod, 1), "rspeed" if rotatespeed < 0 else "rspeed ", int(rotatespeed)

        # Drive
        self.drive_direct(int(rotatespeed), -int(rotatespeed))

    def drive_callback(self, sensors, static):
        """
        @author: Manuel Reinsperger
        @summary: this is an internal method for use in drive_distance_wait via poll_sensors and contains the self correcting algorithm
        @return: has reached desired distance (0: no, 1: yes)
        @rtype: int
        """
        if "initRight" not in static:
            # Initialize static variables
            print sensors
            static["initRight"] = static["prevRight"] = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT]
            static["initLeft"] = static["prevLeft"] = sensors[self.SENSOR_ENCODER_COUNTS_LEFT]
            static["rightOvershoot"] = False
            static["leftOvershoot"] = False

        # Load the last sensor value and set the current to last
        prevRight = static["prevRight"]
        static["prevRight"] = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT]
        prevLeft = static["prevLeft"]
        static["prevLeft"] = sensors[self.SENSOR_ENCODER_COUNTS_LEFT]

        # Correct sensor value over- and underflows for right wheel
        if abs(abs(prevRight) - abs(static["prevRight"])) > 60000:
            # If value jump has been detected correct the initial value for consistency
            static["initRight"] = static["initRight"] + (-65536 if prevRight > static["prevRight"] else 65536)
        # Correct sensor value over- and underflows for left wheel
        if abs(abs(prevLeft) - abs(static["prevLeft"])) > 60000:
            # If value jump has been detected correct the initial value for consistency
            static["initLeft"] = static["initLeft"] + (-65536 if prevLeft > static["prevLeft"] else 65536)

        # Load old or changed initial value
        initRight = static["initRight"]
        initLeft = static["initLeft"]

        # Load overshoot from previous cycles
        rightOvershoot = static["rightOvershoot"]
        leftOvershoot = static["leftOvershoot"]

        # Calculate the current relative values
        curRight = sensors[self.SENSOR_ENCODER_COUNTS_RIGHT] - initRight
        curLeft = sensors[self.SENSOR_ENCODER_COUNTS_LEFT] - initLeft

        # Load other static values
        dist = static["dist"]
        realspeed = static["speed"]
        speed = abs(realspeed)

        # Check if close enough to goal to stop
        if self.float_close(abs(curRight), dist, abs_tol=max(speed / 250, 1)) and self.float_close(abs(curLeft), dist, abs_tol=max(speed / 50, 1)):
            # If so stop all motors and tell poll_sensors to terminate
            self.stop_all()
            return 1

        # Set wheel speeds and directions
        # Slows down both directions if overshoots target
        if speed > 0 and dist > 0:
            # Create needs to drive forward
            if curRight < dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inrMod = 1 if not rightOvershoot else 0.2
            else:
                # Create has overshot the angle
                inrMod = -0.2
                # Mark it for further cycles
                static["rightOvershoot"] = True
            if curLeft < dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inlMod = 1 if not leftOvershoot else 0.2
            else:
                # Create has overshot the angle
                inlMod = -0.2
                # Mark it for further cycles
                static["leftOvershoot"] = True
        else:
            if curRight > dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inrMod = -1 if not rightOvershoot else -0.2
            else:
                # Create has overshot the angle
                inrMod = 0.2
                # Mark it for further cycles
                static["rightOvershoot"] = True
            if curLeft > dist:
                # Create has not yet reached the angle
                # Uses a smaller multiplier if it has already overshot the angle once
                inlMod = -1 if not leftOvershoot else -0.2
            else:
                # Create has overshot the angle
                inlMod = 0.2
                # Mark it for further cycles
                static["leftOvershoot"] = True

        # Apply the power curve which slows down when coming closer to the goal
        rMod = inrMod * (0.65 * min(pow(float(dist - curRight), 2.0) / pow(speed, 2), 1.0) + 0.35)
        lMod = inlMod * (0.65 * min(pow(float(dist - curLeft), 2.0) / pow(speed, 2), 1.0) + 0.35)

        # Calculate the final speed from original speed and modifiers
        rightspeed = round(realspeed * rMod)
        leftspeed = round(realspeed * lMod)

        # Debug logs if debug flag is set
        if ("debug" in static) and static["debug"]:
            print "dist", dist, "initR", initRight, "initL", initLeft, "right", curRight, "left", curLeft, \
                  ("inrMod   " if curRight < dist else "inrMod") if speed > 0 and dist > 0 else ("inrMod  " if curRight > dist else "inrMod "), inrMod, \
                  ("inlMod   " if curLeft < dist else "inlMod") if speed > 0 and dist > 0 else ("inlMod  " if curLeft > dist else "inlMod "), inlMod, \
                  "lMod" if lMod < 0 else "lMod ", round(lMod, 1), "rMod" if rMod < 0 else "lMod ", \
                  round(rMod, 1), "rspeed" if rightspeed < 0 else "rspeed ", int(rightspeed), "lspeed" if leftspeed < 0 else "lspeed ", int(leftspeed)

        # Drive
        self.drive_direct(int(rightspeed), int(leftspeed))

    def drive_bump_callback(self, sensors, static):
        if ("debug" in static) and static["debug"]:
            print sensors
        if sensors[self.SENSOR_BUMPWHEEL] > 0:
            self.stop_all()
            return 1
        else:
            self.drive_direct(int(static["speed"]), int(static["speed"]))
            return 0

    def drive_until_bump(self, speed, timeout=5, debug=False):
        """
        @author: Manuel Reinsperger
        @summary: drives for [dist] mm
        @args: speed (int): average speed in mm/s
                dist (int): distance in mm
        @caveats: if one of the parameters is negative it will drive backwards
                  if incorrectly terminated can leave an open sensor stream from the create
                  employs a timeout
        """
        # Initialize sensor stream
        self.stream_sensors([self.SENSOR_BUMPWHEEL], timeout, self.drive_bump_callback, {"speed": speed, "debug": debug})
        # Stop all create movement after completion
        self.stop_all()

    def drive_distance_wait(self, speed, dist, timeout=None, debug=False):
        """
        @author: Manuel Reinsperger
        @summary: drives for [dist] mm
        @args: speed (int): average speed in mm/s
                dist (int): distance in mm
        @caveats: if one of the parameters is negative it will drive backwards
                  if incorrectly terminated can leave an open sensor stream from the create
                  employs a timeout
        """
        # Correct negative values for use with algorithm
        if speed < 0:
            speed = abs(speed)
            if dist > 0:
                dist = dist * -1
        # Calculate timeout if none is given
        if timeout is None:
            timeout = max(abs(float(dist) / float(speed)) * 3.0, 2.0)
        # Get distance from mm to ticks
        dist = int(dist * (self.WHEEL_TICKS_PER_REVOLUTION / (self.WHEEL_DIAMETER * math.pi)))
        # Initialize sensor stream
        self.stream_sensors([self.SENSOR_ENCODER_COUNTS_RIGHT, self.SENSOR_ENCODER_COUNTS_LEFT], timeout, self.drive_callback, {"dist": dist, "speed": speed, "debug": debug})
        # Stop all create movement after completion
        self.stop_all()

    def rotate_angle_wait(self, speed, angle, timeout=None, debug=False):
        """
        @author: Manuel Reinsperger
        @summary: rotates clockwise for [angle] degrees
        @args: speed (int): average speed in mm/s
                dist (int): distance in mm
        @caveats: if one parameter is negative the create will rotate clockwise
                  if incorrectly terminated can leave an open sensor stream from the create
                  employs a timeout
        """
        # Correct negative values for use with algorithm
        if speed < 0:
            speed = abs(speed)
            if angle > 0:
                dist = angle * -1
        # Convert angle to driving distance
        dist = self.ROTATION_RATIO * angle
        # Calculate timeout if none is given
        if timeout is None:
            timeout = max(abs(float(dist) / float(speed)) * 3.0, 2.0)
        # Get distance from mm to ticks
        dist = int(dist * (self.WHEEL_TICKS_PER_REVOLUTION / (self.WHEEL_DIAMETER * math.pi)))
        # Initialize sensor stream
        self.stream_sensors([self.SENSOR_ENCODER_COUNTS_RIGHT], timeout, self.rotate_callback, {"dist": dist, "speed": speed, "debug": debug})
        # Stop all create movement after completion
        self.stop_all()

    def poll_sensor(self, sensor):
        """
        @author: Manuel Reinsperger
        @summary: poll create for single sensor value
        @args: sensor (int): number of sensor, see documentation or sensor statics for more
        @return: sensor value or None on error
        @rtype: int
        """
        if 6 < sensor < len(self.SENSOR_SIZE_LIST):         # Work on basic sensors, not groups
            # Send sensor query
            self.send_command_ASCII('142 ' + str(sensor))
            # Initialize result to 0
            valu = 0
            # Read results
            for i in range(ord(self.SENSOR_SIZE_LIST[sensor - 1]) - ord('0')):
                # Bitshift new values into result
                valu = (valu << 8) | ord(self.connection.read(1))

            return valu
        else:
            # On error return None
            return None

    def poll_sensors(self, *arg):
        """
        @author: Manuel Reinsperger
        @summary: poll create for multiple sensor values
        @args: *arg (int): polled sensors, see documentation or sensor statics for more
        @return: sensor value or None on error
        @rtype: int
        """
        if len(arg) is 0:
            # If no sensors are given return None
            return

        # Initialize data stores
        sent_command = ""
        sensor_list = []
        return_list = []

        # Construct sensor query
        for sensor in arg:
            if 6 > sensor > len(self.SENSOR_SIZE_LIST):
                # If a requested sensor is on in the valid list return none
                print "Sensor " + str(sensor) + " is not available!"
                return None
            else:
                # Append sensor to command
                sent_command += " " + str(sensor)
                # Add sensor return byte length
                sensor_list.append(ord(self.SENSOR_SIZE_LIST[sensor - 1]) - ord('0'))

        # Send sensor query list
        self.send_command_ASCII("149 " + str(len(sensor_list)) + sent_command)

        # Read results
        for sensor in sensor_list:
            # Initialize current value to 0
            valu = 0
            # Read return byte length bytes
            for i in range(sensor):
                # Bitshift new values into result
                valu = (valu << 8) | ord(self.connection.read(1))
            # Add result to return list
            return_list.append(valu)

        return return_list

    def stream_sensors(self, sensors, timeout, callback, statics={}):
        """
        @author: Manuel Reinsperger
        @summary: set up a sensor stream for [sensors] from the create and call [callback] at each full packet
        @args: sensors (int array): polled sensors, see documentation or sensor statics for more
                     timeout (int): maximum time this process is allowed to take
               callback (function): callback function, has to take two parameters (sensor_values, static_values)
              statics (dictionary): "static" shared storage that is passed to each [callback] call
        @return: success
        @rtype: Boolean
        """
        # Set up stream for sensors
        self.send_command_ASCII('148 ' + str(len(sensors)) + ' ' + ' '.join([str(sv) for sv in sensors]))
        # Calculate max time this process is allowed to take
        full_timeout = time.time() + timeout

        while True:
            # Empty out temporary variables
            vlist = {}
            check = 0
            pid = -1
            remaining_bytes = -1

            # Read until finding packet header of [19]
            read = ord(self.connection.read(1))
            if read is not 19:
                print "Miss: ", read
                continue
            check = check + read

            # Read the expected number of bytes
            nobytes = ord(self.connection.read(1))
            check = check + nobytes

            # Read all expected bytes
            for byte in range(0, nobytes):
                if remaining_bytes <= 0:
                    # If no bytes are remaining for the current sensor read the next sensor label
                    read = ord(self.connection.read(1))
                    check = check + read
                    # Set current sensors id
                    pid = read
                    # Set remaining bytes to the size from SENSOR_SIZE_LIST
                    remaining_bytes = ord(self.SENSOR_SIZE_LIST[pid - 1]) - ord('0')
                elif remaining_bytes > 0:
                    # If there are more bytes for the current sensor load them into the value
                    read = ord(self.connection.read(1))
                    check = check + read
                    if pid in vlist:
                        # If the sensor is already in the value list byteshift the new value in
                        vlist[pid] = (vlist[pid] << 8) | read
                    else:
                        # If the sensor is not in the value list initialize it with the read value
                        vlist[pid] = read
                    remaining_bytes = remaining_bytes - 1

            # Read the checksum
            checksum = ord(self.connection.read(1))

            # Calculate and check checksum
            if ((check + checksum) & 0xFF) is 0:
                # If check succeeded call the callback function with the received values
                if callback(vlist, statics):
                    # If callback signals success close the stream, flush the input and exit
                    self.send_command_ASCII('150 0')
                    time.sleep(0.03)
                    self.connection.flushInput()
                    print "exit good"
                    return True
            else:
                print "Checksum failure!"

            if time.time() > full_timeout:
                # If a timeout occurred close the stream, flush the input and exit with an error
                self.send_command_ASCII('150 0')
                time.sleep(0.03)
                self.connection.flushInput()
                print "exit time", time.time()
                return False

        # This is unreachable, but still considered due to the many magics of computer errors
        print "exit error"
        self.send_command_ASCII('150 0')
        time.sleep(0.03)
        self.connection.flushInput()

    def get_distance(self):
        """
        @author: Manuel Reinsperger
        @summary: returns the traveled mm as calculated from encoder counter-clockwise
        @caveats: when the wheels have been forcefully moved this can be incorrrect
        @returns: distance in mm
        @rtype: [int, int]
        """
        right, left = self.poll_sensors(self.SENSOR_ENCODER_COUNTS_RIGHT, self.SENSOR_ENCODER_COUNTS_LEFT)
        return [((right / 508.8) * (72 * math.pi)), ((left / 508.8) * (72 * math.pi))]

    def set_mode(self, mode):
        """
        @author: Bahnuel Reinsperger
        @summary: sets mode to safe or full
        @args: mode (int): mode type, 0 for safe, 1 for full
        """
        self.send_command_ASCII(chr(131 + int(mode)))

    def drive_direct(self, rightmotor, leftmotor):
        """
        @author: Manuel Reinsperger
        @summary: start driving with motor speeds
        @args: speed (int): speed in mm/s
        @sends: 145   Drive Direct command
                rightmotor >> 8 Speed right high byte (bits 8-15)
                rightmotor      Speed right low byte (bits 0-7)
                leftmotor >> 8  Speed left high byte (bits 8-15)
                leftmotor       Speed left low byte (bits 0-7)
        """
        rightspeedlow = (rightmotor & 0x00FF)
        rightspeedhigh = (rightmotor & 0xFF00) >> 8
        leftspeedlow = (leftmotor & 0x00FF)
        leftspeedhigh = ((leftmotor & 0xFF00) >> 8)
        self.send_command_ASCII('145 %s %s %s %s' %
                                (rightspeedhigh, rightspeedlow, leftspeedhigh, leftspeedlow))

    def drive_circle(self, speed, radius):
        """
        @author: Manuel Reinsperger
        @summary: start driving a circle with [radius] and [speed]
        @args: speed (int): mm/s
              radius (int): mm
        @sends: 137   Drive Direct command
                speed >> 8  Speed right high byte (bits 8-15)
                speed       Speed right low byte (bits 0-7)
                radius >> 8 Speed left high byte (bits 8-15)
                radius      Speed left low byte (bits 0-7)
        """
        speedlow = str(speed & 0xFF)
        speedhigh = str((speed & 0xFF00) >> 8)
        radiuslow = str(radius & 0xFF)
        radiushigh = str((radius & 0xFF00) >> 8)
        self.send_command_ASCII('137 %s %s %s %s' %
                                (speedhigh, speedlow, radiushigh, radiuslow))
