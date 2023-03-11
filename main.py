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

######################################################################################################################
#Test Tab

#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")

def req_packet():
    #Create serial port object

    uart = serial.Serial("COM3", 9600, timeout=1)
    line = uart.readline()
    print("Beacon Text:")
    print(line)

#Adds buttons to interface
send_packet_btn = ttk.Button(test_tab, text="Send Packet", command=send_packet, padding=5).grid(column=0,row=0)
req_packet_btn = ttk.Button(test_tab, text="Request Packet", command=req_packet, padding=5)
req_packet_btn.grid(column=1,row=0)
req_packet_btn.state(['disabled']) #Remove when ready for testing

######################################################################################################################
#All other tabs contained within separate modules

root.mainloop()