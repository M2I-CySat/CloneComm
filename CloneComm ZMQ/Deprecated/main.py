from tkinter import *
from tkinter import ttk
import importlib
#import serial
import time
#from InterfaceTab import InterfaceTab
from CySatLog import CySatLog
from TCPConnect import TCPConnect
import multitasking
import rx

#Use struct to send data (packets)?

#Imports CySatGlobal for command information
# global_module = importlib.import_module('CySatGlobal')
# cmd_dictionary = global_module.cmd_dictionary
# sys_dictionary = global_module.sys_dictionary
# sys_list = global_module.sys_list

# global_module.populate_global_variables()

global connected
global logger
uart = NONE
test_mode = FALSE

#Creates the main application window
root = Tk()
root.title("CloneComm")
mainframe = ttk.Frame(root, padding=5)
mainframe.grid(row=0, column=0)


######################################################################################################################
#Creates a logging window

log_label = ttk.Label(mainframe, text="Command Log",padding=3)
log_label.grid(row=2, column=0, columnspan=2)

logger = CySatLog(mainframe, state='disabled', wrap='none')
logger.grid(row=3, column=0, columnspan=3, sticky=NSEW)


######################################################################################################################
#UART interface for connecting and disconnecting

UART_label = ttk.Label(mainframe, text="Connect to TCP Server")
UART_label.grid(row=0,column=1)

UART_frame = TCPConnect(mainframe, logger)
UART_frame.grid(row=1,column=1,padx=10,sticky=S)


######################################################################################################################
#Creates tabs for each subsystem

notebook_label = ttk.Label(mainframe, text="CySat Commands", font="TkHeadingFont")
notebook_label.grid(row=0, column=0, padx=10)

tab_interface = ttk.Notebook(mainframe, padding=3)
tab_interface.grid(row=1,column=0,sticky=NSEW)

test_tab = ttk.Frame(tab_interface,padding=5)
# obc_tab = InterfaceTab(tab_interface,"OBC",1,logger)
# adcs_tab = InterfaceTab(tab_interface,"ADCS",2,logger)
# sdr_tab = InterfaceTab(tab_interface,"SDR",3,logger)
# eps_tab = InterfaceTab(tab_interface,"EPS",4,logger)

tab_interface.add(test_tab, text='Test')
# tab_interface.add(obc_tab, text='  OBC  ')
# tab_interface.add(adcs_tab, text='  ADCS  ')
# tab_interface.add(sdr_tab, text='  SDR  ')
# tab_interface.add(eps_tab, text='  EPS  ')


######################################################################################################################
#NOTE: These commands were for when other tabs were included in the same file
#These can be removed when the test tab is no longer needed

#Populates dropdown list (combobox option names) for the selected subsystem
# def get_dropdown_list(tab_index):
#     cmd_list = cmd_dictionary[tab_index]
#     dropdown_cmd_list = []
#     for key, value in cmd_list.items():
#         if(value.cmd_sendable == 1):
#             dropdown_cmd_list.append(value.cmd_description)
#     return(dropdown_cmd_list)

# #Populates command list for the selected subsystem (used for more technical tasks)
# def get_cmd_list(tab_index):
#     cmd_list = cmd_dictionary[tab_index]
#     return(cmd_list)


######################################################################################################################
#Test Tab

#Commands for basic packet-sending testing
def send_packet():
    print("Send Packet (Currently nonfunctional)")
    #print(port_entry.get())
    logger.writeToLog("Send Packet")

def req_packet():
    global uart

    logger.writeToLog("Request Packet")
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
        logger.writeToLog(line)
        elapsed_time = time.time() - start_time

#Adds buttons to interface
send_packet_btn = ttk.Button(test_tab, text="Send Packet", command=send_packet)
send_packet_btn.grid(column=0,row=2,pady=10)
req_packet_btn = ttk.Button(test_tab, text="Request Packet", command=req_packet)
req_packet_btn.grid(column=1,row=2,pady=10)

###
print("Pos -1")
root.mainloop()

