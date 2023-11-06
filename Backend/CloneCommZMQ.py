# C L O N E C O M M   Z M Q
# By Steven Scheuermann

# CloneComm clientside

# There will be a CloneComm "Server" GNU Radio program with 2 ZMQ blocks


import zmq
import time
import pmt
import numpy as np
import CSPP_generator as cspp
import crcmod
import TC_45
import descrambler

addr = "10.26.193.182"


def str_to_array(stra):
    arr= [0]*len(stra)
    for i in range(len(stra)):
        arr[i] = ord(stra[i])
    print(arr)
    return arr

def bytearray_to_array(barry):
    arr = [0]*len(barry)
    for i in range(len(barry)):
        arr[i] = ord(barry[i])
    print(arr)
    return arr

def return_response(rx):
    rx = bytearray(rx)
    return cspp.ax.return_bytearray_as_hex_spaces(rx)
    
context_tx = zmq.Context()
socket_tx = context_tx.socket(zmq.PUB)
socket_tx.connect("tcp://"+addr+":5556")

context_rx = zmq.Context()
socket_rx = context_rx.socket(zmq.SUB)
socket_rx.connect("tcp://"+addr+":5557")
socket_rx.subscribe("")


#message = cspp.makeCySatPacket("OBC","01",[], True, True, True)

#message = TC_45.TC_45()

i=0
while True:
    #if i%500 == 0:
    #    message_length = len(message)
    #    pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(message_length,(message)))
#
    #    socket_tx.send(pmt.serialize_str(pdu))
    #    #print("Sending "+str(i))

    try:
        messagerx = socket_rx.recv(flags=zmq.NOBLOCK)
        statusmessage = ""
        filename = ""
        extension = ""
        j = 0
        descramble = False
        for i in range(0,len(messagerx)):
            if messagerx[i] == 0xFF:
                messagerx = messagerx[i:]
                if messagerx[2]%2==1:
                    statusmessage+= "[TX] [CSPP] "
                else:
                    statusmessage+= "[RX] [CSPP] "
                match messagerx[1]:
                    case 0xAA:
                        statusmessage+= "[PACKET] "
                        descramble = True
                        # see if file is already open, if not, create it
                        if filename.exists() == False:
                            match messagerx[5]:
                                case 0x00:
                                    extension = ".DAT"
                                    dataType = 0x00
                                case 0x01:
                                    extension = ".KEL"
                                    dataType = 0x01
                                case 0x02:
                                    extension = ".LIS"
                                    dataType = 0x02
                                case 0x03:
                                    extension = ".HCK"
                                    dataType = 0x03
                                case _:
                                    extension = ".TXT"
                                    dataType = 0x04
                            filename += extension
                            fw = open(filename, "wb+")
                    case 0x0A:
                        statusmessage+= "[OBC] "
                    case 0x14:
                        statusmessage+= "[ADCS] "
                    case 0x1E:
                        statusmessage+= "[EPS] "
                    case 0x0E:
                        statusmessage+= "[UHF] "
                    case 0x28:
                        statusmessage+= "[SDR] "
                    case 0x5A:
                        statusmessage+= "[EOL] "
                    case _:
                        print("Packet not recognized")
                statusmessage+="[COMMAND: "+"{:02x}".format(messagerx[2])+"] [LENGTH: "+str(messagerx[3])+"]:\n[HEX]: "+(return_response(messagerx[4:-1]))+"\n"+"[STR]: "+(messagerx[4:-1]).decode("utf-8","replace")+"\n"
                print(statusmessage)
                if descramble==True:
                    print("Packet descrambler goes here")
                    messagerx = messagerx[2:]
                    # check packet ID and ensure that no packet is missing:
                    packetID = int.from_bytes(messagerx[8:11], byteorder="big")
                    #packet/packets is/are missing:
                    if packetID > j:
                        #fill in file until reached current packet ID number:
                        while packetID > j:
                            arr = [0] * 8
                            # three 0xAA bytes:
                            arr[0:2] = {0xAA}
                            # data type:
                            arr[3] = dataType
                            # measurement ID bytes:
                            arr[4:7] = bytearray(0, byteorder="big")
                            # packet ID bytes:
                            arr[8:11] = bytearray(j, byteorder="big")
                            #bytes read:
                            arr[12] = bytes(71)

                            # write to file:
                            fw.write(descrambler.fillData(arr))
                            j +=1
                        #write current data:
                        fw.write(descrambler.descramble(messagerx))
                    j += 1
        fw.close()
    except zmq.Again as e:
        e=1
    time.sleep(0.01)
    i=i+1
