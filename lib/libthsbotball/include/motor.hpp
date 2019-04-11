#ifndef _LIBTHSBOTBALL_MOTOR_H_
#define _LIBTHSBOTBALL_MOTOR_H_

class Motor {
public:
    int port;
    int speed;

    Motor(int port, int speed);

    void driveForwardForTime(long ms);

private:
    void _driveForTime(bool direction, long ms);
};

#endif
