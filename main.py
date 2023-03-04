from tkinter import *
from tkinter import ttk
import importlib

from CySatGlobal import Command
from CySatPacket import Packet
from CySatPacket import create_packet

#Use struct to send data (packets)?

#Imports CySatGlobal for command information
global_module = importlib.import_module('CySatGlobal')
cmd_dictionary = global_module.cmd_dictionary
sys_dictionary = global_module.sys_dictionary
sys_list = global_module.sys_list

global_module.populate_global_variables()

#Creates a new Command class which includes system ID
#Mostly for simulating how a CySat packet will be created (likely to be removed later)
class TypeCommand:
    def __init__(self, sys_id, cmd_id):
        self.sys_id = sys_id
        self.cmd_id = cmd_id

def create_TypeCommand(sys_id, cmd_id):
    sending_cmd = TypeCommand(sys_id, cmd_id)
    return sending_cmd

#Creates the main application window
root = Tk()
root.title("CloneComm")
mainframe = ttk.Frame(root, padding=5)
ttk.Label(mainframe, text="CySat Commands", font="TkHeadingFont").grid(row=0, column=0, columnspan=3)

#Initializes textvariables for dropdown menus
obc_command = StringVar()
sdr_command = StringVar()
eps_command = StringVar()
uhf_command = StringVar()
packet_input = StringVar()

#Organizes widgets inside the main window
mainframe.grid(row=0, column=0)

#Creates tabs for each subsystem
tab_interface = ttk.Notebook(mainframe, padding=5)
tab_interface.grid(row=1,column=1,rowspan=3,sticky=NSEW)

test_tab = ttk.Frame(tab_interface,padding=5)
obc_tab = ttk.Frame(tab_interface,padding=5)
adcs_tab = ttk.Frame(tab_interface,padding=5)
sdr_tab = ttk.Frame(tab_interface,padding=5)
eps_tab = ttk.Frame(tab_interface,padding=5)
uhf_tab = ttk.Frame(tab_interface,padding=5)

tab_interface.add(test_tab, text='Test')
tab_interface.add(obc_tab, text='  OBC  ')
tab_interface.add(adcs_tab, text='  ADCS  ')
tab_interface.add(sdr_tab, text='  SDR  ')
tab_interface.add(eps_tab, text='  EPS  ')
tab_interface.add(uhf_tab, text='  UHF  ')

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
#Test Tab (currently in use for testing interface functions, will be removed later)
#NOTE: All interface elements used in the test tab will be included in each subsystem tab

#Test command list population
test_dropdown = get_dropdown_list(0)
test_cmd_list = get_cmd_list(0)

#-------------------------------------------------------------------#
#DROPDOWN COMMAND MENU
#Creates a dropdown menu for command options
#Uses command list for the selected subsystem
ttk.Label(test_tab, text="Choose Command:", padding=3).grid(column=0,row=0,sticky=W)
test_command = StringVar(test_tab)
test_combobox = ttk.Combobox(test_tab,textvariable=test_command,values=test_dropdown,state=(["readonly"]),width=46)
test_combobox.grid(column=2,row=0)

#When the user selects a command in the combobox, looks for ID of selected command in the command manifest
def get_dropdown_selection():
    for key, value in test_cmd_list.items():
        if(value.cmd_description == test_command.get()):
            value.cmd_id = key
            #Returns command id for selected command
            return value.cmd_id

#Checks if selected command (indicated by cmd_id) has a payload
#Used to enable/disable input box
def command_has_payload():
    cmd = test_cmd_list[get_dropdown_selection()]
    if cmd.cmd_has_payload == 1:
        return TRUE
    else:
        return FALSE

#-------------------------------------------------------------------#
#INPUT BOX
#Creates an input box
ttk.Label(test_tab, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
test_entry = ttk.Entry(test_tab, textvariable=packet_input)
test_entry.grid(column=1,row=2,columnspan=3, sticky=EW)

#Disables input box if a command has not been selected from the dropdown menu
#OR disables input box if the command does not have a data payload
test_entry.state(['disabled'])
def set_entry_state(var,index,mode):
    if test_command.get() == 0 or command_has_payload():
        test_entry.delete(0,END)
        test_entry.state(['disabled'])
    else:
        test_entry.state(['!disabled'])
test_command.trace_add("write", set_entry_state)

#Retrieves data from input box and selection from combobox
def get_input():
    #Command id from dropdown selection will be used to call a specific command
    input = create_TypeCommand(0,get_dropdown_selection())
    print("System ID: " + str(input.sys_id))
    print("Command ID: " + str(input.cmd_id))

#-------------------------------------------------------------------#
#SEND ENTRY BUTTON
#Button to send packet (for testing)
send_custom_btn = ttk.Button(test_tab, text="Send Entry", command=get_input)
send_custom_btn.grid(column=2,row=3,sticky=E)

#Disables the "Send Entry" button:
#   If nothing has been entered
#   If the selected command does not allow the user to enter custom packet data
#Updates any time the user changes the text in the entry box
send_custom_btn.state(['disabled'])
def set_button_state(var,index,mode):
    if len(packet_input.get()) == 0:
        if command_has_payload():
            send_custom_btn.state(['!disabled'])
        else:
            send_custom_btn.state(['disabled'])
    else:
        send_custom_btn.state(['!disabled'])
test_command.trace_add("write", set_button_state)
packet_input.trace_add("write", set_button_state)


######################################################################################################################
#OBC Tab (currently used for testing buttons)
#ADD ANY PACKET TESTING CODE HERE

#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")

def req_packet():
    print("Packet Request Button Test")

#Adds buttons to interface
send_packet_btn = ttk.Button(obc_tab, text="Send Packet", command=send_packet, padding=5).grid(column=0,row=0)
req_packet_btn = ttk.Button(obc_tab, text="Request Packet", command=req_packet, padding=5).grid(column=1,row=0)


######################################################################################################################
#ADCS Tab

#ADCS command list population
adcs_dropdown = get_dropdown_list(2)
adcs_cmd_list = get_cmd_list(2)

#-------------------------------------------------------------------#
#DROPDOWN COMMAND MENU
#Creates a dropdown menu for command options
#Uses command list for the selected subsystem
ttk.Label(adcs_tab, text="Choose Command:", padding=3).grid(column=0,row=0,sticky=W)
adcs_command = StringVar(adcs_tab)
adcs_combobox = ttk.Combobox(adcs_tab,textvariable=adcs_command,values=adcs_dropdown,state=(["readonly"]))
adcs_combobox.grid(column=2,row=0)


######################################################################################################################
#More Tabs!
#Will be added later

#-------------------------------------------------------------------#

root.mainloop()