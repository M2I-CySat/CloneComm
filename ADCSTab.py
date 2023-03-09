from tkinter import *
from tkinter import ttk
import importlib

#Creates a new Command class which includes system ID
#Mostly for simulating how a CySat packet will be created (likely to be removed later)
class TypeCommand:
    def __init__(self, sys_id, cmd_id):
        self.sys_id = sys_id
        self.cmd_id = cmd_id

def create_TypeCommand(sys_id, cmd_id):
    sending_cmd = TypeCommand(sys_id, cmd_id)
    return sending_cmd

#Imports commands from CySatGlobal
global_module = importlib.import_module('CySatGlobal')
cmd_dictionary = global_module.cmd_dictionary
sys_dictionary = global_module.sys_dictionary
sys_list = global_module.sys_list

global_module.populate_global_variables()

#Makes command list for specifically ADCS commands
adcs_cmd_list = cmd_dictionary[2]

#Makes an array of command descriptions for ADCS dropdown menu
def get_adcs_commands():
        adcs_dropdown_cmds = []
        for key, value in adcs_cmd_list.items():
            if(value.cmd_sendable == 1):
                adcs_dropdown_cmds.append(value.cmd_description)
        return(adcs_dropdown_cmds)
    
adcs_dropdown_cmds = get_adcs_commands()

#Creates ADCS tab
class adcs_Tab(ttk.Frame):

    def __init__(self, root):
        super(adcs_Tab, self).__init__()
        self.root = root

        ttk.Label(self, text="Choose Command:", padding=3).grid(column=0,row=0,sticky=W)
        adcs_command = StringVar(self)
        adcs_packet_input = StringVar(self)
        adcs_combobox = ttk.Combobox(self, textvariable=adcs_command, values=adcs_dropdown_cmds)
        adcs_combobox.grid(column=2,row=0)

        #When the user selects a command in the combobox, looks for ID of selected command in the command manifest
        def get_dropdown_selection():
            for key, value in adcs_cmd_list.items():
                if(value.cmd_description == adcs_command.get()):
                    value.cmd_id = key
                    #Returns command id for selected command
                    return value.cmd_id

        #Checks if selected command (indicated by cmd_id) has a payload
        #Used to enable/disable input box
        def command_has_payload():
            cmd = adcs_cmd_list[get_dropdown_selection()]
            if cmd.cmd_has_payload == 1:
                return TRUE
            else:
                return FALSE

        #-------------------------------------------------------------------#
        #INPUT BOX
        #Creates an input box
        ttk.Label(self, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
        test_entry = ttk.Entry(self, textvariable=adcs_packet_input)
        test_entry.grid(column=1,row=2,columnspan=3, sticky=EW)

        #Disables input box if a command has not been selected from the dropdown menu
        #OR disables input box if the command does not have a data payload
        test_entry.state(['disabled'])
        def set_entry_state(var,index,mode):
            if adcs_command.get() == 0 or command_has_payload():
                test_entry.delete(0,END)
                test_entry.state(['disabled'])
            else:
                test_entry.state(['!disabled'])
        adcs_command.trace_add("write", set_entry_state)

        #Retrieves data from input box and selection from combobox
        def get_adcs_input():
            #Command id from dropdown selection will be used to call a specific command
            input = create_TypeCommand(2,get_dropdown_selection())
            print("System ID: " + str(input.sys_id))
            print("Command ID: " + str(input.cmd_id))

        #-------------------------------------------------------------------#
        #SEND ENTRY BUTTON
        #Button to send packet (for testing)
        send_custom_btn = ttk.Button(self, text="Send Entry", command=get_adcs_input)
        send_custom_btn.grid(column=2,row=3,sticky=E)

        #Disables the "Send Entry" button:
        #   If nothing has been entered
        #   If the selected command does not allow the user to enter custom packet data
        #Updates any time the user changes the text in the entry box
        send_custom_btn.state(['disabled'])
        def set_button_state(var,index,mode):
            if len(adcs_packet_input.get()) == 0:
                if command_has_payload():
                    send_custom_btn.state(['!disabled'])
                else:
                    send_custom_btn.state(['disabled'])
            else:
                send_custom_btn.state(['!disabled'])
        adcs_command.trace_add("write", set_button_state)
        adcs_packet_input.trace_add("write", set_button_state)