import re
from biohack import codons_to_acids, acids_to_codons

def complement(dna: str) -> str:
    map = {"C": "G", "G": "C", "A": "T", "T": "A"}
    complement_dna = ""
    for nucleotid in dna:
        complement_dna += map[nucleotid]
    return complement_dna

print(complement("AAAGGGGCT"))

def find_instances(dna: str, restrictions: str):
    '''
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
    Takes a DNA sequence and converts it to sequence
    of aminoacids.
    '''
    acids = []
    for i in range(0, len(dna), 3):
        if i >= len(dna) - 2: break
        codon = dna[i: i+3]
        acids.append(codons_to_acids[codon])
    return acids

def remove_instances(dna: str, instances: list):
    result_dna = list(dna)
    acids = convert_to_acids(dna)
    for i in range(0, len(dna), 3):
        if instances[i] is not None:
            acid = acids[i//3]
            for codon in acids_to_codons[acid]:
                print(codon, instances[i])
                if list(codon) != result_dna[i: i+3]:
                    print('YES!')
                    result_dna[i] = codon[0]
                    result_dna[i+1] = codon[1]
                    result_dna[i+2] = codon[2]
                    if instances[i-1] is not None:
                        for j in range(i-3, i):
                            instances[j] = None
                    if i+3 < len(dna) and instances[i+3] is not None:
                        for j in range(i+3, i+6):
                            instances[j] = None
    result_dna = ''.join(result_dna)
    # return result_dna
    if is_proper_dna(result_dna, restrictions):
        return result_dna
    else:
        instances = find_instances(result_dna, restrictions)
        return remove_instances(result_dna, instances)

str = "GAATCGGGGGGGGGGGGGGGGGGGGGGGGGGGGTCTAGA"

restrictions = [
    ('GAATC', 'EcoRI'),
    ('TCTAGA', 'XbaI'),
    ('ACTAGT', 'SpeI'),
    ('CTGCAG', 'PstI'),
    ('GCGGCCGC', 'NotI'),
    ('GCTCTCC', 'SapI'),
    ('GGTCTC', 'BcaI')
]

insta = find_instances(str, restrictions)
print(remove_instances(str, insta))
