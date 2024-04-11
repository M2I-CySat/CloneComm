import CSPP_generator as CSPP
import struct


def TakeMeasurement(duration, delay, tesfile):
    return CSPP.makeCySatPacket("SDR","03",[["int",duration,2],["int",delay,2],["int",tesfile,1]], True, True, True)