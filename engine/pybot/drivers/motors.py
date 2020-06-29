
RD_VERSION = 0x00
SET_VEL_2MTR = 0x01
SET_VEL_MTR = 0x02
TEST_MOTORS = 0x03
GET_TYPE = 0x04

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def setvel2mtr(dev, left_sense, left_vel, right_sense, right_vel):
    msg = [SET_VEL_2MTR, left_sense, left_vel / 256, left_vel % 256, right_sense, right_vel / 256, right_vel % 256]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

def setvelmtr(dev, motor_id, sense, vel):
    msg = [SET_VEL_MTR, motor_id, sentido, vel / 256, vel % 256]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

def testMotors(dev):
    dev.send([TEST_MOTORS])
    raw = dev.read(1)
    return raw[0]

def getType(dev):
    dev.send([GET_TYPE])
    raw = dev.read(2)
    return raw[1]

