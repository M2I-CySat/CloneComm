from tkinter import *
from tkinter import ttk
import importlib
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

#Initializes textvariables for dropdown menus
obc_command = StringVar()
adcs_command = StringVar()
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

######################################################################################################################
#Test Tab (currently in use for testing interface functions, will be removed later)

tab_interface.add(test_tab, text='Test')

#Populates command list for the selected subsystem (in this case, test (id = 1))
#Will be used for other subsystems
cmd_list = cmd_dictionary[1]
dropdown_cmd_list = []
for key, value in cmd_list.items():
    if(value.cmd_sendable == 1):
        dropdown_cmd_list.append(value.cmd_description)

#Creates a dropdown menu for command options
ttk.Label(test_tab, text="Choose Command:", padding=3).grid(column=0,row=0,sticky=W)
test_command = StringVar(test_tab)
test_combobox = ttk.Combobox(test_tab,textvariable=test_command,values=dropdown_cmd_list,state=(["readonly"]))
test_combobox.grid(column=2,row=0)

#Creates an input box
ttk.Label(test_tab, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
test_entry = ttk.Entry(test_tab, textvariable=packet_input)
test_entry.grid(column=1,row=2,columnspan=3, sticky=EW)

#Disables input box if a command has not been selected from the dropdown menu
test_entry.state(['disabled'])
def set_button_state(var,index,mode):
    if test_command.get() == 0:
        test_entry.state(['disabled'])
    else:
        test_entry.state(['!disabled'])
test_command.trace_add("write", set_button_state)

#When the user selects a command in the combobox, looks for ID of selected command in the command manifest
def get_dropdown_selection():
    for key, value in cmd_list.items():
        if(value.cmd_description == test_command.get()):
            value.cmd_id = key
            #Returns command id for selected command
            return value.cmd_id
        
#Retrieves data from input box and selection from combobox
def get_input():
    print(packet_input.get())
    #Command id from dropdown selection will be used to call a specific command
    print(get_dropdown_selection())

#Button to send packet (for testing)
send_custom_btn = ttk.Button(test_tab, text="Send Entry", command=get_input)
send_custom_btn.grid(column=2,row=3,sticky=E)

#If nothing has been entered, disables the "Send Entry" button
#Updates any time the user changes the text in the entry box
send_custom_btn.state(['disabled'])
def set_button_state(var,index,mode):
    if len(packet_input.get()) == 0:
        send_custom_btn.state(['disabled'])
    else:
        send_custom_btn.state(['!disabled'])
packet_input.trace_add("write", set_button_state)


######################################################################################################################
#OBC Tab (currently used for testing buttons)

#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")

def req_packet():
    print("Packet Request Button Test")

#Adds OBC tab to interface
tab_interface.add(obc_tab, text='  OBC  ')
send_packet_btn = ttk.Button(obc_tab, text="Send Packet", command=send_packet, padding=5).grid(column=0,row=0)
req_packet_btn = ttk.Button(obc_tab, text="Request Packet", command=req_packet, padding=5).grid(column=1,row=0)

######################################################################################################################
#More tabs (commands will be added later)

tab_interface.add(adcs_tab, text='  ADCS  ')
tab_interface.add(sdr_tab, text='  SDR  ')
tab_interface.add(eps_tab, text='  EPS  ')
tab_interface.add(uhf_tab, text='  UHF  ')

root.mainloop()