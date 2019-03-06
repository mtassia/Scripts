#!/bin/python3
import re
import sys

DOMTBLOUT=open(sys.argv[1], 'r')
ANNOTATION_LIST=[] #Initiates the list that will ultimately be sorted for finding best-fit domain annotation
for LINE in DOMTBLOUT: #Loops through a domtblout file from hmmer
	#Remove header and footer of domtblout file
	SPLIT_LINE=LINE.split() #Convert string to a list
	if SPLIT_LINE[0][0] == "#": #Removes lines starting with '#'
		continue
	else: #For the remaining lines in the file, import them as a list of 22 fields with headers specified in HMMers domain table format
		DOMTBL_LINE=re.split(r'\s+', LINE.rstrip())	#Initiates an object where fields 0-21 are as designated by HMMers domtblout and 22- are the final 
		DESCRIPTION="" #Initiates a variable to create a string corresponding to the 'description of target' column in the domtblout format
		for INDEX in range(22, len(DOMTBL_LINE)): #Indicies between 22:-1 correspond to an improperly formated 'description of target' which needs to be converted to a single list index
			DESCRIPTION+=DOMTBL_LINE[INDEX]+" " #Import the above indices into a single string
		del DOMTBL_LINE[22:] #Remove the improperly formatted indices
		DOMTBL_LINE.append(DESCRIPTION.rstrip()) #Add the correctly formatted string
		
		ANNOTATION_LIST.append(DOMTBL_LINE)
DOMTBLOUT.close()

BEST_HIT_LINES=[] #Create a new list that contains only the best hits for each query
PREVIOUS_QUERY=[]
for QUERY in ANNOTATION_LIST:
	
	if (PREVIOUS_QUERY == []) or (PREVIOUS_QUERY[3] != QUERY[3]): #If reading first line of file or reading new query data, loop
		BEST_HIT_LINES.append(QUERY)
		QUERY_LENGTH_RANGE=range(int(QUERY[5])) #If first occurance of query, load length into a range list. This list will be used to exclude overlap for each domain hit on query. Final value of length is equal to query length-1 for python reasons
		DOMAIN_RANGE=range(int(QUERY[19]),int(QUERY[20])) #Load coordinate range where domain in line is present
		
		for RESIDUE in DOMAIN_RANGE: #Check to see if current domain overlaps previous domain found present in query length
			if RESIDUE in QUERY_LENGTH_RANGE:
				QUERY_LENGTH_RANGE.remove(RESIDUE)
				
		print(QUERY[3],QUERY_LENGTH_RANGE)
		print(QUERY[0],DOMAIN_RANGE)
		
		PREVIOUS_QUERY=QUERY

	else: # FIX THIS BLOCK WHICH INTENDS TO, FOR EVERY NON-OVERLAPPING DOMAIN, REMOVE IT'S RANGE FROM THE RANGE OF THE CURRENT QUERY
		DOMAIN_RANGE=range(int(QUERY[19]),int(QUERY[20])) #Load coordinate range where domain in line is present
		
		if DOMAIN_RANGE[0] not in QUERY_LENGTH_RANGE:
			continue
		elif DOMAIN_RANGE[-1] not in QUERY_LENGTH_RANGE:
			continue
		else:
			
	
		#for RESIDUE in DOMAIN_RANGE:
		#	if RESIDUE in TEMP_QUERY_LENGTH_RANGE:
                #                QUERY_LENGTH_RANGE.remove(RESIDUE)
		#	if RESIDUE not in TEMP_QUERY_LENGTH_RANGE:
		#		continue
		#	else:

			PREVIOUS_QUERY=QUERY
			continue		

		#print(QUERY[0],DOMAIN_RANGE[0],DOMAIN_RANGE[-1])
		
		PREVIOUS_QUERY=QUERY
