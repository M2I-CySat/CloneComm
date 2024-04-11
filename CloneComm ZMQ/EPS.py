import CSPP_generator as CSPP
import struct


def PackRequest():
    return CSPP.makeCySatPacket("EPS","15",[], True, True, True)

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
    return CSPP.makeCySatPacket("EPS","17",[], True, True, True)

def CounterRequest():
    return CSPP.makeCySatPacket("EPS","0F",[], True, True, True)

def PowerRequestHex(str):
    print("PowerRequestHex")
    print(str)
    match str:
        case "Battery Bus":
            return "01"
        # case "5v Bus":
        #     return "04"
        case "Battery Charge 1":
            return "06"
        case "Battery Charge 2":
            return "07"
        case "Boost Board":
            return "08"
        case "Out2":
            return "09"
        case "Out3":
            return "0A"
        # case "UHF":
        #     return "0B"
        case "Out6":
            return "0C"
        case "Heater 1":
            return "0D"
        case "Heater 2":
            return "0E"
        case "Heater 3":
            return "0F"

def ChangePower(inval):
    inval2 = PowerRequestHex(inval)
    print("Attempting to switch power")
    print(inval)
    return CSPP.makeCySatPacket("EPS","11",[["hex",inval2,1]], True, True, True)