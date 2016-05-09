# Picrust SOP
This article details the standard operating procedures for our picrust pipeline


## Usage:
### picrust_pipeline.py  

```
usage: picrust_pipeline.py [-h] -i INPUT [-x XTON] [-t THREADS]
                           [-m {uclust,usearch,sortmerna}]

Create a picrust SOP shell script

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The filtered.fna file
  -x XTON, -xton XTON   the number less than or equal to how many times to see
                        a sequence before filtering. i.e. singletons are <= 1,
                        therefore -x == 1 DEFAULT=1
  -t THREADS, --threads THREADS
                        Threads to use
  -m {uclust,usearch,sortmerna}, --method {uclust,usearch,sortmerna}
                        OTU Picking Method: Valid choices are sortmerna,
                        usearch61, and uclust
```


## Workflow

### Remove Singletons
`xton_remover.py -i filtered.fna -x 1 -o xton_1_filtered.fna`

### Remove Chimeras
`vsearch --uchime_ref xton_1_filtered.fna --db /media/nfs_opt/bin/gold.fa --nonchimeras nonchimeric_xton_1_filtered.fna`

### Pick OTUs
`pick_closed_reference_otus.py -i nonchimeric_xton_1_filtered.fna -o . -f -a -O 8 -p pick_closed_reference_otus_uclust.params`



## Workflow

### Remove Singletons
`xton_remover.py`

### Remove Chimeras

###
