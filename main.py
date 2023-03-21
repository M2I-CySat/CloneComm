from tkinter import *
from tkinter import ttk
import importlib
import serial
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

#Creates the main application window
root = Tk()
root.title("CloneComm")
mainframe = ttk.Frame(root, padding=5)
ttk.Label(mainframe, text="CySat Commands", font="TkHeadingFont").grid(row=0, column=0, columnspan=3)

#Organizes widgets inside the main window
mainframe.grid(row=0, column=0)

#Creates tabs for each subsystem
tab_interface = ttk.Notebook(mainframe, padding=5)
tab_interface.grid(row=1,column=1,rowspan=3,sticky=NSEW)

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


###
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
log = Text(root, state='disabled', width=40, height=24, wrap='none')
log.grid(row=1, column=1, rowspan=3, sticky=NSEW) # sticky=NSEW allows the text box to expand with the window

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

ttk.Label(test_tab,text="Port:").grid(column=0,row=0,sticky=W,pady=10)
port_entry = ttk.Entry(test_tab)
port_entry.grid(column=1,row=0)
ttk.Label(test_tab,text="Baud Rate:").grid(column=0,row=1,sticky=W)
baud_entry = ttk.Entry(test_tab)
baud_entry.grid(column=1,row=1)


#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")
    print(port_entry.get())
    writeToLog("Packet Send Button Test")

def req_packet():
    #Create serial port object

    uart = serial.Serial("COM5", 9600, timeout=10)
    line = uart.readline()
    print("Beacon Text:")
    print(line)
    uart.close()
    writeToLog("Beacon Text: " + line)

#Adds buttons to interface
send_packet_btn = ttk.Button(test_tab, text="Send Packet", command=send_packet)
send_packet_btn.grid(column=0,row=2,pady=10)
req_packet_btn = ttk.Button(test_tab, text="Request Packet", command=req_packet)
req_packet_btn.grid(column=1,row=2,pady=10)
#req_packet_btn.state(['disabled']) #Remove when ready for testing

######################################################################################################################
#All other tabs contained within separate modules

root.mainloop()