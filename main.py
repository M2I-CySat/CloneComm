from tkinter import *
from tkinter import ttk

#Use struct to send data (packets)?

#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")

def req_packet():
    print("Packet Request Button Test")

#Initializes textvariables for dropdown menus
test_command = "Choose command..."
obc_command = "Choose command..."
adcs_command = "Choose command..."
sdr_command = "Choose command..."
eps_command = "Choose command..."
uhf_command = "Choose command..."

#Creates the main application window
root = Tk()
root.title("CloneComms")
mainframe = ttk.Frame(root, padding=5)
ttk.Label(mainframe, text="CySat Commands", font="TkHeadingFont").grid(row=0, column=0, columnspan=3)

#Organizes widgets inside the main window
mainframe.grid(row=0, column=0)

#Creates tabs for each subsystem

#NOT YET IMPLEMENTED:
#Each subsystem will have a dropdown menu of command options
#A text input box will be available if manual input is required for a command

tab_interface = ttk.Notebook(mainframe, padding=5)
tab_interface.grid(row=1,column=1,rowspan=3,sticky=NSEW)

test_tab = ttk.Frame(tab_interface)
obc_tab = ttk.Frame(tab_interface)
adcs_tab = ttk.Frame(tab_interface)
sdr_tab = ttk.Frame(tab_interface)
eps_tab = ttk.Frame(tab_interface)
uhf_tab = ttk.Frame(tab_interface)

tab_interface.add(test_tab, text='Test Commands')

#Creates a dropdown menu for command options

test_combobox = ttk.Combobox(test_tab,textvariable=test_command,values=['Test 1','Test 2'])
test_combobox.grid(column=1,row=0)
ttk.Label(test_tab, text="Choose Command:", padding=5).grid(column=0,row=0)

#Button to send packet (for testing)
send_packet_btn = ttk.Button(test_tab, text="Send Packet", command=send_packet, padding=5)
send_packet_btn.grid(column=1,row=2)

#Button to request a packet (for testing)
req_packet_btn = ttk.Button(test_tab, text="Request Packet", command=req_packet, padding=5)
req_packet_btn.grid(column=0,row=2)

tab_interface.add(obc_tab, text='OBC Commands')
tab_interface.add(adcs_tab, text='ADCS Commands')
tab_interface.add(sdr_tab, text='SDR Commands')
tab_interface.add(eps_tab, text='EPS Commands')
tab_interface.add(uhf_tab, text='UHF Commands')

root.mainloop()