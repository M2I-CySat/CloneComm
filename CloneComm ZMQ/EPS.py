import CSPP_generator as CSPP
import struct


def PackRequest():
    return CSPP.makeCySatPacket("EPS","01",[], True, True, True)

def XRequest():
    return CSPP.makeCySatPacket("EPS","03",[], True, True, True)

def YRequest():
    return CSPP.makeCySatPacket("EPS","05",[], True, True, True)

def ZRequest():
    return CSPP.makeCySatPacket("EPS","07",[], True, True, True)

def BusRequest():
    return CSPP.makeCySatPacket("EPS","09",[], True, True, True)

def TempRequest():
    return CSPP.makeCySatPacket("EPS","0B",[], True, True, True)

def IORequest():
    return CSPP.makeCySatPacket("EPS","0D",[], True, True, True)

def CounterRequest():
    return CSPP.makeCySatPacket("EPS","0F",[], True, True, True)

def PackRequest():
    return CSPP.makeCySatPacket("EPS","01",[], True, True, True)