#!/usr/bin/env python3

import csv
import os
import gzip

YGOB_pillars = 'v7-Aug2012/Pillars.tab'
results = 'Orthologues_renamed'

OrthoFinder_GroupsTable = {}
YGOB_GroupsTable = {}
YGOB_Gene2Group = {}
with open(YGOB_pillars, 'r') as f:
    reader = csv.reader(f, delimiter="\t")
    n = 0
    for row in reader:
        YGOB_GroupsTable[n] = set()
        for gene in row:
            if gene != '---':
                YGOB_GroupsTable[n].add(gene)
                YGOB_Gene2Group[gene] = n
        n += 1
gene2species = {}
for species in os.listdir(results):
    if not species.endswith('.tsv.gz'):
        continue
    orthogroupfile = os.path.join(results, species)
    with gzip.open(orthogroupfile, 'rt') as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        qspeciesname = header[2]        
        for row in reader:
            orthogroup = row[0]
            tspecies = row[1]
            if orthogroup not in OrthoFinder_GroupsTable:
                OrthoFinder_GroupsTable[orthogroup] = set()
            for gene in row[2].split(", "):
                OrthoFinder_GroupsTable[orthogroup].add(gene)                
                #if gene in gene2species and gene2species[gene] != qspeciesname:
                #    print(f"WARNING: {gene} in {orthogroup} has multiple species assignments: {gene2species[gene]} and {qspeciesname}")
                if gene not in gene2species:
                    gene2species[gene] = qspeciesname
            for gene in row[3].split(", "):
                OrthoFinder_GroupsTable[orthogroup].add(gene)
                #if gene in gene2species and gene2species[gene] != tspecies:
                #    print(f"WARNING: {gene} in {orthogroup} has multiple species assignments: {gene2species[gene]} and {tspecies}")
                if gene not in gene2species:
                    gene2species[gene] = tspecies

for OG in OrthoFinder_GroupsTable:
    YGOB_OGs = {}
    for gene in OrthoFinder_GroupsTable[OG]:
        if gene in YGOB_Gene2Group:
            YGOB_OGname = YGOB_Gene2Group[gene]
            if YGOB_OGname not in YGOB_OGs:
                YGOB_OGs[YGOB_OGname] = 0
            YGOB_OGs[YGOB_OGname] += 1
    print(f'OrthoGroup: {OG}, YGOB: {YGOB_OGs}')
    print(f'{OG}: ', ", ".join(OrthoFinder_GroupsTable[OG]))
    for ygob in YGOB_OGs:
        print(f'YGOB_{ygob}', ", ".join(YGOB_GroupsTable[ygob]))
    print("//")