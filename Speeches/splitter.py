# Transcript Splitter

import sys

def splitFile(fname):
	f = open(fname, 'r')

	for line in f:
		speaker = re.match(r'(^[A-Z]+:)',line)
		if speaker: print speaker

def main():
	splitFile(sys.argv[1])



main()
