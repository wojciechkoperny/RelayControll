import tkinter as tk
from tkinter import Label, messagebox
import sys, ftd2xx as ftdi
from typing import Text

isBoardPowerUp = 3
isDebuggerPowerUp = 3
statusPin = 0

USED_PINS = 0x03

def ft_read(d, nbytes):
    s = d.read(nbytes)
    return [ord(c) for c in s] if type(s) is str else list(s)

def update_board_power_text():
    global isBoardPowerUp
    global statusPin
    if isBoardPowerUp == 1:
        isBoardPowerUp = 0
        board_power_text.set(str("POWER DOWN "+ lines[1]))
        board_label_text.set(str(lines[1]+" is powered up"))
        labelBoard.config(bg="green")
        statusPin[0]=statusPin[0] | (1<<0)
        print("ON Board", statusPin[0])
        #lowbits = value & mask
        d.write(str(statusPin[0]&USED_PINS))
        #d.write(str(255))
    elif isBoardPowerUp == 0 :
        isBoardPowerUp = 1
        board_power_text.set(str("POWER  UP "+lines[1]))
        board_label_text.set(str(lines[1]+ " is powered down"))
        labelBoard.config(bg="red")
        statusPin[0]=statusPin[0] & ~(1<<0)
        print("OFF board", statusPin[0])
        d.write(str(statusPin[0]&USED_PINS))
        #d.write(str(0))
    else :
        board_power_text.set("UNDEFINED STATE")


def update_debug_power_text():

    global isDebuggerPowerUp
    global statusPin
    if isDebuggerPowerUp == 1:
        isDebuggerPowerUp = 0
        debug_power_text.set(str("POWER DOWN "+ lines[2]))
        statusPin[0]=statusPin[0] | (1<<1)
        print("ON debug", str(statusPin[0]&USED_PINS))
        debugger_label_text.set(str(lines[2]+" is powered up"))
        labeldebugger.config(bg="green")
        d.write(str(statusPin[0]&USED_PINS))
    elif isDebuggerPowerUp == 0 :
        isDebuggerPowerUp = 1
        debug_power_text.set(str("POWER  UP "+lines[2]))
        statusPin[0]= statusPin[0] & ~(1<<1)
        print("OFF debug", str(statusPin[0]&USED_PINS))
        debugger_label_text.set(str(lines[2]+" is powered down"))
        labeldebugger.config(bg="red")
        d.write(str(statusPin[0]&USED_PINS))
    else :
        debug_power_text.set(" UNDEFINED STATE")


def on_closing():
    print("zamykam")
    d.close()

window = tk.Tk()

window.title("kontrola przekaźników WK")
window.geometry('400x200') 

#window.protocol("WM_DELETE_WINDOW", on_closing)

f = open('config.cfg','r')

lines = f.readlines()

try:
    d = ftdi.open(int(lines[0]))    # Open first FTDI device
except:
    messagebox.showerror("Connection Info", "No FTDI device found. Set device number in config.cfg line 1")

d.setBitMode(USED_PINS, 1) 

statusPin = ft_read(d, 1)
print(ft_read(d, 1))

board_power_text = tk.StringVar() 
board_power_state = tk.Button(window, textvariable=board_power_text,  command=update_board_power_text)

debug_power_text = tk.StringVar()
debug_power_state = tk.Button(window, textvariable=debug_power_text,  command=update_debug_power_text)

#label = Label(frame, textvariable = var, background="red" )
board_label_text = tk.StringVar()
labelBoard = tk.Label(window,textvariable = board_label_text)

debugger_label_text = tk.StringVar()
labeldebugger= tk.Label(window,textvariable = debugger_label_text)

#statusPin = b'T'
if statusPin[0] & 0x01:
    isBoardPowerUp = 0
    board_label_text.set(str(lines[1] + " is powered up"))
    labelBoard.config(bg="green")
    board_power_text.set(str("POWER DOWN " + lines[1]))
else :
    isBoardPowerUp = 1
    board_label_text.set(str(lines[1] +" is powered down"))
    labelBoard.config(bg="red")
    board_power_text.set(str("POWER UP " + lines[1]))

if statusPin[0] & 0x02:
    isDebuggerPowerUp = 0
    debugger_label_text.set(str(lines[2]+" is powered up"))
    labeldebugger.config(bg="green")
    debug_power_text.set(str("POWER DOWN "+ lines[2]))

else :
    isDebuggerPowerUp = 1
    debugger_label_text.set(str(lines[2]+" is powered down"))
    labeldebugger.config(bg="red")
    debug_power_text.set(str("POWER UP "+ lines[2]))


board_power_state.pack()
debug_power_state.pack()
labelBoard.pack()
labeldebugger.pack()

messagebox.showinfo("Connection Info", d.getDeviceInfo())

window.mainloop()