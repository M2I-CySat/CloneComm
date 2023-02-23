from tkinter import *
from tkinter import ttk

#Commands for basic packet-sending testing
def send_packet():
    print("Packet Send Button Test")

def req_packet():
    print("Packet Request Button Test")

root = Tk()
root.title("CloneComms")

mainframe = ttk.Frame(root, padding=5)
titlelbl = ttk.Label(mainframe, text="Commands")
send_packet_btn = ttk.Button(mainframe, text="Send Packet", command=send_packet)
req_packet_btn = ttk.Button(mainframe, text="Request Packet", command=req_packet)

mainframe.grid(column=0,row=0)
titlelbl.grid(row=0, column=0)
send_packet_btn.grid(row=1, column=0)
req_packet_btn.grid(row=2, column=0)

root.mainloop()