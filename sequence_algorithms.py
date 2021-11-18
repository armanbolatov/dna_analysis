import re
from dictionaries import codons_to_acids, acids_to_codons

def get_nth_key(dictionary: dict, n=0) -> str:
    '''
    Input: a dictionary
    Output: a key located at postiton n
    '''
    if n < 0: n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n: return key
    raise IndexError("dictionary index out of range")

def complement(dna: str) -> str:
    '''
    Input: a DNA sequences
    Output: its complementary sequences
    '''
    map = {"C": "G", "G": "C", "A": "T", "T": "A"}
    complement_dna = ""
    for nucleotid in dna:
        complement_dna += map[nucleotid]
    return complement_dna

def find_instances(dna: str, restrictions: str) -> list:
    '''
    Input: a DNA sequence and restriction site
    Output: a list containing tuples of base sequence and names
    of the selected restriction sites at position i.
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

def convert_to_acids(dna: str) -> list:
    '''
    Input: a DNA sequence
    Output: a sequence of aminoacids
    '''
    acids = []
    for i in range(0, len(dna), 3):
        if i >= len(dna) - 2: break
        codon = dna[i: i + 3]
        acids.append(codons_to_acids[codon])
    return acids

def remove_instances(dna: str, instances: list) -> str:
    '''
    Input: a DNA sequence and instances of restriction sites in it
    Output: the DNA sequence after removing all selected
    restrictions sites from it
    '''
    result_dna = list(dna)
    acids = convert_to_acids(dna)
    for i in range(len(dna)):
        if instances[i] is not None:
            acid = acids[i // 3]
            for codon in acids_to_codons[acid]:
                j = i - (i % 3)
                if list(codon) != result_dna[j: j + 3]:
                    for k in range(3):
                        result_dna[j + k] = codon[k]
                    for k in range(len(instances[i][0])):
                        instances[i + k] = None
                    break
    result_dna = ''.join(result_dna)
    return result_dna

def find_positions(instances: list) -> dict:
    '''
    Input: instances of restriction sites in the DNA
    Output: a dictionary which maps a restriction into positions where it
    was found in the given DNA
    '''
    positions, i = dict(), 0
    while i < len(instances):
        if instances[i] is not None:
            rest = instances[i]
            if rest not in positions:
                positions[rest] = [i]
            else: positions[rest].append(i)
            i += len(rest[0])
        else: i += 1
    return positions
