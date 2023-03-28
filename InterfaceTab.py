from tkinter import *
from tkinter import ttk
import importlib
from TypeCommand import TypeCommand
from TypeCommand import create_TypeCommand
from CySatPacket import *

#Imports commands from CySatGlobal
global_module = importlib.import_module('CySatGlobal')
cmd_dictionary = global_module.cmd_dictionary
sys_dictionary = global_module.sys_dictionary
sys_list = global_module.sys_list

global_module.populate_global_variables()

#Creates ADCS tab
class InterfaceTab(ttk.Frame):

    def __init__(self, root, subsystem_name, subsystem_no):
        
        super(InterfaceTab, self).__init__(padding=5)
        self.root = root
        self.subsystem_name = subsystem_name
        self.subsystem_no = subsystem_no

        #Makes command list for specifically ADCS commands
        cmd_list = cmd_dictionary[subsystem_no]
        
        #Makes an array of command descriptions for ADCS dropdown menu
        def get_commands():
            dropdown_cmds = []
            for key, value in cmd_list.items():
                if(value.cmd_sendable == 1):
                    dropdown_cmds.append(value.cmd_description)
            return(dropdown_cmds)
            
        dropdown_cmds = get_commands()

        #Adds main label to user interface
        heading = ttk.Label(self, text= subsystem_name + " Command Selection", padding=3, font=('Consolas',12,'bold'))
        heading.grid(column=0,row=0,columnspan=3)

        ttk.Label(self, text="Choose Command:", padding=3).grid(column=0,row=1,sticky=W)
        command = StringVar(self)
        packet_input = StringVar(self)
        combobox = ttk.Combobox(self, textvariable=command, values=dropdown_cmds, state='readonly', width=46)
        combobox.grid(column=2,row=1)

        #-------------------------------------------------------------------#
        #DROPDOWN COMMAND MENU
        #Creates a dropdown menu for command options
        #Uses command list for the selected subsystem

        #When the user selects a command in the combobox, looks for ID of selected command in the command manifest
        def get_dropdown_selection():
            for key, value in cmd_list.items():
                if(value.cmd_description == command.get()):
                    value.cmd_id = key
                    #Returns command id for selected command
                    return value.cmd_id

        #Checks if selected command (indicated by cmd_id) has a payload
        #Used to enable/disable input box
        def command_has_payload():
            cmd = cmd_list[get_dropdown_selection()]
            if cmd.cmd_has_payload == 1:
                return TRUE
            else:
                return FALSE

        #-------------------------------------------------------------------#
        #INPUT BOX
        #Creates an input box
        ttk.Label(self, text="Enter Custom Packet:", padding=3).grid(column=0,row=2)
        input_box = ttk.Entry(self, textvariable=packet_input)
        input_box.grid(column=1,row=2,columnspan=3, sticky=EW)

        #Disables input box if a command has not been selected from the dropdown menu
        #OR disables input box if the command does not have a data payload
        input_box.state(['disabled'])
        def set_entry_state(var,index,mode):
            if command.get() == 0 or command_has_payload():
                input_box.delete(0,END)
                input_box.state(['disabled'])
            else:
                input_box.state(['!disabled'])
        command.trace_add("write", set_entry_state)

        #Retrieves data from input box and selection from combobox
        def get_input():

            input = create_TypeCommand(2,get_dropdown_selection())
            print("System ID: " + str(input.sys_id))
            print("Command ID: " + str(input.cmd_id))

            #Erases input
            input_box.delete(0,END)

            #Specifies sending packet information based on selected subsystem and command
            #Adds data from input box to end of packet (if applicable)
            
                # NOTE: Current error (check CySatPacket)-
                # File "c:\Users\Owner\OneDrive\Documents\GitHub\CloneComms\CySatPacket.py", line 27, in __init__
                #     self.cs = calculate_checksum(sys_id, cmd_id, payload_bytearray)
                # File "c:\Users\Owner\OneDrive\Documents\GitHub\CloneComms\CySatPacket.py", line 37, in calculate_checksum
                #     byte_sum = sys_id + cmd_id
                # TypeError: can only concatenate str (not "int") to str

            # payload = bytearray(packet_input.get(),'utf-8')
            # Psys_id = hex(get_dropdown_selection())
            # Pcmd_id = subsystems_dict[subsystem_name]

            # sending_packet = Packet(Psys_id,Pcmd_id,payload)

            # return(sending_packet)

        #-------------------------------------------------------------------#
        #SEND COMMAND BUTTON
        #Button to send packet
        send_custom_btn = ttk.Button(self, text="Send Command", command=get_input)
        send_custom_btn.grid(column=2,row=3,sticky=E)

        #Disables the "Send Command" button:
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
        command.trace_add("write", set_button_state)
        packet_input.trace_add("write", set_button_state)