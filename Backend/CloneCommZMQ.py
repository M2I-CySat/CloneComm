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

message = TC_45.TC_45()

i=0
while True:
    if i%500 == 0:
        message_length = len(message)
        pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(message_length,(message)))

        socket_tx.send(pmt.serialize_str(pdu))
        #print("Sending "+str(i))

    try:
        messagerx = socket_rx.recv(flags=zmq.NOBLOCK)
        statusmessage = ""
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
                    descrambler.readTxt(messagerx[2:])
                    print("After descramble")
                
                break
    except zmq.Again as e:
        e=1
    time.sleep(0.01)
    i=i+1
