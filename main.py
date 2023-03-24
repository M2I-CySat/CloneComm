from tkinter import *
from tkinter import ttk
import importlib
import serial
import time
from ADCSTab import adcs_Tab
from SDRTab import sdr_Tab
from EPSTab import eps_Tab
from OBCTab import obc_Tab
from UHFTab import uhf_Tab

#Use struct to send data (packets)?

#Imports CySatGlobal for command information
global_module = importlib.import_module('CySatGlobal')
cmd_dictionary = global_module.cmd_dictionary
sys_dictionary = global_module.sys_dictionary
sys_list = global_module.sys_list

global_module.populate_global_variables()

uart = NONE
test_mode = FALSE

#Creates the main application window
root = Tk()
root.title("CloneComm")
mainframe = ttk.Frame(root, padding=5)
mainframe.grid(row=0, column=0)

ttk.Label(mainframe, text="CySat Commands", font="TkHeadingFont").grid(row=0, column=0)

#Creates tabs for each subsystem
tab_interface = ttk.Notebook(mainframe, padding=3)
tab_interface.grid(row=1,column=0,sticky=NSEW)

test_tab = ttk.Frame(tab_interface,padding=5)
obc_tab = obc_Tab(tab_interface)
adcs_tab = adcs_Tab(tab_interface)
sdr_tab = sdr_Tab(tab_interface)
eps_tab = eps_Tab(tab_interface)
uhf_tab = uhf_Tab(tab_interface)

tab_interface.add(test_tab, text='Test')
tab_interface.add(obc_tab, text='  OBC  ')
tab_interface.add(adcs_tab, text='  ADCS  ')
tab_interface.add(sdr_tab, text='  SDR  ')
tab_interface.add(eps_tab, text='  EPS  ')
tab_interface.add(uhf_tab, text='  UHF  ')

######################################################################################################################
#UART interface for connecting and disconnecting

UART_frame = ttk.Frame(mainframe, padding=5)
UART_frame.grid(row=2,column=0)
UART_label = ttk.Label(UART_frame, text="Connect to UART")
UART_label.grid(row=1,column=0,columnspan=2)

#Creates a check box to enable/disable test mode
def change_mode():
    global test_mode

    if test_mode_switcher.get() == 1:
        test_mode = TRUE
    else:
        test_mode = FALSE

test_mode_switcher = IntVar()
test_Mode = ttk.Checkbutton(UART_frame, text='Test Mode', variable=test_mode_switcher, onvalue=1, offvalue=0, command=change_mode)
test_Mode.grid(column=3,row=0,sticky=E)

#Creates entry boxes for UART port and baud rate
#Sets default port and baud rate values
port_entrytxt = StringVar(UART_frame, value="5")
baud_entrytxt = StringVar(UART_frame, value="9600")

ttk.Label(UART_frame,text="Port:").grid(column=0,row=2,sticky=W,pady=10)
port_entry = ttk.Entry(UART_frame,textvariable=port_entrytxt)
port_entry.grid(column=1,row=2)
ttk.Label(UART_frame,text="Baud Rate:").grid(column=0,row=3,sticky=W)
baud_entry = ttk.Entry(UART_frame,textvariable=baud_entrytxt)
baud_entry.grid(column=1,row=3)

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
        writeToLog("UART Connect- Failed")
        if test_mode:
            port_entry.config(state='disabled')
            baud_entry.config(state='disabled')
            connect_to_UART.config(state='disabled')
            disconnect_UART.config(state='!disabled')
            UART_label.config(text='UART Connected')
        return
        
    #If UART connects successfully (or test mode is enabled), disables port and baud rate entry boxes
    if uart.is_open:
        print("UART Port Open")
        writeToLog("UART Connect- Success")
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
        writeToLog("UART Connect- Error")

def uart_close():
    global uart
    writeToLog("UART Disconnect")
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
    UART_label.config(text='UART Not Connected')

connect_to_UART = ttk.Button(UART_frame, text="Connect", command=uart_init)
connect_to_UART.grid(column=0,row=4,pady=10,sticky=W)

disconnect_UART = ttk.Button(UART_frame, text="Disconnect", command=uart_close, state='disabled')
disconnect_UART.grid(column=1,row=4,pady=10,sticky=E)

######################################################################################################################
#NOTE: These commands were for when other tabs were included in the same file

#Populates dropdown list (combobox option names) for the selected subsystem
def get_dropdown_list(tab_index):
    cmd_list = cmd_dictionary[tab_index]
    dropdown_cmd_list = []
    for key, value in cmd_list.items():
        if(value.cmd_sendable == 1):
            dropdown_cmd_list.append(value.cmd_description)
    return(dropdown_cmd_list)

#Populates command list for the selected subsystem (used for more technical tasks)
def get_cmd_list(tab_index):
    cmd_list = cmd_dictionary[tab_index]
    return(cmd_list)


#Creates a terminal window on the side of the main window which displays the output of the program
ttk.Label(mainframe, text="Command Log",padding=3).grid(row=0, column=1)
log = Text(mainframe, state='disabled', width=40, height=24, wrap='none')
log.grid(row=1, column=1, rowspan=2, sticky=NSEW)

#Prints a message in the logging (terminal) window
def writeToLog(msg):
    numlines = int(log.index('end - 1 line').split('.')[0])
    log['state'] = 'normal'
    if numlines==24:
        log.delete(1.0, 2.0)
    if log.index('end-1c')!='1.0':
        log.insert('end', '\n')
    log.insert('end', msg)
    log['state'] = 'disabled'

######################################################################################################################
#Test Tab

#Commands for basic packet-sending testing
def send_packet():
    print("Send Packet (Currently nonfunctional)")
    print(port_entry.get())
    writeToLog("Send Packet")

def req_packet():
    global uart

    writeToLog("Request Packet")
    if uart == NONE:
        print("UART Not Connected- Connect UART First")
        return
    
    start_time = time.time()
    elapsed_time = time.time() - start_time

    #Read from the port for 60 seconds
    while elapsed_time <= 30:
        byte_line = uart.read_until()
        line = str(byte_line, 'utf-8')
        print("Beacon Text:")
        print(line)
        writeToLog(line)
        elapsed_time = time.time() - start_time


#Adds buttons to interface
send_packet_btn = ttk.Button(test_tab, text="Send Packet", command=send_packet)
send_packet_btn.grid(column=0,row=2,pady=10)
req_packet_btn = ttk.Button(test_tab, text="Request Packet", command=req_packet)
req_packet_btn.grid(column=1,row=2,pady=10)
#req_packet_btn.state(['disabled']) #Remove when ready for testing

######################################################################################################################
#All other tabs contained within separate modules

root.mainloop()