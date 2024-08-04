#!/usr/bin/env python3

# parse BLASTP and blat results to transform Y1000 gene IDs into YGOB gene ids using identical matching
# doing some magic to deal with the fact that some proteins are identical across species and
# the DB we are searching from YGOB is not split up by species

import csv
import os

pairings = {}
YGOB_folder = 'v7-Aug2012'
namepairing = 'Y1000_to_YGOB_filepairings.csv'
with open(namepairing, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        # strip the '.pep' off the end
        speciesname = ".".join(row[0].split('.')[:-1])
        pairings[speciesname] = set()
        with open(os.path.join(YGOB_folder,row[1]), 'r') as f:
            reader2 = csv.reader(f, delimiter="\t")
            for gnrow in reader2:
                name = gnrow[0]
                pairings[speciesname].add(name)
                
if not os.path.exists('id_lookup'):
    os.mkdir('id_lookup')
table = {}
for file in os.listdir('results'):
    if file.endswith('.tab'):
        prefix = ".".join(file.split('.')[0:-2])
        type = file.split('.')[-2]
        if prefix not in table:
            table[prefix] = {}
        with open('results/' + file, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            for row in reader:
                # print(row)
                pid = row[2]
                q = row[0]
                subj = row[1]
                
                if prefix in pairings and subj in pairings[prefix]:
                    if q not in table[prefix]:
                        table[prefix][q] = {}
                    # take first hit arbitrarily now
                    if type not in table[prefix][q]:
                        table[prefix][q][type] = [subj, pid]

for prefix in table:
    with open(f'id_lookup/{prefix}__Y1000_to_YGOB_IDs.tsv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Y1000_ID', 'YGOB_ID', 
                        'BLASTP_Subject', 'BLASTP_Percent_id',
                        'BLAT_Subject', 'BLAT_Percent_id'])
        for q in sorted(table[prefix]):
            outrow = [q]
            for type in ('BLASTP', 'blat'):
                if type in table[prefix][q]:
                    outrow.extend( [ table[prefix][q][type][0], table[prefix][q][type][1] ])
                else:
                    outrow.extend( [ '', '' ] )
            writer.writerow(outrow)