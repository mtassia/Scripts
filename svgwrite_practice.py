#This code is entirely experimental and is being developed to accelerate domain diagram creation
#Initial module import and directory setup
import svgwrite

#Creating variables that will be needed to be imported from HMMer domain_table, will be changed to be an import function
ANNOTATION_LIST=[["SEQ1",300,"DOMAIN_1",50,150],["SEQ1",300,"DOMAIN_2",200,268],["SEQ200",400,"DOMAIN_1",20,80],["SEQ200",400,"DOMAIN_2",81,204],["SEQ200",400,"DOMAIN_200",290,399]]
SEQUENCE_IDS=[]
SEQUENCE_LENGTHS=[]
SEQLEN_DICT={}

for i in ANNOTATION_LIST: #Obtain basic sequence information
    if i[0] not in SEQUENCE_IDS:
            SEQUENCE_IDS.append(i[0])
            SEQLEN_DICT[str(i[0])]=int(i[1])
    if i[1] not in SEQUENCE_LENGTHS:
            SEQUENCE_LENGTHS.append(i[1])

SEQUENCE_LENGTHS.sort(reverse=True) #Sort sequence lengths in descending order to find the longest sequence length
LONGEST_SEQ=SEQUENCE_LENGTHS[0] #Use the longest sequence to generate the width of the svg canvas
NUM_SEQS=len(SEQUENCE_IDS) #Use the number of sequences to generate the length of the svg canvas
LONGEST_ID_LEN=len(max(SEQUENCE_IDS, key=len)) #Create an integer variable which contains the length of the longest string - this is to be used to appropriately format the width of the canvas.

#CREATE CANVAS
svgdoc=svgwrite.Drawing(
    filename="test_drawing.svg",
    size = (((LONGEST_ID_LEN*10)+LONGEST_SEQ),NUM_SEQS*30)) #At size 10 arial bold, the W glyph is 9.43px -- therefor the x for scaffold size is loaded as a function of (longest length sequence name * 10) + (length of longest sequence). Y scaffold size is loaded as the number of sequences * 30 (15 above and below scaffold line) for appropriate spacing.

SEQLEN_DICT[SEQUENCE_IDS[0]] #HERE FOR TESTING PURPOSES ONLY - CAN DELETE
#Create TEXT AND LINE-SCAFFOLD PER SEQUENCE
for SEQi in range(len(SEQLEN_DICT)):
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
        start=(((LONGEST_ID_LEN*10)+5),((SEQi*30)+15)), #Start of the line scaffold is equal to the LONGEST_ID_LEN * 10 + 5
        end=(SEQLEN_DICT[SEQUENCE_IDS[SEQi]],((SEQi*30)+15)),
        stroke='black',
        stroke_width='1px'
    ))

#Save Drawing
svgdoc.saveas("test_drawing.svg")
