import CSPP_generator as CSPP
import struct


def TakeMeasurement(duration, delay):
    return CSPP.makeCySatPacket("SDR","03",[["int",duration,2],["int",delay,2]], True, True, True)