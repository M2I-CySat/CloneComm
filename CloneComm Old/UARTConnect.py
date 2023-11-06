import serial
from tkinter import *
from tkinter import ttk
import CySatLog

#Creates the interface used to connect to and disconnect from UART

class UARTConnect(ttk.Frame):

    def __init__(self, frame, logger):

        super(UARTConnect, self).__init__(frame)
        self.logger = logger

        uart_toplabel = ttk.Label(self, text="UART Not Connected", background='red')
        uart_toplabel.grid(column=0,columnspan=3)

        #Creates entry boxes for UART port and baud rate
        #Sets default port and baud rate values
        port_entrytxt = StringVar(self, value="5")
        baud_entrytxt = StringVar(self, value="9600")

        ttk.Label(self, text="Port:").grid(column=0,row=2,sticky=W,pady=10)
        port_entry = ttk.Entry(self,textvariable=port_entrytxt)
        port_entry.grid(column=1,row=2)
        ttk.Label(self,text="Baud Rate:").grid(column=0,row=3,sticky=W)
        baud_entry = ttk.Entry(self,textvariable=baud_entrytxt)
        baud_entry.grid(column=1,row=3)


        #TEST MODE
        #Creates a check box to enable/disable test mode
        #Test mode will be used to test interface functions if no UART connection is present
        test_mode_switcher = IntVar()

        def change_mode():
            global test_mode

            if test_mode_switcher.get() == 1:
                test_mode = TRUE
            else:
                test_mode = FALSE

        test_Mode = ttk.Checkbutton(self, text='Test Mode', variable=test_mode_switcher, onvalue=1, offvalue=0, command=change_mode)
        test_Mode.grid(column=0,row=5)


        # UART Port initialization
        def uart_init():  
            global uart
            global test_mode

            port = "COM" + port_entry.get()
            baud = baud_entry.get()

            try:
                uart = serial.Serial(port, baud, timeout=10)
            except:
                print("No UART Port Connected")
                logger.writeToLog("UART Connect- Failed")
                if test_mode:
                    port_entry.config(state='disabled')
                    baud_entry.config(state='disabled')
                    connect_to_UART.config(state='disabled')
                    disconnect_UART.config(state='!disabled')
                return
                
            #If UART connects successfully (or test mode is enabled), disables port and baud rate entry boxes
            if uart.is_open:
                print("UART Port Open")
                logger.writeToLog("UART Connect- Success")
                port_entry.config(state='disabled')
                baud_entry.config(state='disabled')
                connect_to_UART.config(state='disabled')
                disconnect_UART.config(state='!disabled')
                # Start reader thread
                # reader_thread = uart_module.uart_reader(uart, logger)
                # reader_thread = reader_thread
                # print("UART Read Thread Started")
                # reader_thread.start()
            else:
                print("UART Error! (Port probably not configured properly)")
                logger.writeToLog("UART Connect- Error")

        def uart_close():
            global uart
            logger.writeToLog("UART Disconnect")
            try:
                uart.close()
                print("UART Closed")
            except:
                print("UART Not Open")
            
            #Re-enables entry boxes and UART connect button, disables UART disconnect button
            port_entry.config(state='!disabled')
            baud_entry.config(state='!disabled')
            connect_to_UART.config(state='!disabled')
            disconnect_UART.config(state='disabled')

        connect_to_UART = ttk.Button(self, text="Connect", command=uart_init)
        connect_to_UART.grid(column=0,row=4,pady=10,sticky=W)

        disconnect_UART = ttk.Button(self, text="Disconnect", command=uart_close, state='disabled')
        disconnect_UART.grid(column=1,row=4,pady=10,sticky=E)