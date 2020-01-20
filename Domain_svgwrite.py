#This code is entirely experimental and is being developed to accelerate domain diagram creation
#Initial module import and directory setup
import svgwrite

#Creating variables that will be needed to be imported from HMMer domain_table, will be changed to be an import function
ANNOTATION_LIST=[["SEQ1",300,"DOMAIN_1",50,150],["SEQ1",300,"DOMAIN_2",200,268],["SEQ100200300400500",400,"DOMAIN_1",20,80],["SEQ100200300400500",400,"DOMAIN_2",81,204],["SEQ100200300400500",400,"DOMAIN_200",290,399]] #Simulates a best_hit_domains.py output
SEQUENCE_IDS=[] #Create a list of unique sequence IDs such that number of indices in this list is the number of annotated sequences
SEQUENCE_LENGTHS=[] #Create a list
SEQLEN_DICT={}

for i in ANNOTATION_LIST: #Obtain basic sequence information
    if i[0] not in SEQUENCE_IDS:
            SEQUENCE_IDS.append(i[0]) # Add new sequence ID to list
            SEQLEN_DICT[str(i[0])]=int(i[1]) #Create a dictionary pair between new sequence ID and it's associated length
    if i[1] not in SEQUENCE_LENGTHS:
            SEQUENCE_LENGTHS.append(i[1]) #Create a list of sequence lengths to be used to format the svg document size

SEQUENCE_LENGTHS.sort(reverse=True) #Sort sequence lengths in descending order to find the longest sequence length
LONGEST_SEQ=SEQUENCE_LENGTHS[0] #Use the longest sequence to generate the width of the svg canvas
NUM_SEQS=len(SEQUENCE_IDS) #Use the number of sequences to generate the length of the svg canvas
LONGEST_ID_LEN=len(max(SEQUENCE_IDS, key=len)) #Create an integer variable which contains the length of the longest string - this is to be used to appropriately format the width of the canvas.
LINE_SCAFFOLD_START=(LONGEST_ID_LEN*10)+5

print(LONGEST_SEQ) #Variable sanity check - CAN DELETE
print(NUM_SEQS) #Variable sanity check - CAN DELETE
print(LONGEST_ID_LEN) #Variable sanity check - CAN DELETE
print(LINE_SCAFFOLD_START) #Variable sanity check - CAN DELETE

#CREATE CANVAS
svgdoc=svgwrite.Drawing(
    filename="test_drawing.svg",
    size = (((LONGEST_ID_LEN*10)+LONGEST_SEQ+5),NUM_SEQS*30)) #At size 10 arial bold, the W glyph is 9.43px -- therefor the x for scaffold size is loaded as a function of (longest length sequence name * 10) + (length of longest sequence). Y scaffold size is loaded as the number of sequences * 30 (15 above and below scaffold line) for appropriate spacing. Final 5 accounts for the spacing between text and the line object.

#SEQLEN_DICT[SEQUENCE_IDS[0]] #HERE FOR TESTING PURPOSES ONLY - CAN DELETE
#print(SEQLEN_DICT) #HERE FOR TESTING PURPOSES ONLY - CAN DELETE

#Create TEXT AND LINE-SCAFFOLD PER SEQUENCE
for SEQi in range(len(SEQLEN_DICT)): #Iterate numerically through a series of numbers equal to the number of unique sequence
    svgdoc.add(svgdoc.text( #Create the text for the sequence scaffold
        str(SEQUENCE_IDS[SEQi]), #Load text
        insert=((LONGEST_ID_LEN*10),((SEQi*30)+15)), #Place cursor
        stroke='none', #No stroke on text
        fill=svgwrite.rgb(0,0,0), #Write letters in black with no stroke
        alignment_baseline="middle", #Positioning baseline is set to the middle of the written text
        text_anchor='end', #Text is written so that the last character is 5 pixels from the start of the line scaffold (below)
        font_size='10px',
        font_weight='bold',
        font_family='Arial'
    ))
    svgdoc.add(svgdoc.line( #Create the line for the sequence scaffold
        start=(LINE_SCAFFOLD_START,((SEQi*30)+15)), #Start of the line scaffold is equal to the LONGEST_ID_LEN * 10 + 5
        end=((LINE_SCAFFOLD_START)+SEQLEN_DICT[SEQUENCE_IDS[SEQi]],((SEQi*30)+15)),
        stroke='black',
        stroke_width='1px'
    ))

#Iterate through annotations per sequence to make domain overlays
COUNT=0 #Create a count variable which will help with y-axis formatting as the annotations are looped
for ID in SEQUENCE_IDS: #Loop through a list of the sequence IDs
    for ANNOTATION in ANNOTATION_LIST: #Loop through entries in the annotation list
            if ID == ANNOTATION[0]: #If the annotation line corresponds to the sequence in the list of sequences being iterated above, do the following
                DOMAIN_NAME=ANNOTATION[2] #Load the domain name
                DOMAIN_START=ANNOTATION[3] #Load the start coordinate for the domain
                DOMAIN_END=ANNOTATION[4] #Load the end coordinate for the domain
                DOMAIN_MIDPOINT=(LINE_SCAFFOLD_START+((DOMAIN_START+DOMAIN_END)/2)) #Create a variable with the X coordinate of the domain shape midpoint
                svgdoc.add(svgdoc.rect( #Create a rectangle overlaying the line that corresponds to each domain
                    insert=((LINE_SCAFFOLD_START+DOMAIN_START),((COUNT*30)+7.5)),
                    size=(((DOMAIN_END)-(DOMAIN_START)),15),
                    rx=2, #Make rectangles with rounded edges
                    fill="white",
                    stroke="black",
                    stroke_width="1px"
                ))
                svgdoc.add(svgdoc.text( #Create the lable for the domain ID within the domain shape
                    str(DOMAIN_NAME), #Load domain name text
                    insert=((DOMAIN_MIDPOINT),((COUNT*30)+15)), #Place cursor
                    stroke='none', #No stroke on text
                    fill=svgwrite.rgb(0,0,0), #Write letters in black with no stroke
                    alignment_baseline="middle", #Positioning baseline is set to the middle of the written text
                    text_anchor='middle', #Text is written from the middle position
                    font_size='6px',
                    font_weight='bold',
                    font_family='Arial'
                ))
    COUNT+=1

#Save Drawing
svgdoc.saveas("test_drawing.svg")
