#   Created on: 
#       Last Updated: Oct 3, 2023
#       Author: Em Bradley-DeHaan


import random


packetNum = 0                       #variable for checking packet number
readFile = "C:\\Users\\emmie\\Downloads\\packets927.txt"        #file to be read from, subject to change
writeFile = "C:\\Users\\emmie\\OneDrive\\Desktop\\new.txt"      #file to be written to, subject to change


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


    #CODE FOR CHECKING PACKET NUMBER : CURRENTLY DOES NOT FUNCTION PROPERLY

    # #receive and print measurement ID and packet number bytes:
    # takeFirst(descrambled)
    # curPacket = int.from_bytes(bytes.fromhex(takeSecond(descrambled)), byteorder="little")
    
    # #check for packet number:
    # for i in range(curPacket):
    #     #current packet number:
    #     curPacket[i] = descrambled[i + 8]

    # #check for missing packets:
    # if packetNum < curPacket:
    #     errorStr = "Missing Packet #" + str(packetNum)
    #     print(errorStr)
    #     packetNum = curPacket
    # #increment packetNum global variable:
    # packetNum += 1


    #don't input any unecessary packet information:
    if descrambled[13] == 0:
        return None
    
    data = [0] * 113
    for i in range(len(data)):
        data[i] = descrambled[i + 13]

    return data


##Function that opens two text files--one for reading and one for appending. Upon
##determining if text files exist, function will read a file byte by byte until it 
##reaches the end of a packet, descramble the bytes in the packet, and then 
##append the descrambled packets to a separate file.
def readTxt():
    f = open(readFile, "rb")
    fa = open(writeFile, "wb")
    
    #either file does not exist or could not be found:
    if f == None or fa == None:
        f.close()
        fa.close()
        return
    
    #initializing:
    c = f.read(1)
    c1 = hex(ord(c))                    #current byte being read
    prevByte = 0x00                     #previous byte, used for checking the start of a packet
    b = 0                               #other variable to test
    data = [0] * 129                    #array to store bytes between each package
    data2 = [0] * 113                   #array to store bytes to be transmitted to a file

    #check value of the current byte being read:
    while True:

        #packet start:
        if prevByte == '0x80' and c1 == '0xff':
            b += 1
        #found a packet:
        elif b == 1 and c1 == '0xaa' and prevByte == '0xff':
            b = 0

            #take data and store in an array:
            for i in range(len(data)):
                c = ord(f.read(1))
                data[i] = c

            #descramble data:
            data2 = descramble(data)

            #make sure new data array actually has data:
            if (data2 != None):
                #add descrambled array to descrambled.txt file:
                for i in range(len(data2)):
                    if (data2[i] == 170):
                        break
                    fa.write(data2[i].to_bytes(1))
            #no more data to write:
            else:
                break

        #read next byte:
        prevByte = c1
        c = f.read(1)
        if (len(c) == 0):
            break
        c1 = hex(ord(c))


    #close files:
    f.close()
    fa.close()
        
            
#testing out the descrambler:
readTxt()