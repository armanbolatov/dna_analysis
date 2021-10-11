import re
from biohack import codons_to_acids, acids_to_codons

def complement(dna: str) -> str:
    map = {"C": "G", "G": "C", "A": "T", "T": "A"}
    complement_dna = ""
    for nucleotid in dna:
        complement_dna += map[nucleotid]
    return complement_dna

def find_instances(dna: str, restrictions: str) -> list:
    '''
    Input: a DNA sequence
    Output: a list containing tuples of position, base sequence, and names
    of the selected variables.
    '''
    app = []
    for restriction in restrictions:
        base, name = restriction[0], restriction[1]
        for e in [m.start() for m in re.finditer(base, dna)]:
            app.append((e, base, name))
    app.sort()
    instances = [None] * len(dna)
    pos, j = 0, 0
    while pos < len(dna):
        while j < len(app) and pos > app[j][0]:
            j += 1
        if j >= len(app): break
        if pos == app[j][0]:
            for i in range(len(app[j][1])):
                instances[pos + i] = (app[j][1], app[j][2])
            pos += len(app[j][1]) - 1
        pos += 1
    return instances

def is_proper_dna(dna: str, restrictions: list):
    for nucleotid in find_instances(dna, restrictions):
        if nucleotid is not None:
            return False
    return True

def convert_to_acids(dna: str) -> list:
    '''
    Input: a DNA sequence
    Output: a sequence of aminoacids
    '''
    acids = []
    for i in range(0, len(dna), 3):
        if i >= len(dna) - 2: break
        codon = dna[i: i+3]
        acids.append(codons_to_acids[codon])
    return acids

def remove_instances(dna: str, instances: list) -> str:
    result_dna = list(dna)
    acids = convert_to_acids(dna)
    for i in range(0, len(dna), 3):
        if instances[i] is not None:
            acid = acids[i//3]
            for codon in acids_to_codons[acid]:
                if list(codon) != result_dna[i: i+3]:
                    for j in range(3): result_dna[i+j] = codon[j]
                    if instances[i-1] is not None:
                        for j in range(i-3, i):
                            instances[j] = None
                    if i+3 < len(dna) and instances[i+3] is not None:
                        for j in range(i+3, i+6):
                            instances[j] = None
    result_dna = ''.join(result_dna)
    return result_dna

def find_positions(instances: list):
    positions, i = dict(), 0
    while i < len(instances):
        if instances[i] is not None:
            rest = instances[i]
            if rest not in positions: positions[rest] = [i]
            else: positions[rest].append(i)
            i += len(rest[0])
        else: i += 1
    return positions

str = "GAATCGGGGGGGGGGCTTAGGGGGGGGGGGGGGGGGTCTAGA"

restrictions = [
    ('GAATC', 'EcoRI'),
    ('CTTAG', 'compl_EcoRI'),
    ('TCTAGA', 'XbaI'),
    ('ACTAGT', 'SpeI'),
    ('CTGCAG', 'PstI'),
    ('GCGGCCGC', 'NotI'),
    ('GCTCTCC', 'SapI'),
    ('GGTCTC', 'BcaI')
]

insta = find_instances(str, restrictions)
print(remove_instances(str, insta))

# print(find_positions([None, None, None, ('GAATC', 'EcoRI'), ('GAATC', 'EcoRI'), ('GAATC', 'EcoRI'), ('GAATC', 'EcoRI'), ('GAATC', 'EcoRI'), None, None, None]))
