#   Created on: Oct 3, 2023
#       Last Updated: Oct 29, 2023
#       Author: Em Bradley-DeHaan


import random


packetNum = 0

##Imported from "composer.py":
##
#Slightly modified to properly read the incoming data
##
##Takes the measurement ID bytes from the header of the data array
def takeFirst(elem):
    mID = [0] * 4
    for i in range(4):
        mID[i] = str(elem[i + 4]).zfill(2)
    Measurment_ID_hex = "".join([str(i) for i in mID])
    string = "Measurment ID: " + Measurment_ID_hex
    print(string)
    return Measurment_ID_hex


##Imported from "composer.py":
##
##Slightly modified to properly read the incoming data
##
##Takes the packet number bytes from the header of the data array
def takeSecond(elem):
    pID = [0] * 4
    for i in range(4):
        pID[i] = str(elem[i + 7]).zfill(2)
    Packet_ID_hex = "".join([str(i) for i in pID])
    string = "Packet Number: " + Packet_ID_hex
    print(string)
    return Packet_ID_hex


##Function that takes an array of scrambled bytes, descrambles them with a
##X^17 + X^12 + 1 polynomial multiplicative scrambler, and returns the
##data to be read from the descrambled byte array
##
##This doesn't completely discard header information, but stores it in a
##separate byte array to check for how many bytes to read (making sure it's
##not 0) and the packet number. If the current packet number is not
##the next expected packet, a string is returned
def descramble(arr):
    #print("Starting descramble")
    global packetNum
    descrambled = [0] * len(arr)
    descrambledByte = 0
    lfsr = 0b00000000000000000000000000000000
    arr = bytearray(arr)
    #start descrambling:
    for i in range(len(descrambled)):
        for j in range(8):
            curbit = (arr[i] >> (7-j)) & 1
            lfsr = ((lfsr << 1) | curbit)
            X12 = (lfsr >> 12) & 1
            X17 = (lfsr >> 17) & 1
            outbit = ((curbit) ^ ((X12 ^ X17))) & 1
            descrambledByte = (descrambledByte << 1) | outbit
        descrambled[i] = descrambledByte
        #print("Byte "+str(i)+" Int "+str(int(descrambledByte))+" Str "+str(descrambledByte))
        descrambledByte = 0
    #print("Done descrambling")
    descrambled = bytearray(descrambled)

    return descrambled


##This function fills in a file with 0xAA bytes if a packet is detected to be missing.
def fillData(bytes):
    data = [0] * 126
    data[0:12] = bytes
    data[13:125] = {0xAA}

    return data