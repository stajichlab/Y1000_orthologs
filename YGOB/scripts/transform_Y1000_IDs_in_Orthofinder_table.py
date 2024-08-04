#!/usr/bin/env python3

# read in the post-processed BLASTP and BLAT results
# to update the Orthofinder orthologues file per-species to replace Y1000 gene names with YGBOB names

import csv
import os
import gzip

orthodir = 'Orthologues'
queryfiles = 'query'
lookuptables = 'id_lookup'
results = 'Orthologues_renamed'

if not os.path.exists(results):
    os.mkdir(results)

# read in tables
# going to just use BLASTP values for now
lookup = {}
for lookupfile in os.listdir(lookuptables):
    with open(os.path.join(lookuptables,lookupfile), 'r') as f:
        name = lookupfile.split('__')[0]
        lookup[name] = {}
        reader = csv.reader(f, delimiter="\t")        
        header = next(reader)
        for row in reader:
            lookup[name][row[0]] = row[1]

for species in lookup:
    print(species)
    ogfile = os.path.join(orthodir,f'{species}.tsv.gz')
    if not os.path.exists(ogfile):
        print(f"cannot find {ogfile} in {orthodir}")
        continue
    with gzip.open(ogfile, 'rt') as fh, gzip.open(os.path.join(results,f'{species}.tsv.gz'),'wt') as outfh:
        csvreader = csv.reader(fh, delimiter='\t')        
        csvwriter = csv.writer(outfh, delimiter='\t')
        header = next(csvreader)
        speciesname = header[2]
        csvwriter.writerow(header)
        for row in csvreader:
            og = row[0]
            targetspecies = row[1]
            if targetspecies not in lookup:
                # print(f'skipping {targetspecies} not in query set')
                continue
            qnamelst = row[2].split(', ')
            hitnames = row[3].split(', ')
            newhitnames = set()
            newqnames = set()
            for qname in qnamelst:
                if qname in lookup[species]:
                    YGOBname = lookup[species][qname]
                    newqnames.add(YGOBname)
                else:
                    print(f'no YGOB name for q: {species} {qname}')
                    continue
                if targetspecies in lookup:
                    for tname in hitnames:
                        if tname in lookup[targetspecies]:
                            newhitnames.add(lookup[targetspecies][tname])
                        else:
                            print(f'no YGOB name for t: {targetspecies} {tname}')
            if len(hitnames) > 0:
                csvwriter.writerow([og, targetspecies, ", ".join(newqnames), ", ".join(newhitnames)])
