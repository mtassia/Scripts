#This code is entirely experimental and is being developed to accelerate domain diagram creation
#Initial module import and directory setup
import svgwrite

#Creating variables that will be needed to be imported from HMMer domain_table
ANNOTATION_LIST=[["SEQ1",300,"DOMAIN_1",50,150],["SEQ1",300,"DOMAIN_2",200,268],["SEQ2",400,"DOMAIN_1",20,80],["SEQ2",400,"DOMAIN_2",81,204],["SEQ2",400,"DOMAIN_2",290,399]]
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

#CREATE CANVAS
svgdoc=svgwrite.Drawing(
    filename="test_drawing.svg",
    size = (LONGEST_SEQ+55,NUM_SEQS*30))

SEQLEN_DICT[SEQUENCE_IDS[0]]
#Create TEXT AND LINE-SCAFFOLD PER SEQUENCE
for SEQi in range(len(SEQLEN_DICT)):
    svgdoc.add(svgdoc.text(
        str(SEQUENCE_IDS[SEQi]),
        insert=(0,((SEQi*30)+15)),
        stroke='none',
        fill=svgwrite.rgb(0,0,0),
        textLength='50px',
        font_size='10px',
        font_weight='bold',
        font_family='Arial'
    ))
    svgdoc.add(svgdoc.line(
        start=(55,((SEQi*30)+15)),
        end=(SEQLEN_DICT[SEQUENCE_IDS[SEQi]],((SEQi*30)+15)),
        stroke='black',
        stroke_width='1px'
    ))

#Save Drawing
svgdoc.save()
