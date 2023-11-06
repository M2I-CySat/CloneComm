from tkinter import *
from tkinter import ttk
#import serial

#Creates a logger for use within the CloneComm interface
#It will display any packets sent and received

class CySatLog(Text):

    #Prints a message (msg) in the logging window
    def writeToLog(self, msg):

        numlines = int(self.index('end - 1 line').split('.')[0])
        self['state'] = 'normal'

        if numlines==24:
            self.delete(1.0, 2.0)
        if self.index('end-1c')!='1.0':
            self.insert('end', '\n')
        self.insert('end', msg)
        self['state'] = 'disabled'

    def sendPacket(self, packet, uart=NONE):
        try:
            print("Packet Sent! (not really)")
        except:
            print("Packet sending failure; connect UART")
