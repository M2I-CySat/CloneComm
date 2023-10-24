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


context_tx = zmq.Context()
socket_tx = context_tx.socket(zmq.PUB)
socket_tx.connect("tcp://10.26.197.65:5556")

context_rx = zmq.Context()
socket_rx = context_rx.socket(zmq.SUB)
#socket_rx.connect("tcp://10.26.197.65:5557")


i=1

message = cspp.makeCySatPacket("OBC","01",[], True, True, True)


while True:
    #message = str_to_array(str("(Message #"+str(i)+") Hello!\n"))
    message_length = len(message)
    pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(message_length,(message)))

    socket_tx.send(pmt.serialize_str(pdu))
    #socket.send_string("Hello Em!")
    print("Sending "+str(i))
    time.sleep(5)
    i+=1
