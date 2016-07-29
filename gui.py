from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from ass import *
import main
import os
import json

# print(variableName)

def calculate(*args):
	finalfile = main.x[0].split('.')[0] + '.8085'
	str1 = ''
	str1 = str1 + 'Interpreting...........\nRunning Assembler \n'
	meters.set(str1)
	main.runass()
	str1 = str1 + 'Assembler Completed \n' + 'Running Linker \n'
	meters.set(str1)
	main.runlin()
	str1 = str1 + 'Linker Completed \n' + 'Running Loader \n'
	meters.set(str1)
	main.runload()
	str1 = str1 + 'Loading Complete \n' + '\t\tFile is ready to simulate.\n' + '\t\tFile name is : ' + finalfile + '\n'
	meters.set(str1)

def askopenfilename(*args):
	# get filename
	filename = filedialog.askopenfilename()
	# open file on your own
	if filename:
		inputFile = open(filename,"r")
		code = inputFile.read()
		lines = code.split('\n')
		finalfile = lines[0].split('.')[0] + '.8085'
		print (lines[0].split('.')[0])
		print (finalfile)
		main.x = []
		for line in lines:
			if line != '':
				main.x.append(line)

		print(main.x[0])

def opensimulator(*args):
	finalfile = main.x[0].split('.')[0] + '.8085'
	os.system('python3 sim.py '+finalfile+" " +str(variablename))

def pass1():
	for pass1File in main.x:
		print(pass1File)
		fileName = pass1File.split('.')[0]+'.l'
		top = Toplevel()
		top.minsize(666, 666)
		top.title(fileName)
		readFile = open(fileName).read()
		if readFile:
			message = readFile
		else:
			message = "File does not exist."
		msg = Message(top, text=message).grid(column=1, row=1, sticky=W)

def pass2():
	for pass2File in main.x:
		fileName = pass2File.split('.')[0]+'.li'
		top = Toplevel()
		top.minsize(666, 666)
		top.title(fileName)
		readFile = open(fileName).read()
		if readFile:
			message = readFile
		else:
			message = "File does not exist."
		msg = Message(top, text=message).grid(column=1, row=1, sticky=W)


def symbolTable():
	message = ""
	for pass1File in main.x:
		print(pass1File)
		fileName = pass1File.split('.')[0]
		message += "Symbol Table for " + fileName.strip() +"\n\n"
		for key,value in symTable[fileName].items():
			message += str(key) + " : " + value + "\n"

	top = Toplevel()
	top.minsize(666, 666)
	top.title("Symbol Table")
	msg = Message(top, text=message).grid(column=1, row=1, sticky=W)

def globalTable():
	message = ""
	for pass1File in main.x:
		print(pass1File)
		fileName = pass1File.split('.')[0]
		message += "Global Table for " + fileName.strip() +"\n\n"
		for key,value in globTable[fileName].items():
			message += str(key) + " : " + value + "\n"

	top = Toplevel()
	top.minsize(666, 666)
	top.title("Global Table")
	msg = Message(top, text=message).grid(column=1, row=1, sticky=W)

root = Tk()
root.title("Assembler Linker Loader")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


feet = StringVar()
meters = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
ttk.Button(mainframe, text="Open File", command=askopenfilename).grid(column=2, row=1, sticky=(W, E))


ttk.Button(mainframe, text="Symbol Table", command=symbolTable).grid(column=3, row=1, sticky=(W))
ttk.Button(mainframe, text="Global Table", command=globalTable).grid(column=6, row=1, sticky=(W))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe,text="Pass1 Files" ,command=pass1).grid(column=2, row=3, sticky=W)
ttk.Button(mainframe,text="Pass2 Files" ,command=pass2).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="Run", command=calculate).grid(column=2, row=4, sticky=W)
ttk.Button(mainframe, text="Simulate", command=opensimulator).grid(column=3, row=4, sticky=W)

for child in mainframe.winfo_children(): 
	child.grid_configure(padx=25, pady=25)

root.bind('<Return>', calculate)

root.mainloop()
