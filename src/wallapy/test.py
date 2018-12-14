import time
import math


class Test:
    '''
    @author: Manuel Reinsperger
    @summary: this class can be used to test various create algorithms and has helped develop the drive and rotate algorithms
    '''
    rrot = 0
    lrot = 0
    ROTATION_RATIO = (242.5 * math.pi) / 360
    WHEEL_DIAMETER = 72
    WHEEL_TICKS_PER_REVOLUTION = 508.8

    def __init__(self):
        pass

    def reset(self):
        self.rrot = 0
        self.lrot = 0

    def test_drive(self, init, speed, dist):
        self.reset()
        self.drive_distance_wait(speed, dist)
        print self.rrot, self.lrot

    def test_rotate(self, speed, angle):
        self.reset()
        self.rotate_angle_wait(speed, angle)
        print self.rrot, self.lrot

    def drive_distance_wait(self, speed, dist):
        if speed < 0:
            speed = abs(speed)
            if dist > 0:
                dist = dist * -1

        timeout = max(abs(float(dist) / float(speed)) * 2.0, 2.0)
        dist = int(dist * (self.WHEEL_TICKS_PER_REVOLUTION / (self.WHEEL_DIAMETER * math.pi)))
        self.stream_sensors([44, 43], timeout, self.drive_callback, {"dist": dist, "speed": speed, "debug": True})
        self.stop_all()

    def rotate_angle_wait(self, speed, angle):
        if speed < 0:
            speed = abs(speed)
            if angle > 0:
                dist = angle * -1

        dist = self.ROTATION_RATIO * angle
        timeout = max(abs(float(dist) / float(speed)) * 4.0, 2.0)
        dist = int(dist * (self.WHEEL_TICKS_PER_REVOLUTION / (self.WHEEL_DIAMETER * math.pi)))
        self.stream_sensors([44], timeout, self.rotate_callback, {"dist": dist, "speed": speed, "debug": True})
        self.stop_all()

    def stream_sensors(self, sensors, timeout, callback, statics={}):
        self.send_command_ASCII('148 ' + str(len(sensors)) + ' ' + ' '.join([str(sv) for sv in sensors]))
        # Get new values
        full_timeout = time.time() + timeout

        while True:
            vlist = {44: self.rrot, 43: self.lrot}
            time.sleep(0.1)

            check = 0
            checksum = 0

            if ((check + checksum) & 0xFF) is 0:
                if callback(vlist, statics):
                    self.send_command_ASCII('150 0')
                    time.sleep(0.03)
                    # self.connection.flushInput()
                    print "exit good"
                    return 1

            if time.time() > full_timeout:
                self.send_command_ASCII('150 0')
                time.sleep(0.03)
                # self.connection.flushInput()
                print "exit time", time.time()
                return -1

        print "exit error"
        self.send_command_ASCII('150 0')
        time.sleep(0.03)
        # self.connection.flushInput()
        return -2

    def float_close(self, a, b, rel_tol=1e-5, abs_tol=0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def drive_direct(self, r, l):
        self.rrot = self.rrot + int(((r / 508.8) * (72 * math.pi))) % 65535
        self.lrot = self.lrot + int(((l / 508.8) * (72 * math.pi))) % 65535

    def stop_all(self):
        """
        @author: Manuel Reinsperger
        @summary: stop the create
        @aends: 145 0 0 0 0 stop both motors
        """
        self.send_command_ASCII('150 0')
        self.send_command_ASCII('145 0 0 0 0')

    def send_command_ASCII(self, te):
        pass

    def drive_callback(self, sensors, static):
        if "initRight" not in static:
            # Initialize values
            static["initRight"] = static["prevRight"] = sensors[44]
            static["initLeft"] = static["prevLeft"] = sensors[43]
            static["rightOvershoot"] = False
            static["leftOvershoot"] = False

        rightOvershoot = static["rightOvershoot"]
        prevRight = static["prevRight"]
        static["prevRight"] = sensors[44]
        leftOvershoot = static["leftOvershoot"]
        prevLeft = static["prevLeft"]
        static["prevLeft"] = sensors[43]

        if abs(abs(prevRight) - abs(static["prevRight"])) > 60000:
            static["initRight"] = static["initRight"] + (-65536 if prevRight > static["prevRight"] else 65536)

        if abs(abs(prevLeft) - abs(static["prevLeft"])) > 60000:
            static["initLeft"] = static["initLeft"] + (-65536 if prevLeft > static["prevLeft"] else 65536)

        initRight = static["initRight"]
        initLeft = static["initLeft"]

        curRight = sensors[44] - initRight
        curLeft = sensors[43] - initLeft
        dist = static["dist"]
        realspeed = static["speed"]
        speed = abs(realspeed)

        # Check if close enough to goal
        if self.float_close(abs(curRight), dist, abs_tol=max(speed / 250, 1)) and self.float_close(abs(curLeft), dist, abs_tol=max(speed / 50, 1)):
            self.stop_all()
            return 1

        # Set wheel speeds and directions
        # Slows down both directions if overshoots target
        if speed > 0 and dist > 0:
            if curRight < dist:
                inrMod = 1 if not rightOvershoot else 0.2
            else:
                inrMod = -0.2
                static["rightOvershoot"] = True
            if curLeft < dist:
                inlMod = 1 if not leftOvershoot else 0.2
            else:
                inlMod = -0.2
                static["leftOvershoot"] = True
        else:
            if curRight > dist:
                inrMod = -1 if not rightOvershoot else -0.2
            else:
                inrMod = 0.2
                static["rightOvershoot"] = True
            if curLeft > dist:
                inlMod = -1 if not leftOvershoot else -0.2
            else:
                inlMod = 0.2
                static["leftOvershoot"] = True

        # Apply the power curve which slows down when coming closer to the goal
        rMod = inrMod * (0.65 * min(pow(float(dist - curRight), 2.0) / pow(speed, 2), 1.0) + 0.35)
        lMod = inlMod * (0.65 * min(pow(float(dist - curLeft), 2.0) / pow(speed, 2), 1.0) + 0.35)

        rightspeed = round(realspeed * rMod)
        leftspeed = round(realspeed * lMod)

        if ("debug" in static) and static["debug"]:
            print "dist", dist, "initR", initRight, "initL", initLeft, "right", curRight, "left", curLeft, \
                  ("inrMod   " if curRight < dist else "inrMod") if speed > 0 and dist > 0 else ("inrMod  " if curRight > dist else "inrMod "), inrMod, \
                  ("inlMod   " if curLeft < dist else "inlMod") if speed > 0 and dist > 0 else ("inlMod  " if curLeft > dist else "inlMod "), inlMod, \
                  "lMod" if lMod < 0 else "lMod ", round(lMod, 1), "rMod" if rMod < 0 else "lMod ", \
                  round(rMod, 1), "rspeed" if rightspeed < 0 else "rspeed ", int(rightspeed), "lspeed" if leftspeed < 0 else "lspeed ", int(leftspeed)

        # Drive
        self.drive_direct(int(rightspeed), int(leftspeed))

    def rotate_callback(self, sensors, static):
        if "initRight" not in static:
            static["initRight"] = static["prevRight"] = sensors[44]
            static["rightOvershoot"] = False

        prevRight = static["prevRight"]
        static["prevRight"] = sensors[44]

        if abs(abs(prevRight) - abs(static["prevRight"])) > 60000:
            initRight = static["initRight"] = static["initRight"] + (-65536 if prevRight > static["prevRight"] else 65536)
        else:
            initRight = static["initRight"]

        rightOvershoot = static["rightOvershoot"]
        curRight = sensors[44] - initRight
        dist = static["dist"]
        realspeed = static["speed"]
        speed = abs(realspeed)

        # Check if close enough to goal
        if self.float_close(abs(curRight), abs(dist), abs_tol=max(speed / 250, 1)):
            self.stop_all()
            return 1

        # Set wheel speeds and directions
        # Slows down both directions if overshoots target
        if speed > 0 and dist > 0:
            if curRight < dist:
                inrMod = 1 if not rightOvershoot else 0.2
            else:
                inrMod = -0.2
                static["rightOvershoot"] = True
        else:
            if curRight > dist:
                inrMod = -1 if not rightOvershoot else -0.2
            else:
                inrMod = 0.2
                static["rightOvershoot"] = True

        # Apply the power curve which slows down when coming closer to the goal
        rMod = inrMod * (0.65 * min(pow(float(dist - curRight), 2.0) / pow(speed, 2), 1.0) + 0.35)

        rotatespeed = round(realspeed * rMod)

        if ("debug" in static) and static["debug"]:
            print "dist", dist, "initR", initRight, "right", curRight, "rMod" if rMod < 0 else "lMod ", \
                  round(rMod, 1), "rspeed" if rotatespeed < 0 else "rspeed ", int(rotatespeed)

        # Drive
        self.drive_direct(int(rotatespeed), -int(rotatespeed))
