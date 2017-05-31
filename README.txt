# Scripts
Useful scripts for molecular data manipulation

---------------------------------------------
Pull_coordinates.py
Dependencies: Python 2.7, Biopython-1.60
Pulls a range of sites for sequences in a fasta file. Both coordinate template and fasta file must contain sequences with equivalent headers (e.g., Sequence "Drosophila_TRAF6" must appear in both files).
Program works with reverse coordinates (e.g., 501->204)
Usage:

Inputs 
1. Coordinate_template 
2. Fasta file

Coordinate_template format example
#ID START STOP
Drosophila_TRAF6 1 250
Human_TRAF6 5 353
etc...
---------------------------------------------



