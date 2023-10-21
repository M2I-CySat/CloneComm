import zmq
import time


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.bind("tcp://127.0.0.1:5556")
socket.subscribe("")
while True:
    try:
        message = socket.recv(flags=zmq.NOBLOCK)
        print("Message rx")
        print(str(message))
    except zmq.Again as e:
        e=1
    time.sleep(0.01)