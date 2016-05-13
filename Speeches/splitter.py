# Transcript Splitter

import sys
import re

def splitFile(fname, cname):
	f = open(fname, 'r')

	ctext = []

	text = ""
	while True:
		line = f.readline()
		if line.startswith(cname.upper() + ':'):
			text += line
			break

	store = True
	for line in f:
		speaker = re.match(r'(^[A-Z]+:)',line)
		if speaker:
			if text != "": ctext.append(text)
			text = ""
			if line.startswith(cname.upper() + ':'):
				store = True
			else: store = False

		if store:
			text += line.strip()

	return ctext

def writeFile(ctext,fname,cname):
	sname = cname.upper() + '.' + fname[0:len(fname)-4] + '.txt'
	f = open(sname, 'w')
	for line in ctext:
		f.write(line + '\n')
	f.close()

def main():
	fname = sys.argv[1]
	cname = sys.argv[2]
	ctext = splitFile(fname, cname)
	writeFile(ctext,fname,cname)

main()
