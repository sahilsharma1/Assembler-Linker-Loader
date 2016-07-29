from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys
from ass import *
import json
import main

# Registers

# General Purpose

# print(sys.argv[1:])

reg = {}
reg['A'] = 0
reg['B'] = 0
reg['C'] = 0
reg['D'] = 0
reg['E'] = 0
reg['F'] = 0
reg['G'] = 0
reg['H'] = 0
reg['PC'] = 0
# Special Function

reg['SP'] = 0
PC = 0
stack = []

oplen = {}
dbloc = []

def calculatelen():
	inputFile = open('lenopcodes.cf',"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		line = line.lstrip().rstrip()
		if line != '' :
			oplen[line.split(' ')[0]] = int(line.split(' ')[1])

calculatelen()
memory = {}

def load(filename):
	inputFile = open(filename,"r")
	code = inputFile.read()
	lines = code.split('\n')
	mem = 0
	for line in lines :
		op = line.split(' ')[0].lstrip().rstrip()
		if op != 'DB':
			memory[mem] = line
			mem += oplen[op]
		else:
			memory[mem] = int(line.split(' ')[1].lstrip().rstrip())
			dbloc.append(mem)
			mem += 1

def simulator(pc = 0):
	inst = memory[pc]
	opcode = inst.split(' ')[0]
	print ('Current Instruction : ' + str(memory[pc]))
	curinst.set(str(memory[pc]))
	print ('Register Values' )
	print ('A : ' + str(reg['A']))
	rega.set(str(reg['A']))
	print ('B : ' + str(reg['B']))
	regb.set(str(reg['B']))
	print ('C : ' + str(reg['C']))
	regc.set(str(reg['C']))
	print ('D : ' + str(reg['D']))
	regd.set(str(reg['D']))
	print ('E : ' + str(reg['E']))
	rege.set(str(reg['E']))
	print ('F : ' + str(reg['F']))
	regf.set(str(reg['F']))
	print ('G : ' + str(reg['G']))
	regg.set(str(reg['G']))
	print ('H : ' + str(reg['H']))
	regh.set(str(reg['H']))
	print ('Variable Memory Locations')
	memlocs = ''
	for db in dbloc:
		memlocs += (str(db) + ' : ' + str(memory[db]) + '\n')
	memstr.set(memlocs)
	print (memlocs)
	# raw_input("Press Enter to continue...")
	if opcode == 'HLT':
		progcompleted.set('DONE')
		return False
	elif opcode == 'JMP':
		nextinst = int(inst.split(' ')[1])
		PC = nextinst
		print (nextinst)
		print (PC)
	elif opcode == 'MVI':
		regvar = inst.split(' ')[1].split(',')[0].lstrip().rstrip()
		reg[regvar] = int(inst.split(' ')[1].split(',')[1].lstrip().rstrip())
		PC = pc + int(oplen[opcode])
	elif opcode == 'ADI':
		reg['A'] = int(reg['A']) + int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])
	elif opcode == 'STA':
		memloc = int(inst.split(' ')[1])
		memory[memloc] = int(reg['A'])
		PC = pc + int(oplen[opcode])
	elif opcode == 'LDA':
		memloc = int(inst.split(' ')[1])
		reg['A'] = int(memory[memloc])
		PC = pc + int(oplen[opcode])
	elif opcode == 'MOV':
		destreg = inst.split(' ')[1].split(',')[0].lstrip().rstrip()
		srcreg = inst.split(' ')[1].split(',')[1].lstrip().rstrip()
		reg[destreg] = reg[srcreg]
		PC = pc + int(oplen[opcode])
	elif opcode == 'ADD':
		srcreg = inst.split(' ')[1]
		reg['A'] = int(reg['A']) + int(reg[srcreg])
		PC = pc + int(oplen[opcode])
	elif opcode == 'SUI':
		reg['A'] = int(reg['A']) - int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])
	elif opcode == 'SUB':
		srcreg = inst.split(' ')[1]
		reg['A'] = int(reg['A']) - int(reg[srcreg])
		PC = pc + int(oplen[opcode])
	elif opcode == 'ANI':
		reg['A'] = int(reg['A']) & int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])
	elif opcode == 'ANA':
		srcreg = inst.split(' ')[1]
		reg['A'] = int(reg['A']) & int(reg[srcreg])
		PC = pc + int(oplen[opcode])
	elif opcode == 'ORI':
		reg['A'] = int(reg['A']) | int(inst.split(' ')[1])
		PC = pc + int(oplen[opcode])
	elif opcode == 'ORA':
		srcreg = inst.split(' ')[1]
		reg['A'] = int(reg['A']) | int(reg[srcreg])
		PC = pc + int(oplen[opcode])
	elif opcode == 'PUSH':
		srcreg = inst.split(' ')[1]
		stack.append(int(reg[srcreg]))
		PC = pc + int(oplen[opcode])
	elif opcode == 'POP':
		srcreg = inst.split(' ')[1]
		reg[srcreg] = stack.pop()
		PC = pc + int(oplen[opcode])
	elif opcode == 'JNZ':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) != 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JZ':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) == 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JP':
		# print('hello!')
		nextinst = int(inst.split(' ')[1])

		# print('\n' + reg['A'])
		if int(reg['A']) > 0:
			# print('hi!')
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	elif opcode == 'JM':
		nextinst = int(inst.split(' ')[1])
		if int(reg['A']) < 0:
			PC = nextinst
		else:
			PC = pc + int(oplen[opcode])
	reg['PC'] = PC
	return True

def result():
	x = True
	while(x):
		x = simulator(int(reg['PC']))

def callbackf():
	simulator(int(reg['PC']))

#######
# Gui #
#######
def askopenfilename(*args):
	# get filename
	filename = filedialog.askopenfilename()
	load(filename)

def openexist(*args):
	# get filename
	filename = sys.argv[1]
	load(filename)

root = Tk()
root.title("Simulator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

curinst = StringVar()
rega = StringVar()
regb = StringVar()
regc = StringVar()
regd = StringVar()
rege = StringVar()
regf = StringVar()
regg = StringVar()
regh = StringVar()
memstr = StringVar()
meters = StringVar()
progcompleted = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
ttk.Button(mainframe, text="Load", command=openexist).grid(column=1, row=1, sticky=(W, E))
ttk.Button(mainframe, text="Open Another File", command=askopenfilename).grid(column=2, row=1, sticky=(W))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Run", command=callbackf).grid(column=3, row=1, sticky=W)
ttk.Button(mainframe, text="Result", command=result).grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Current Instruction").grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=curinst).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Register Values").grid(column=1, row=4, sticky=(W, E))
ttk.Label(mainframe, text="A").grid(column=1, row=5, sticky=(W, E))
ttk.Label(mainframe, textvariable=rega).grid(column=2, row=5, sticky=(W, E))
ttk.Label(mainframe, text="B").grid(column=1, row=6, sticky=(W, E))
ttk.Label(mainframe, textvariable=regb).grid(column=2, row=6, sticky=(W, E))
ttk.Label(mainframe, text="C").grid(column=1, row=7, sticky=(W, E))
ttk.Label(mainframe, textvariable=regc).grid(column=2, row=7, sticky=(W, E))
ttk.Label(mainframe, text="D").grid(column=1, row=8, sticky=(W, E))
ttk.Label(mainframe, textvariable=regd).grid(column=2, row=8, sticky=(W, E))
ttk.Label(mainframe, text="E").grid(column=1, row=9, sticky=(W, E))
ttk.Label(mainframe, textvariable=rege).grid(column=2, row=9, sticky=(W, E))
ttk.Label(mainframe, text="F").grid(column=1, row=10, sticky=(W, E))
ttk.Label(mainframe, textvariable=regf).grid(column=2, row=10, sticky=(W, E))
ttk.Label(mainframe, text="G").grid(column=1, row=11, sticky=(W, E))
ttk.Label(mainframe, textvariable=regg).grid(column=2, row=11, sticky=(W, E))
ttk.Label(mainframe, text="H").grid(column=1, row=12, sticky=(W, E))
ttk.Label(mainframe, textvariable=regh).grid(column=2, row=12, sticky=(W, E))
ttk.Label(mainframe, text="Memory Locations").grid(column=1, row=13, sticky=(W, E))
ttk.Label(mainframe, textvariable=memstr).grid(column=2, row=13, sticky=(W, E))
ttk.Label(mainframe, textvariable=progcompleted).grid(column=2, row=14, sticky=(W, E))

# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
root.bind('<Return>', simulator)

root.mainloop()