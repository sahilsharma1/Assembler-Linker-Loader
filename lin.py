import ass

symTable = ass.symTable
globTable = ass.globTable
filelen = ass.filelen
externtable = {}
finalsymTable = {}

def getLoc(exter, fileNames):
	for fileName in fileNames:
		fileName = fileName.split('.')[0]
		for vari in globTable[fileName]:
			print(vari)
			if vari == exter:
				val = symTable[fileName][vari]
				val = val.split('#')[1]
				return (fileName,val)

def linker( fileNames ):
	startCount = {}
	lastcount = 0
	for fileName in fileNames:
		startCount[fileName.split('.')[0]] = lastcount
		lastcount += filelen[fileName.split('.')[0]]
	for fileName in fileNames :
		fileName = fileName.split('.')[0]
		inputFile = open(fileName+'.li','r')
		code = inputFile.read()
		lines = code.split('\n')
		outFile = open(fileName+'.loaded','w')
		newCode = []
		for line in lines :
			line = line.lstrip().rstrip()
			if '$' in line:
				exter = line.split(' ')[1].split('$')[1]
				x, y = getLoc(exter, fileNames)
				newLine = line.replace('$'+exter, '@' + str(int(startCount[x]+int(y))))
				newCode.append(newLine)
			else:
				newCode.append(line)

		outFile.write('\n'.join(newCode))
		outFile.close()

	outFile = open(fileNames[0].split('.')[0]+'.ls','w')
	linkCode = []
	progCount = 0
	for fileName in fileNames :
		fileName = fileName.split('.')[0]
		inputFile = open(fileName+'.loaded','r')
		code = inputFile.read()
		lines = code.split('\n')
		for line in lines :
			line = line.lstrip().rstrip()
			if '#' in line:
				tag = line.split(' ')[1]
				newtag = '#' + str((int(tag.split('#')[1]) + startCount[fileName]))
				linkCode.append(line.replace(tag, newtag))
			elif '@' in line:
				newtag = line.replace('@','#')
				linkCode.append(newtag)
			else:
				linkCode.append(line)
	outFile.write('\n'.join(linkCode))
	outFile.close()