import tkinter as tk
import tkinter.ttk as ttk
from turtle import window_width

columnOrHeader = True

window = tk.Tk()
for i in range(3):
    window.columnconfigure(i,weight=1,minsize=75)
    window.rowconfigure(i,weight=1,minsize=75)
    for j in range(3):
        frame = tk.Frame(master=window,relief=tk.RAISED,borderwidth=1)
        frame.grid(row=i,column=j,padx=100,pady=100)

uploadButton = ttk.Button(
    text="Upload"
    )
uploadButton.grid(column=2,row=1)

startTrainingButton = ttk.Button(text="Start Training")
startTrainingButton.grid(column=0,row=1)

topBar = ttk.Frame(window,height=50,bg="blue")
topBar.pack(fill=tk.X,side=tk.TOP)
columnCheck = ttk.Checkbutton(master=window,text="Column Training",variable=columnOrHeader,onvalue=1,offvalue=0)
headerCheck = ttk.Checkbutton(master=window,text="Header Training",variable=columnOrHeader,onvalue=0,offvalue=1)
testExistingButton = ttk.Button(text="Test Existing Model")
testSREOsButton = ttk.Button(text="Test SREOs")
columnCheck.grid(column=0,row=0,sticky="n")
headerCheck.grid(column=1,row=0,sticky="nw")
testExistingButton.grid(column=2,row=0,sticky="n")
testSREOsButton.grid(colum=2,row=0)

def flipColumnHeaderCheck():
    global columnOrHeader
    columnOrHeader = not columnOrHeader
    columnCheck.invoke()
    headerCheck.invoke()

columnCheck.command = flipColumnHeaderCheck()
headerCheck.command = flipColumnHeaderCheck()

window.mainloop()