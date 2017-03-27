#!/usr/bin/python
#Runs using BioPython and Python2.7
#Argument1 = Renaming template, Argument2 = Fasta file

from Bio import SeqIO
from Bio.Alphabet import IUPAC
import sys

#Obtain sequences headers and coordinates for extraction
COORD_FILE=open(sys.argv[1], 'r')
COORDINATE_LIST=[]
for COORD_LINE in COORD_FILE:
	SPLIT_LINE=COORD_LINE.split()
	count = 0
	TMP_LIST=[]
	for i in range(len(SPLIT_LINE)):
		if count == 0:
			TMP_LIST.append(SPLIT_LINE[i])
			count += 1
		elif count > 0:
			TMP_LIST.append(int(SPLIT_LINE[i]))
			count += 1
	COORDINATE_LIST.append(TMP_LIST)
COORD_FILE.close()

#Print a helpful message
NUM_COORD=len(COORDINATE_LIST)
print NUM_COORD,'coordinates have been entered.\n'

#For each sequence in fasta file, find matching coordinate data
COUNT=0
CUT_SEQ_RECORDS=[]
for SEQUENCE in SeqIO.parse(sys.argv[2],'fasta',IUPAC.ambiguous_dna):
	SEQ_NAME=SEQUENCE.id
	for COORDINATE in COORDINATE_LIST:
		if COORDINATE[0] == SEQ_NAME:
			print 'Processing',SEQ_NAME
			RECORD="REC"+str(COUNT)
			START=COORDINATE[1]-1
			STOP=COORDINATE[2]-1
			CUT_SEQ_RECORDS.append(SEQUENCE[START:STOP])
			COUNT+=1
print 'Total number of sequences processed:',COUNT

#Write output file
FILE_ID=sys.argv[2].split(".")
NEW_FILE_NAME=FILE_ID[0]+".regions_extracted.fasta"
SeqIO.write(CUT_SEQ_RECORDS,NEW_FILE_NAME,"fasta")
