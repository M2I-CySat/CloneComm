import zmq
import descrambler
import time
import CSPP_generator as cspp


def return_response(rx):
    rx = bytearray(rx)
    return cspp.ax.return_bytearray_as_hex_spaces(rx)

def rx(socket_rx):
    print("TASKING")
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
                    messagerx = messagerx[2:]
                    descrambler.descramble(messagerx)
                    print("After descramble")
                
                break
    except zmq.Again as e:
        e=1
    time.sleep(0.01)