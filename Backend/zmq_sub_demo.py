import zmq
import time

print(zmq.__version__)
context = zmq.Context()
socket = context.socket(zmq.SUB)
#socket.connect("tcp://10.24.222.150:5556")
socket.connect("tcp://10.26.197.65:5557")
socket.subscribe("")
while True:
    try:
        message = socket.recv(flags=zmq.NOBLOCK)
        print("Message rx")
        print(str(message))
    except zmq.Again as e:
        e=1
    time.sleep(0.01)