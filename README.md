## Scripts
Repository contains various bioinformatics scripts
___

### `Pull_coordinates.py`
Dependencies: `Python 2.7`, `Biopython-1.60`

Pulls a range of sites for sequences in a fasta file. Both coordinate template and fasta file must contain sequences with equivalent headers (e.g., Sequence "Drosophila_TRAF6" must appear in both files).
Program works with reverse coordinates (e.g., 501->204)

**Usage:**

Inputs
1. Coordinate_template (`*.tsv`)
2. Fasta file (`*.fasta`)

Output
1. `*.regions_extracted.fasta`

**Coordinate_template format example:**
```
Drosophila_TRAF6 1 250
Human_TRAF6 5 353
etc...
```
___

### `Best_fit_domains.py`
Dependencies: `Python3`

Parses the domain-table output format (`--domtblout`) from [`HMMER`](http://hmmer.org/) and outputs only the best (according to full-sequence E-value) non-overlapping domains for each annotated polypeptide sequence and outputs filtered domain-table output as a tab-delimited file of 23 fields (fields correspond to the same fields in the original `domtblout` file).

**Usage:**

Inputs
1. Domain-table file (`*.domtblout`)

Output
1. Filtered domain table (`*.besthits.tsv`)

___
### `Domain_svgwrite.py`
Domain architecture diagram generator under development.
More to come.
