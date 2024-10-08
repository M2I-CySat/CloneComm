import PyQt5.QtWidgets as qt
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import traceback
import sys
import time
import zmq
import descrambler
import CSPP_generator as cspp
import pmt
import ADCS
import EPS
import SDR
import ax25_function as AX
from os.path import exists


ip = "127.0.0.1"
txport = "5556" 
rxport = "5557" 

context_tx = zmq.Context()
socket_tx = context_tx.socket(zmq.PUB)
#test = socket_tx.connect("tcp://"+ip+":"+txport)
#print(test)

socket_tx.bind("tcp://{}:{}".format(ip, txport)) 
pdu =  pmt.cons(pmt.PMT_NIL, pmt.make_u8vector(32, 0xAA))
while True:
    socket_tx.send(pmt.serialize_str(pdu))
    time.sleep(0.01)

