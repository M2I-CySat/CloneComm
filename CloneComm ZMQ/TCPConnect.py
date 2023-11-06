from tkinter import *
from tkinter import ttk
import CySatLog
import zmq
import rx

#Creates the interface used to connect to and disconnect from TCP

class TCPConnect(ttk.Frame):

    def __init__(self, frame, logger):

        super(TCPConnect, self).__init__(frame)
        self.logger = logger

        TCP_toplabel = ttk.Label(self, text="TCP Not Connected", background='red')
        TCP_toplabel.grid(column=0,columnspan=3)

        #Creates entry boxes for TCP port and baud rate
        #Sets default port and baud rate values
        ip_entrytxt=("10.26.193.182")
        txport_entrytxt=("5556")
        rxport_entrytxt=("5557")

        ttk.Label(self, text="Ground Station IP:").grid(column=0,row=2,sticky=W,pady=10)
        ip_entry = ttk.Entry(self)
        ip_entry.insert(0,ip_entrytxt)
        ip_entry.grid(column=1,row=2)
        ttk.Label(self,text="TX Port:").grid(column=0,row=3,sticky=W)
        txport_entry = ttk.Entry(self)
        txport_entry.insert(0,txport_entrytxt)
        txport_entry.grid(column=1,row=3)
        ttk.Label(self,text="RX Port:").grid(column=0,row=4,sticky=W)
        rxport_entry = ttk.Entry(self)
        rxport_entry.insert(0,rxport_entrytxt)
        rxport_entry.grid(column=1,row=4)


        #TEST MODE
        #Creates a check box to enable/disable test mode
        #Test mode will be used to test interface functions if no TCP connection is present
        test_mode_switcher = IntVar()

        def change_mode():
            global test_mode

            if test_mode_switcher.get() == 1:
                test_mode = TRUE
            else:
                test_mode = FALSE

        test_Mode = ttk.Checkbutton(self, text='Test Mode', variable=test_mode_switcher, onvalue=1, offvalue=0, command=change_mode)
        test_Mode.grid(column=0,row=6)


        # TCP Port initialization
        def TCP_init():
            global connected  
            global socket_tx
            global socket_rx
            global test_mode

            ip = ip_entry.get()
            txport = txport_entry.get()
            rxport = rxport_entry.get()

            try:
                context_tx = zmq.Context()
                socket_tx = context_tx.socket(zmq.PUB)
                socket_tx.connect("tcp://"+ip+":"+txport)
                context_rx = zmq.Context()
                socket_rx = context_rx.socket(zmq.SUB)
                socket_rx.connect("tcp://"+ip+":"+rxport)
                socket_rx.subscribe("")
                connected = True
            except:
                print("No TCP Port Connected")
                logger.writeToLog("TCP Connect- Failed")
                if test_mode:
                    ip_entry.config(state='disabled')
                    txport_entry.config(state='disabled')
                    rxport_entry.config(state='disabled')
                    connect_to_TCP.config(state='disabled')
                    disconnect_TCP.config(state='!disabled')
                return
                
            #If TCP connects successfully (or test mode is enabled), disables port and baud rate entry boxes
            print("TCP Port Open")
            logger.writeToLog("TCP Connect- Success")
            ip_entry.config(state='disabled')
            txport_entry.config(state='disabled')
            rxport_entry.config(state='disabled')
            connect_to_TCP.config(state='disabled')
            disconnect_TCP.config(state='!disabled')

            TCP_toplabel.config(text="TCP Connected", background='green')

            # Start reader thread
            # reader_thread = TCP_module.TCP_reader(TCP, logger)
            # reader_thread = reader_thread
            # print("TCP Read Thread Started")
            # reader_thread.start()


        def TCP_close():
            global connected
            global socket_tx
            global socket_rx
            logger.writeToLog("TCP Disconnect")
            try:
                socket_tx.disconnect()
                socket_rx.disconnect()
                connected = False
                print("TCP Closed")
            except:
                print("TCP Not Open")
            
            #Re-enables entry boxes and TCP connect button, disables TCP disconnect button
            ip_entry.config(state='!disabled')
            txport_entry.config(state='!disabled')
            rxport_entry.config(state='!disabled')
            connect_to_TCP.config(state='!disabled')
            disconnect_TCP.config(state='disabled')
            TCP_toplabel.config(text="TCP Not Connected", background='red')

        connect_to_TCP = ttk.Button(self, text="Connect", command=TCP_init)
        connect_to_TCP.grid(column=0,row=5,pady=10,sticky=W)

        disconnect_TCP = ttk.Button(self, text="Disconnect", command=TCP_close, state='disabled')
        disconnect_TCP.grid(column=1,row=5,pady=10,sticky=E)