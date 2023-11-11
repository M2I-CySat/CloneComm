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
from os.path import exists


# C L O N E C O M M   Z M Q
# By Steven Scheuermann

# CloneComm clientside

# There will be a CloneComm "Server" GNU Radio program with 2 ZMQ blocks

# This program is pretty ugly due to quirks and prior commitments that were abandoned too late

# It would be distributed throughout multiple .py files but stuff happened

# The old version was so beautiful before I had to restart :(






# This has to be done outside main because commandlogger hates me (It might not any more but im not changing it)

# Variables
global connected
connected = False
global socket_tx
global socket_rx

# Basic Window Configuration
app = qt.QApplication([])
#app.setStyle("Windows")
window = qt.QWidget()
window.setWindowTitle("CloneComm ZMQ")
window.setFixedWidth(1000)
window.setFixedHeight(600)

# Setting up the logger early because bad things (might no longer?) happen if I don't
global commandlogger
commandlogger = qt.QTextEdit()





class WorkerSignals(qtc.QObject): # Code for most multithreading stuff borrowed from https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress
    '''
    finished = qtc.pyqtSignal()
    error = qtc.pyqtSignal(tuple)
    result = qtc.pyqtSignal(str)
    progress = qtc.pyqtSignal(int)

# More multithreading stuff I don't understand. This is only used for the tcp rx so you shouldn't need to mess with it

class Worker(qtc.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress

    @qtc.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

# Function to start up reception

def start_reception(args):
    print(str(connected))
    # Pass the function to execute
    worker = Worker(rxtask,args)
    worker.signals.result.connect(log_output)
    worker.signals.finished.connect(thread_complete)
    #worker.signals.progress.connect(progress_fn)

    # Execute
    threadpool.start(worker)

# Other stuff I don't fully understand

def thread_complete():
    log_output("Thread complete")

def progress_fn():
    log_output("Some progress idk")

# Logs a string to the command log and scrolls to the maximum upon message reception

def log_output(str):
    commandlogger.append(str)
    commandlogger.verticalScrollBar().setValue(commandlogger.verticalScrollBar().maximum())




# I wanted to put these in their own file but it is being stupid
# Connects to the internet and starts reception task
def connect(ip,txport,rxport,connectedvar):
    global socket_tx
    global socket_rx
    global connected
    if connected == False:
        try:
            context_tx = zmq.Context()
            socket_tx = context_tx.socket(zmq.PUB)
            socket_tx.connect("tcp://"+ip+":"+txport)
            context_rx = zmq.Context()
            socket_rx = context_rx.socket(zmq.SUB)
            socket_rx.connect("tcp://"+ip+":"+rxport)
            socket_rx.subscribe("")
            connected = True
            log_output("Connected to server")
            start_reception(connectedvar)
        except:
            log_output("Error connecting to server")
            connected = False
            return
# Disconnects from the internet and stops reception task
def disconnect(connected2):
    global socket_tx
    global socket_rx
    global connected
    try:
        socket_tx.disconnect()
        socket_rx.disconnect()
        connected = False
        log_output("TCP Closed")
    except:
        log_output("TCP Disconnect Error")
        connected = False
    return connected


# The reception task. Handles incomiong packets from CySat.
def rxtask(connected2):
    global socket_tx
    global socket_rx
    global connected
    filename = ""
    extension = ""
    packetIDs = [0]
    j = 0
    filler = [0] * 113
    filler = {0xAA}
    print(str(connected))
    while connected:
        try:
            messagerx = socket_rx.recv(flags=zmq.NOBLOCK)
            print("Packet received")
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
                    log_output(statusmessage)
                    log_output(str(messagerx.hex()))
                    if descramble==True:
                        print("Packet descrambler goes here")
                        messagerx = messagerx[2:]
                        
                        #write current data:
                        data = [0] * 131
                        data = descrambler.descramble(messagerx)

                        # account for this packet being written:
                        packetID = int.from_bytes(data[8:11], byteorder="little")
                        print("Packet ID: "+str(packetID))
                        
                        j += 1
                        print("Appending " + str(packetID) + " to list.")
                        packetIDs.append(packetID)
                        print("New item: " + str(packetIDs[j]))

                        # generation extension and save data type:
                        match data[3]:
                            case 0x00:
                                extension = ".DAT"
                            case 0x01:
                                extension = ".KEL"
                            case 0x02:
                                extension = ".LIS"
                            case 0x03:
                                extension = ".HCK"
                            case _:
                                extension = ".TXT"
                        dataType = int.from_bytes(data[4:7], byteorder="little")

                        # check for missing packets out of order
                        # check for missing packets:
                        # if packetID > j:
                        #     log_output("Packet missing")
                        #     while packetID > j:
                        #         # make a call to seek()
                        #         # seek(113 * missing packet #)
                        #         filename = str(dataType) + extension
                        #         if exists(filename):
                        #             f = open(filename, "ab")
                        #         else:
                        #             f = open(filename, "wb+")
                        #         f.write(filler)
                        #         f.close()
                        #         j += 1

                        # print current packet:
                        filename = str(dataType) + extension
                        if exists(filename):
                            f = open(filename, "r+b")
                        else:
                            f = open(filename, "wb+")
                        f.seek(packetID*113)
                        f.write(data[13:(data[12] + 13)])
                        f.close()

                        #print("After descramble")
                        #log_output("[PACKET RX]: "+str(data[13:(data[12] + 13)]))
                        sum = 0
                        i=0
                        while i < len(packetIDs):
                            if i in packetIDs:
                                a=1
                            else:
                                print("Packet #"+str(i)+" missing.")
                                sum+=1
                            i+=1
                        #log_output("[PACKET RX]: "+str(data[13:data[12]+13]))
                        
                    break
        except zmq.Again as e:
            e=1
        time.sleep(0.01)
        #log_output("Hello")
        # put packet missing insertion here:


# Sends a message to CySat
def uplink(message):
    global socket_tx
    message_length = len(message)
    pdu = pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(message_length,(message)))
    socket_tx.send(pmt.serialize_str(pdu))

# I don't know but apparetly I had a good reason for this at one point
def return_response(rx):
    rx = bytearray(rx)
    return cspp.ax.return_bytearray_as_hex_spaces(rx)

def get_datatype(str):
    match str:
        case "DAT":
            return 0
        case "KEL":
            return 1
        case "LIS":
            return 2
        case "HCK":
            return 3
        case "TES":
            return 4

# Where the GUI is set up


class button():
    def __init__(self, layout, text, command,x,y):
        global socket_tx
        self = qt.QPushButton(text)
        self.clicked.connect(command)
        layout.addWidget(self,x,y)



def main():
    global connected
    global socket_tx

    # Setup the layouts
    mainlayout = qt.QVBoxLayout()
    upperlayout = qt.QHBoxLayout()
    lowerlayout = qt.QVBoxLayout()
    commandlayout = qt.QGridLayout()


    # Initialie Command Send Area

    # Initialize Feature Tabs
    ctabs = qt.QTabWidget()
    OBCTab = qt.QWidget()
    ADCSTab = qt.QWidget()
    EPSTab = qt.QWidget()
    UHFTab = qt.QWidget()
    PayloadTab = qt.QWidget()
    EOLTab = qt.QWidget()

    # OBC Tab
    obclayout = qt.QVBoxLayout()
    obccomlayout=qt.QGridLayout()
    # b1 = qt.QPushButton("Ping Satellite")
    # b1.clicked.connect(lambda: uplink(cspp.makeCySatPacket("OBC","01",[], True, True, True))) # Done
    # commandlayout.addWidget(b1,1,1)
    button(obccomlayout,"Ping Satellite",lambda: uplink(cspp.makeCySatPacket("OBC","01",[], True, True, True)),1,1)
    button(obccomlayout,"Request File List",lambda: uplink(cspp.makeCySatPacket("OBC","13",[], True, True, True)),1,2)
    button(obccomlayout,"Restart Satellite",lambda: uplink(cspp.makeCySatPacket("OBC","15",[], True, True, True)),1,3)
    button(obccomlayout,"ADCS Health Check",lambda: uplink(cspp.makeCySatPacket("ADCS","09",[], True, True, True)),2,1)
    button(obccomlayout,"EPS Health Check",lambda: uplink(cspp.makeCySatPacket("EPS","13",[], True, True, True)),2,2)
    button(obccomlayout,"EPS Health Check",lambda: uplink(cspp.makeCySatPacket("UHF","23",[], True, True, True)),2,3)
    obclayout.addLayout(obccomlayout)
    # File Send Layout
    sendlayout = qt.QGridLayout()

    sendlayout.addWidget(qt.QLabel("File Downlink And Delete Controls"),1,2)


    # File Delete Stuff
    # Dropdown menu for file type
    typesel2 = qt.QComboBox()
    sendlayout.addWidget(qt.QLabel("Data Type"),2,2)
    typesel2.addItems(['Select file type','DAT', 'KEL', 'LIS', 'HCK'])
    sendlayout.addWidget(typesel2,3,2)

    # Text box for file number
    numsel2 = qt.QLineEdit("")
    sendlayout.addWidget(qt.QLabel("File Number"),2,3)
    sendlayout.addWidget(numsel2,3,3)

    # Send Button
    button(sendlayout,"Delete File",lambda: uplink(cspp.makeCySatPacket("OBC","17",[["int",int(numsel2.text()),4],["int",get_datatype(typesel2.currentText()),4]], True, True, True)),3,4)
    obclayout.addLayout(sendlayout)

    # Dropdown menu for file type
    typesel = qt.QComboBox()
    sendlayout.addWidget(qt.QLabel("Data Type"),4,2)
    typesel.addItems(['Select file type','DAT', 'KEL', 'LIS', 'HCK', 'TES'])
    sendlayout.addWidget(typesel,5,2)
    
    # Text box for file number
    numsel = qt.QLineEdit("8")
    sendlayout.addWidget(qt.QLabel("File Number"),4,3)
    sendlayout.addWidget(numsel,5,3)

    # Text box for start packet
    spsel = qt.QLineEdit("0")
    sendlayout.addWidget(qt.QLabel("Start Packet"),4,4)
    sendlayout.addWidget(spsel,5,4)
    # Text box for end packet
    epsel = qt.QLineEdit("80")
    sendlayout.addWidget(qt.QLabel("End Packet"),4,5)
    sendlayout.addWidget(epsel,5,5)

    # Send Button
    button(sendlayout,"Retrieve File",lambda: uplink(cspp.makeCySatPacket("OBC","11",[["int",int(numsel.text()),4],["int",get_datatype(typesel.currentText()),4],["int",int(spsel.text()),4],["int",int(epsel.text()),4]], True, True, True)),5,5)
    obclayout.addLayout(sendlayout)

    # ADCS Tab
    adcslayout = qt.QVBoxLayout()

    adcsclayout = qt.QGridLayout()

    button(adcsclayout,"Update TLEs",lambda: uplink(ADCS.TC_45()),1,1)
    button(adcsclayout,"Update Time",lambda: uplink(ADCS.TC_2()),1,2)

    adcsglayout = qt.QGridLayout()
    # Telemetry Request

    adcsglayout.addWidget(qt.QLabel("Telemetry Request Number"),0,2)
    adcsglayout.addWidget(qt.QLabel("Output Data Length"),0,3)

    numsel3 = qt.QLineEdit("140")
    adcsglayout.addWidget(numsel3,1,2)
    numsel3a = qt.QLineEdit("6")
    adcsglayout.addWidget(numsel3a,1,3)
    button(adcsglayout,"Telemetry Request",lambda: uplink(ADCS.TLM(int(numsel3.text()),int(numsel3a.text()))),1,1)


    adcsglayout.addWidget(qt.QLabel("Command Number"),2,2)
    adcsglayout.addWidget(qt.QLabel("Data (Hex)"),2,3)
    numsel4 = qt.QLineEdit("10")
    adcsglayout.addWidget(numsel4,3,2)
    numsel5 = qt.QLineEdit("01")
    adcsglayout.addWidget(numsel5,3,3)
    button(adcsglayout,"Telecommand",lambda: uplink(ADCS.TC(int(numsel4.text()),numsel5.text())),3,1)

    adcslayout.addLayout(adcsclayout)
    adcslayout.addLayout(adcsglayout)


    # EPS Tab

    epslayout = qt.QVBoxLayout()




    # Combine tabs into one thing
    OBCTab.setLayout(obclayout)
    ADCSTab.setLayout(adcslayout)
    ctabs.addTab(OBCTab,"OBC")
    ctabs.addTab(ADCSTab,"ADCS")
    ctabs.addTab(EPSTab,"EPS")
    ctabs.addTab(UHFTab,"UHF")
    ctabs.addTab(PayloadTab,"Payload")
    ctabs.addTab(EOLTab,"EOL")

    #upperlayout.addLayout(commandlayout)
    upperlayout.addWidget(ctabs)


    # Initialize Feature Tabs
    tabs = qt.QTabWidget()
    tcptab = qt.QWidget()
    filetab = qt.QWidget()
    timingtab = qt.QWidget()
    infotab = qt.QWidget()

    # TCP Connect Tab
    tcplayout = qt.QGridLayout()

    ipbox = qt.QLineEdit("10.26.193.173")
    tcplayout.addWidget(qt.QLabel("Server IP"),1,1)
    tcplayout.addWidget(ipbox,1,2)

    txportbox = qt.QLineEdit("5556")
    tcplayout.addWidget(qt.QLabel("Uplink Port"),2,1)
    tcplayout.addWidget(txportbox,2,2)

    rxportbox = qt.QLineEdit("5557")
    tcplayout.addWidget(qt.QLabel("Downlink Port"),3,1)
    tcplayout.addWidget(rxportbox,3,2)

    connectbutton = qt.QPushButton("Connect")
    connectbutton.clicked.connect(lambda: connect(ipbox.text(),txportbox.text(),rxportbox.text(),connected))
    tcplayout.addWidget(connectbutton,4,1)

    disconnectbutton = qt.QPushButton("Disconnect")
    disconnectbutton.clicked.connect(lambda: disconnect(connected))
    tcplayout.addWidget(disconnectbutton,5,1)

    tcptab.setLayout(tcplayout)

    # File Status Tab

    # Pass Timing Tab

    # Info Tab


    # Initialize Command Log
    lowerlayout.addWidget(qt.QLabel("Command Log"))

    lowerlayout.addWidget(commandlogger)





    # Combine and show the layouts, do multithreading init stuff, and execute the program
    tabs.addTab(tcptab,"TCP Connection")
    tabs.addTab(filetab,"File Status")
    tabs.addTab(timingtab,"Pass Timing")
    tabs.addTab(infotab,"Info")

    upperlayout.addLayout(commandlayout)
    upperlayout.addWidget(tabs)


    mainlayout.addLayout(upperlayout)
    mainlayout.addLayout(lowerlayout)
    window.setLayout(mainlayout)
    window.show()

    global threadpool
    threadpool = qtc.QThreadPool()
    app.threadpool = threadpool


    print("Multithreading with maximum %d threads" % app.threadpool.maxThreadCount())
    app.exec()
    connected = False # This is so the thread exits


if __name__ == "__main__":
    main()
