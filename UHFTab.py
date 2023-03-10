from tkinter import *
from tkinter import ttk
import importlib
from TypeCommand import TypeCommand
from TypeCommand import create_TypeCommand

#Imports commands from CySatGlobal
global_module = importlib.import_module('CySatGlobal')
cmd_dictionary = global_module.cmd_dictionary
sys_dictionary = global_module.sys_dictionary
sys_list = global_module.sys_list

global_module.populate_global_variables()

#Makes command list for specifically UHF commands
uhf_cmd_list = cmd_dictionary[5]

#Makes an array of command descriptions for UHF dropdown menu
def get_uhf_commands():
    uhf_dropdown_cmds = []
    for key, value in uhf_cmd_list.items():
        if(value.cmd_sendable == 1):
            uhf_dropdown_cmds.append(value.cmd_description)
    return(uhf_dropdown_cmds)
    
uhf_dropdown_cmds = get_uhf_commands()

#Creates uhf tab
class uhf_Tab(ttk.Frame):

    def __init__(self, root):
        
        super(uhf_Tab, self).__init__(padding=5)
        self.root = root

        #Adds main label to user interface
        uhf_label = ttk.Label(self, text="UHF Command Selection", padding=3, font=('Consolas',12,'bold'))
        uhf_label.grid(column=0,row=0,columnspan=3)

        ttk.Label(self, text="Choose Command:", padding=3).grid(column=0,row=1,sticky=W)
        uhf_command = StringVar(self)
        uhf_packet_input = StringVar(self)
        uhf_combobox = ttk.Combobox(self, textvariable=uhf_command, values=uhf_dropdown_cmds, state='readonly', width=46)
        uhf_combobox.grid(column=2,row=1)

        #-------------------------------------------------------------------#
        #DROPDOWN COMMAND MENU
        #Creates a dropdown menu for command options
        #Uses command list for the selected subsystem
        
        #When the user selects a command in the combobox, looks for ID of selected command in the command manifest
        def get_dropdown_selection():
            for key, value in uhf_cmd_list.items():
                if(value.cmd_description == uhf_command.get()):
                    value.cmd_id = key
                    #Returns command id for selected command
                    return value.cmd_id

        #Checks if selected command (indicated by cmd_id) has a payload
        #Used to enable/disable input box
        def command_has_payload():
            cmd = uhf_cmd_list[get_dropdown_selection()]
            if cmd.cmd_has_payload == 1:
                return TRUE
            else:
                return FALSE

        #-------------------------------------------------------------------#
        #INPUT BOX
        #Creates an input box
        ttk.Label(self, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
        uhf_entry = ttk.Entry(self, textvariable=uhf_packet_input)
        uhf_entry.grid(column=1,row=2,columnspan=3, sticky=EW)

        #Disables input box if a command has not been selected from the dropdown menu
        #OR disables input box if the command does not have a data payload
        uhf_entry.state(['disabled'])
        def set_entry_state(var,index,mode):
            if uhf_command.get() == 0 or command_has_payload():
                uhf_entry.delete(0,END)
                uhf_entry.state(['disabled'])
            else:
                uhf_entry.state(['!disabled'])
        uhf_command.trace_add("write", set_entry_state)

        #Retrieves data from input box and selection from combobox
        def get_uhf_input():
            #Command id from dropdown selection will be used to call a specific command
            input = create_TypeCommand(5,get_dropdown_selection())
            print("System ID: " + str(input.sys_id))
            print("Command ID: " + str(input.cmd_id))

            #Erases input
            uhf_entry.delete(0,END)

        #-------------------------------------------------------------------#
        #SEND COMMAND BUTTON
        #Button to send packet
        send_custom_btn = ttk.Button(self, text="Send Command", command=get_uhf_input)
        send_custom_btn.grid(column=2,row=3,sticky=E)

        #Disables the "Send Command" button:
        #   If nothing has been entered
        #   If the selected command does not allow the user to enter custom packet data
        #Updates any time the user changes the text in the entry box
        send_custom_btn.state(['disabled'])
        def set_button_state(var,index,mode):
            if len(uhf_packet_input.get()) == 0:
                if command_has_payload():
                    send_custom_btn.state(['!disabled'])
                else:
                    send_custom_btn.state(['disabled'])
            else:
                send_custom_btn.state(['!disabled'])
        uhf_command.trace_add("write", set_button_state)
        uhf_packet_input.trace_add("write", set_button_state)