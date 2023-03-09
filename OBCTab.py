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

#Makes command list for specifically OBC commands
obc_cmd_list = cmd_dictionary[1]

#Makes an array of command descriptions for OBC dropdown menu
def get_obc_commands():
    obc_dropdown_cmds = []
    for key, value in obc_cmd_list.items():
        if(value.cmd_sendable == 1):
            obc_dropdown_cmds.append(value.cmd_description)
    return(obc_dropdown_cmds)
    
obc_dropdown_cmds = get_obc_commands()

#Creates obc tab
class obc_Tab(ttk.Frame):

    def __init__(self, root):
        
        super(obc_Tab, self).__init__(padding=5)
        self.root = root

        #Adds main label to user interface
        obc_label = ttk.Label(self, text="OBC Command Selection", padding=3, font=('Consolas',12,'bold'))
        obc_label.grid(column=0,row=0,columnspan=3)

        ttk.Label(self, text="Choose Command:", padding=3).grid(column=0,row=1,sticky=W)
        obc_command = StringVar(self)
        obc_packet_input = StringVar(self)
        obc_combobox = ttk.Combobox(self, textvariable=obc_command, values=obc_dropdown_cmds, state='readonly', width=46)
        obc_combobox.grid(column=2,row=1)

        #-------------------------------------------------------------------#
        #DROPDOWN COMMAND MENU
        #Creates a dropdown menu for command options
        #Uses command list for the selected subsystem
        
        #When the user selects a command in the combobox, looks for ID of selected command in the command manifest
        def get_dropdown_selection():
            for key, value in obc_cmd_list.items():
                if(value.cmd_description == obc_command.get()):
                    value.cmd_id = key
                    #Returns command id for selected command
                    return value.cmd_id

        #Checks if selected command (indicated by cmd_id) has a payload
        #Used to enable/disable input box
        def command_has_payload():
            cmd = obc_cmd_list[get_dropdown_selection()]
            if cmd.cmd_has_payload == 1:
                return TRUE
            else:
                return FALSE

        #-------------------------------------------------------------------#
        #INPUT BOX
        #Creates an input box
        ttk.Label(self, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
        obc_entry = ttk.Entry(self, textvariable=obc_packet_input)
        obc_entry.grid(column=1,row=2,columnspan=3, sticky=EW)

        #Disables input box if a command has not been selected from the dropdown menu
        #OR disables input box if the command does not have a data payload
        obc_entry.state(['disabled'])
        def set_entry_state(var,index,mode):
            if obc_command.get() == 0 or command_has_payload():
                obc_entry.delete(0,END)
                obc_entry.state(['disabled'])
            else:
                obc_entry.state(['!disabled'])
        obc_command.trace_add("write", set_entry_state)

        #Retrieves data from input box and selection from combobox
        def get_obc_input():
            #Command id from dropdown selection will be used to call a specific command
            input = create_TypeCommand(1,get_dropdown_selection())
            print("System ID: " + str(input.sys_id))
            print("Command ID: " + str(input.cmd_id))

            #Erases input
            obc_entry.delete(0,END)

        #-------------------------------------------------------------------#
        #SEND ENTRY BUTTON
        #Button to send packet (for testing)
        send_custom_btn = ttk.Button(self, text="Send Entry", command=get_obc_input)
        send_custom_btn.grid(column=2,row=3,sticky=E)

        #Disables the "Send Entry" button:
        #   If nothing has been entered
        #   If the selected command does not allow the user to enter custom packet data
        #Updates any time the user changes the text in the entry box
        send_custom_btn.state(['disabled'])
        def set_button_state(var,index,mode):
            if len(obc_packet_input.get()) == 0:
                if command_has_payload():
                    send_custom_btn.state(['!disabled'])
                else:
                    send_custom_btn.state(['disabled'])
            else:
                send_custom_btn.state(['!disabled'])
        obc_command.trace_add("write", set_button_state)
        obc_packet_input.trace_add("write", set_button_state)