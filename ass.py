import re

oplen = {}
symTable = {}
globTable = {}
filelen = {}
variablename = {}
def isvariable(line):
	var = re.compile(r'var (.+*)=(.+*)')

def calculatelen():
	inputFile = open('lenopcodes.cf',"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		line = line.lstrip().rstrip()
		if line != '' :
			oplen[line.split(' ')[0]] = int(line.split(' ')[1])

def tryInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def test( fileNames ):
	calculatelen()
	glo = re.compile(r'glob var (.*)=(.*)')
	ext = re.compile(r'extern(.*)')
	var = re.compile(r'var (.*)=(.*)')
	maxi = re.compile(r'(.+)=max(.+)\,(.+)')
	add = re.compile(r'(.+)=(.+)\+(.+)')
	addadd = re.compile(r'(.+)=(.+)\+(.+)\+(.+)')
	addsub = re.compile(r'(.+)=(.+)\+(.+)\-(.+)')
	subadd = re.compile(r'(.+)=(.+)\-(.+)\+(.+)')
	subsub = re.compile(r'(.+)=(.+)\-(.+)\-(.+)')
	addeq = re.compile(r'(.+)\+=(.+)')
	subeq = re.compile(r'(.+)\-=(.+)')
	mul = re.compile(r'(.+)=(.+)\*(.+)')
	sub = re.compile(r'(.+)=(.+)\-(.+)')
	ana = re.compile(r'(.+)=(.+)\&(.+)')
	ora = re.compile(r'(.+)=(.+)\|(.+)')
	slop = re.compile(r'loop(.+)')
	elop = re.compile(r'endloop(.*)')
	ifgt = re.compile(r'if (.*)>(.*)')
	ifge = re.compile(r'if (.*)>=(.*)')
	ifgte = re.compile(r'endif(.*)')
	ifeq = re.compile(r'if (.*)==(.*)')
	for fileName in fileNames :
		inputFile = open(fileName, "r")
		fileName = fileName.split('.')[0]
		outFile = open(fileName+'.l','w')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		memaddr = 0
		loopctr = 0
		ifctr = 0
		ifjmp = {}
		symTable[fileName] = {}
		globTable[fileName] = {}
		for line in lines :
			line = line.lstrip().rstrip()
			if addeq.match(line):
				x=addeq.match(line).group(1).lstrip().rstrip()
				y=addeq.match(line).group(2).lstrip().rstrip()
				if tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][x]))
					newCode.append('ADI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][x]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif subeq.match(line):
				x=subeq.match(line).group(1).lstrip().rstrip()
				y=subeq.match(line).group(2).lstrip().rstrip()
				if tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][x]))
					newCode.append('SUI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][x]))
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif maxi.match(line):
				x = maxi.match(line).group(1).lstrip().rstrip()
				y = maxi.match(line).group(2).lstrip().rstrip()
				z = maxi.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					newCode.append('JP &&&'+str(ifctr))
					newCode.append('JZ &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
					memaddr += oplen['JP']
					memaddr += oplen['JZ']
					newCode.append('MVI A,'+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					newCode.append('MVI A,-1')
					memaddr += oplen['MVI']
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
					newCode.append('JM &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['JM']
					newCode.append('MVI A,'+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
				elif tryInt(y) and not tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('SUB B')
					newCode.append('JP &&&'+str(ifctr))
					newCode.append('JZ &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['MVI']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['JP']
					memaddr += oplen['JZ']
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('STA '+str(symTable[fileName][x]))
					newCode.append('MVI A,-1')
					memaddr += oplen['LDA']
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
					newCode.append('JM &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['JM']
					newCode.append('MVI A,'+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
				elif not tryInt(y) and tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					# newCode.append('MOV B,A')
					# newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('SUI '+z)
					newCode.append('JP &&&'+str(ifctr))
					newCode.append('JZ &&&'+str(ifctr))
					ifctr += 1
					# memaddr += oplen['MVI']
					# memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['JP']
					memaddr += oplen['JZ']
					newCode.append('MVI A,'+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					newCode.append('MVI A,-1')
					memaddr += oplen['MVI']
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
					newCode.append('JM &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['JM']
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['STA']
					memaddr += oplen['LDA']
					ifjmp[ifctr-1] = memaddr
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUB B')
					newCode.append('JP &&&'+str(ifctr))
					newCode.append('JZ &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['JP']
					memaddr += oplen['JZ']
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('STA '+str(symTable[fileName][x]))
					newCode.append('MVI A,-1')
					memaddr += oplen['LDA']
					memaddr += oplen['STA']
					memaddr += oplen['MVI']
					ifjmp[ifctr-1] = memaddr
					newCode.append('JM &&&'+str(ifctr))
					ifctr += 1
					memaddr += oplen['JM']
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['STA']
					memaddr += oplen['LDA']
					ifjmp[ifctr-1] = memaddr
			elif var.match(line):
				symTable[fileName][var.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				variablename[str(memaddr + 3)] = str(var.match(line).group(1).lstrip().rstrip())
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+var.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif glo.match(line):
				variablename[str(memaddr + 3)] = str(glo.match(line).group(1).lstrip().rstrip())
				symTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				globTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+glo.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif ext.match(line):
				symTable[fileName][ext.match(line).group(1).lstrip().rstrip()] = '$'+str(ext.match(line).group(1).lstrip().rstrip())


			elif addadd.match(line):
				x = addadd.match(line).group(1).lstrip().rstrip()
				y = addadd.match(line).group(2).lstrip().rstrip()
				z = addadd.match(line).group(3).lstrip().rstrip()
				w = addadd.match(line).group(4).lstrip().rstrip() 
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ADI '+z)
					memaddr += oplen['MVI']
					memaddr += oplen['ADI']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADI '+y)
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADI '+z)
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADD B')
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
				if tryInt(w):
					newCode.append('ADI '+w)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(w):
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][w]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif addsub.match(line):
				x = addsub.match(line).group(1).lstrip().rstrip()
				y = addsub.match(line).group(2).lstrip().rstrip()
				z = addsub.match(line).group(3).lstrip().rstrip()
				w = addsub.match(line).group(4).lstrip().rstrip() 
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ADI '+z)
					memaddr += oplen['MVI']
					memaddr += oplen['ADI']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADI '+y)
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADI '+z)
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADD B')
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
				if tryInt(w):
					newCode.append('SUI '+w)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(w):
					newCode.append('MOV C,A')
					newCode.append('LDA '+str(symTable[fileName][w]))
					newCode.append('MOV B,A')
					newCode.append('MOV A,C')
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['MOV']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif subadd.match(line):
				x = subadd.match(line).group(1).lstrip().rstrip()
				y = subadd.match(line).group(2).lstrip().rstrip()
				z = subadd.match(line).group(3).lstrip().rstrip()
				w = subadd.match(line).group(4).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+y)
					newCode.append('SUI '+str(symTable[fileName][z]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUI '+z)
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUB B')
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
				if tryInt(w):
					newCode.append('ADI '+w)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(w):
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][w]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif subsub.match(line):
				x = subsub.match(line).group(1).lstrip().rstrip()
				y = subsub.match(line).group(2).lstrip().rstrip()
				z = subsub.match(line).group(3).lstrip().rstrip()
				w = subsub.match(line).group(4).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+y)
					newCode.append('SUI '+str(symTable[fileName][z]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUI '+z)
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUB B')
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
				if tryInt(w):
					newCode.append('SUI '+w)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(w):
					newCode.append('MOV C,A')
					newCode.append('LDA '+str(symTable[fileName][w]))
					newCode.append('MOV B,A')
					newCode.append('MOV A,C')
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['MOV']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif add.match(line):
				x = add.match(line).group(1).lstrip().rstrip()
				y = add.match(line).group(2).lstrip().rstrip()
				z = add.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif mul.match(line):
				x = mul.match(line).group(1).lstrip().rstrip()
				y = mul.match(line).group(2).lstrip().rstrip()
				z = mul.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					k = int(z)
					while k>1 :
						newCode.append('ADI '+y)
						k=k-1
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					k=int(z)
					while k > 1:
						memaddr += oplen['ADI']
						k=k-1
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					k = int(y)
					while k > 1:
						newCode.append('LDA '+str(symTable[fileName][z]))
						newCode.append('ADD B')
						newCode.append('MOV B,A')
						k=k-1
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					k=int(y)
					while k > 1:
						memaddr += oplen['LDA']
						memaddr += oplen['ADD']
						memaddr += oplen['MOV']
						k=k-1
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					k=int(z)
					while k >1:
						newCode.append('LDA '+str(symTable[fileName][y]))
						newCode.append('ADD B')
						newCode.append('MOV B,A')
						k=k-1
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					k=int(z)
					while k > 1:
						memaddr += oplen['LDA']
						memaddr += oplen['ADD']
						memaddr += oplen['MOV']
						k=k-1
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					# newCode.append('LDA '+str(symTable[fileName][y]))
					# newCode.append('MOV B,A')
					# k = int(str(symTable[fileName][z])[1:])
					newCode.append('LDA '+str(symTable[fileName][z]))
					memaddr += oplen['LDA']
					# memaddr += oplen['MOV']
					# memaddr += oplen['LDA']
					# newCode.append('PUSH D')
					newCode.append('MOV F,A')
					newCode.append('MVI B,0')
					memaddr += oplen['MVI']
					memaddr += oplen['MOV']
					symTable[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1
					
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADD B')
					newCode.append('MOV B,A')
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['MOV']
					
					newCode.append('MOV A,F')
					newCode.append('SUI 1')
					newCode.append('MOV F,A')
					newCode.append('JNZ '+str(symTable[fileName][loopctr-1]))
					# newCode.append('POP D')
					loopctr -= 1
					memaddr += oplen['MOV']
					memaddr += oplen['SUI']
					memaddr += oplen['MOV']
					memaddr += oplen['JNZ']
					# memaddr += oplen['POP']
					newCode.append('MOV A,B')
					newCode.append('STA '+str(symTable[fileName][x]))
					
					#memaddr += oplen['ADD']
					memaddr += oplen['MOV']
					memaddr += oplen['STA']
			elif sub.match(line):
				x = sub.match(line).group(1).lstrip().rstrip()
				y = sub.match(line).group(2).lstrip().rstrip()
				z = sub.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+y)
					newCode.append('SUI '+str(symTable[fileName][z]))
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif ana.match(line):
				x = ana.match(line).group(1).lstrip().rstrip()
				y = ana.match(line).group(2).lstrip().rstrip()
				z = ana.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANA B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ANA']
					memaddr += oplen['STA']
			elif ora.match(line):
				x = ora.match(line).group(1).lstrip().rstrip()
				y = ora.match(line).group(2).lstrip().rstrip()
				z = ora.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORA B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ORA']
					memaddr += oplen['STA']
			elif slop.match(line):
				x = slop.match(line).group(1).lstrip().rstrip()
				if tryInt(x):
					newCode.append('PUSH D')
					newCode.append('MVI E,'+x)
					memaddr += oplen['PUSH']
					memaddr += oplen['MVI']
					symTable[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1
				else:
					newCode.append('PUSH D')
					newCode.append('LDA '+str(symTable[fileName][x]))
					newCode.append('MOV E,A')
					memaddr += oplen['PUSH']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					symTable[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1
			elif elop.match(line):
				newCode.append('MOV A,E')
				newCode.append('SUI 1')
				newCode.append('MOV E,A')
				newCode.append('JNZ '+str(symTable[fileName][loopctr-1]))
				newCode.append('POP D')
				loopctr -= 1
				memaddr += oplen['MOV']
				memaddr += oplen['SUI']
				memaddr += oplen['MOV']
				memaddr += oplen['JNZ']
				memaddr += oplen['POP']
			elif ifgt.match(line):
				x = ifgt.match(line).group(1).lstrip().rstrip()
				y = ifgt.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JP &&&'+str(ifctr))
				newCode.append('JZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JP']
				memaddr += oplen['JZ']
			elif ifge.match(line):
				x = ifgt.match(line).group(1).lstrip().rstrip()
				y = ifgt.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JP &&&'+str(ifctr))
				ifctr += 1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JP']
			elif ifeq.match(line):
				x = ifeq.match(line).group(1).lstrip().rstrip()
				y = ifeq.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JNZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JNZ']
			elif ifgte.match(line):
				ifjmp[ifctr-1] = memaddr
			
		outFile.write('\n'.join(newCode))
		outFile.close()
		filelen[fileName] = memaddr
		################################
		inputFile = open(fileName+'.l','r')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		for line in lines :
			if '&&&' in line:
				tag = line.split(' ')[1]
				linenum = tag.split('&&&')[1].lstrip().rstrip()
				linenum = int(linenum)
				newtag = '#'+str(ifjmp[linenum])
				newCode.append(line.replace(tag, newtag))
			else:
				newCode.append(line)
		outFile = open(fileName+'.li','w')
		outFile.write('\n'.join(newCode))
		outFile.close()
		print(variablename)