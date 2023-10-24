import zmq
import random
import sys
import time
import pmt
import numpy as np


def str_to_array(stra):
    arr= [0]*len(stra)
    for i in range(len(stra)):
        #print(str(int(stra[i])))
        arr[i] = ord(stra[i])
    print(arr)
    return arr




port = "5556"

context = zmq.Context()
socket = context.socket(zmq.PUB)
#socket.connect("tcp://10.26.194.16:5556")
#socket.bind("tcp://10.26.194.74:5556")
socket.connect("tcp://10.26.197.65:5556")


i=1

while True:
    message = str_to_array(str("(Message #"+str(i)+") Hello!\n"))
    message_length = len(message)
    pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(message_length,(message)))

    socket.send(pmt.serialize_str(pdu))
    #socket.send_string("Hello Em!")
    print("Sending "+str(i))
    time.sleep(1)
    i+=1
