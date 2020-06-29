
RD_VERSION = 0x00
WRITE = 0x01
READ = 0x02

def getVersion(dev):
    dev.send([RD_VERSION])
    raw = dev.read(3)
    return raw[1] + raw[2] * 256

def write(dev, address, data):
    msg = [WRITE, address, data]
    dev.send(msg)
    raw = dev.read(1)
    return raw[0]

def read(dev, address):
    msg = [READ, address]
    dev.send(msg)
    raw = dev.read(2)
    return raw[1]

