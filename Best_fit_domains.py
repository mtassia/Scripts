#!/bin/python3
import re
import sys

#ATOM-SPECIFIC BLOCK FOR BUILDING CODE:
#import os
#print(os.getcwd())
DOMTBLOUT=open("Hsapiens_genome_proteins_RHIM_Pfam_model.Present.Pfam.domtblout", 'r') #REMOVE THIS FOR FINAL VERSION; REINITIALIZE THE VARIABLE OPTION ON LINE 11
#######################################

#DOMTBLOUT=open(sys.argv[1], 'r') #First argument is the domain-table output from HMMEr
ANNOTATION_LIST=[] #Initiates the list that will be filled as DOMTBLOUT is read and indexed in block below

#Following for-loop reads, line-by-line, DOMTBLOUT and loads it into ANNOTATION_LIST after proper indexing
for LINE in DOMTBLOUT:

	#Remove header and footer of domtblout file
	SPLIT_LINE=LINE.split() #Convert read string to a list object
	if SPLIT_LINE[0][0] == "#": #If line starts with #, skip it
		continue

	#Load data-content lines of DOMTBLOUT into a 22-field list object (ANNOTATION_LIST)
	else:
		DOMTBL_LINE=re.split(r'\s+', LINE.rstrip())	#Initiates an object where fields 0-21 are as designated by HMMers domtblout and 22- are the final field(s)
		DESCRIPTION="" #Initiates a variable to create a single string corresponding to the 'description of target' column in the domtblout format
		for INDEX in range(22, len(DOMTBL_LINE)): #Indicies between 22: correspond to an improperly formated 'description of target' which needs to be converted to a single list index
			DESCRIPTION+=DOMTBL_LINE[INDEX]+" " #Import the 22: indices into a single string
		del DOMTBL_LINE[22:] #Remove the improperly formatted indices from DOMTBL_LINE
		DOMTBL_LINE.append(DESCRIPTION.rstrip()) #Replace the removed indices with the properly formatted index

		ANNOTATION_LIST.append(DOMTBL_LINE) #After cleaning datalines, append to this variable. ANNOTATION_LIST will be a list-of-lists where each primary index is a line from the DOMTBLOUT
DOMTBLOUT.close()

BEST_HIT_LINES=[] #Create a new list that will contain only the best hits for each query
PREVIOUS_QUERY=[] #Creates a list variable that will be used to compare lines as ANNOTATION_LIST is read

#For-loop will loop through ANNOTATION, per line from DOMTBLOUT. Each loop will load a 22-field list object into QUERY
for QUERY in ANNOTATION_LIST:

	#If reading first data line or reading a line describing a new sequence from the previous line, following block will build a range list according to the sequence's length to build best domain-architecture where no two domains can overlap (i.e., best-hit domains only kept per sequence)
	if (PREVIOUS_QUERY == []) or (PREVIOUS_QUERY[3] != QUERY[3]): #If previous query doesn't exist (i.e., first iteration of loop) or line pertains to a new sequence from the previous line, do the following...
		BEST_HIT_LINES.append(QUERY) #Line necessarily contains a 'best-hit' domain as DOMTBLOUT is organized in decreasing order of high-quality hits. Therefore, load line into the BEST_HIT_LINES list object
		QUERY_LENGTH_RANGE=list(range(int(QUERY[5]))) #Create a list that contains a range of length equal to the lenght of the sequence (e.g., if sequence length is 500, list will include integers from 0-499)
		DOMAIN_RANGE=list(range(int(QUERY[19]),int(QUERY[20]))) #Create a list object that contains a range that starts at environmental start of domain and ends at environmental end of domain

		#For-loop will remove values from QUERY_LENGTH_RANGE for every value present in DOMAIN_RANGE. In this way, no two domains can overlap per sequence being annotated.
		for RESIDUE in DOMAIN_RANGE:
			if RESIDUE in QUERY_LENGTH_RANGE:
				QUERY_LENGTH_RANGE.remove(RESIDUE)

#SANITY CHECK##############################
		print(QUERY[3],QUERY_LENGTH_RANGE)
		print(QUERY[0],DOMAIN_RANGE)
###########################################

		PREVIOUS_QUERY=QUERY #Load current line into the PREVIOUS_QUERY variable for future comparison

	else: # FIX THIS BLOCK WHICH INTENDS TO, FOR EVERY NON-OVERLAPPING DOMAIN, REMOVE IT'S RANGE FROM THE RANGE OF THE CURRENT QUERY
		DOMAIN_RANGE=list(range(int(QUERY[19]),int(QUERY[20]))) #Load coordinate range where domain in line is present

		#Block checks for the following annotation problems with the currently loaded domain: Start overlap with previous, better hit; Stop overlap; Current domain encompasses previous, better hit. If any of these errors occur, better domain already annotated in region and currently loaded domain should be skipped.
		if DOMAIN_RANGE[0] not in QUERY_LENGTH_RANGE:
			print(QUERY[0], "start overlaps a previous domain")
			continue
		elif DOMAIN_RANGE[-1] not in QUERY_LENGTH_RANGE:
			print(QUERY[0], "end overlaps a previous domain")
			continue
		elif DOMAIN_RANGE[int(len(DOMAIN_RANGE)/2)] not in QUERY_LENGTH_RANGE:
			print(QUERY[0], "encompasses a previous domain")
			continue

#SANITY CHECK##############################
#		print(QUERY[3],QUERY_LENGTH_RANGE)
#		print(QUERY[0],DOMAIN_RANGE)
###########################################

		#If domain does not overlap with a previously analyzed domain, then remove this region from the QUERY_LENGTH_RANGE and add line to BEST_HIT_LINES
		else:
			for RESIDUE in DOMAIN_RANGE:
				if RESIDUE in QUERY_LENGTH_RANGE:
					QUERY_LENGTH_RANGE.remove(RESIDUE)
			BEST_HIT_LINES.append(QUERY) #Add domain to BEST_HIT_LINES variable
			PREVIOUS_QUERY=QUERY

#SANITY CHECK##############################
#		print(QUERY[3],QUERY_LENGTH_RANGE)
#		print(QUERY[0],DOMAIN_RANGE)
###########################################

#Write BEST_HIT_LINES to a file as a tsv
#FILE_OUTPUT_NAME=sys.argv[1]+".besthits.tsv"
FILE_OUTPUT=open(("tmp_test"+".besthits.tsv"),'w') #Replace this line with the above line for final implementation
for LINE in BEST_HIT_LINES:
#	print('\t'.join(map(str,LINE))+"\n")
	FILE_OUTPUT.write('\t'.join(map(str,LINE))+"\n")
