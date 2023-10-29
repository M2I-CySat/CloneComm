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
    print("Starting descramble")
    global packetNum
    descrambled = [0] * len(arr)
    descrambledByte = 0
    lfsr = 0b00000000000000000000000000000000

    #start descrambling:
    for i in range(len(descrambled)):
        for j in range(8):
            curbit = (arr[i] >> (7-j)) & 1
            lfsr = ((lfsr << 1) | curbit)
            X12 = (lfsr >> 12) & 1
            X17 = (lfsr >> 17) & 1
            outbit = ((curbit) ^ ((X12 ^ X17))) & 1
            descrambledByte = (descrambledByte << 1) | outbit
            #descrambledByte = str(outbit) + descrambledByte
        descrambled[i] = descrambledByte
        descrambledByte = 0
    print("Done descrambling")

    #get which file extension type:
    match descrambled[1]:
        case 0x00:
            filename = ".DAT"
        case 0x01:
            filename = ".KEL"
        case 0x02:
            filename = ".LIS"
        case 0x03:
            filename = ".HCK"
        case 0x04:
            filename = ".TXT"
    print("Extension generated")

    filename = "file" + packetNum + filename
    print('Filename to create: {}'.format(filename))

    #create a file to be written byte-by-byte:
    print("Before file creation")
    f = open(filename, "wb+")
    print("After file creation")

    #write descrambled array into the newly created file:
    for i in range(len(descrambled)):
        f.write(descrambled[i])

    #close file:
    print("Closing file")
    f.close()
    packetNum += 1


##Function that opens two text files--one for reading and one for appending. Upon
##determining if text files exist, function will read a file byte by byte until it 
##reaches the end of a packet, descramble the bytes in the packet, and then 
##append the descrambled packets to a separate file.
def readTxt(array):
    
    #initializing:
    data = [0] * 129            #array to store bytes between each package

    #take data and store in an array:
    for i in range(len(array)):
        print(array[i])
        data[i] = array[i]

    #descramble data:
    descramble(data)