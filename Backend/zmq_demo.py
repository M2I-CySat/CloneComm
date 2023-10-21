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
socket.connect("tcp://10.50.109.217:5556")

i=1

while True:
    message = str("(Message #"+str(i)+") Hello!\n")
    res = bytes(message, 'utf-8')
    socket.send(pmt.serialize_str(pmt.to_pmt(str_to_array(message))))
    print("Sending "+str(i))
    time.sleep(1)
    i+=1
