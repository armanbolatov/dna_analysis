import re

str = "GAATC"

restrictions = [
    ('GAATC', 'EcoRI'),
    ('TCTAGA', 'XbaI'),
    ('ACTAGT', 'SpeI'),
    ('CTGCAG', 'PstI'),
    ('GCGGCCGC', 'NotI'),
    ('GCTCTCC', 'SapI'),
    ('GGTCTC', 'BcaI')
]


def find_instances(dna: str, restrictions: str):
    instances = []
    for restriction in restrictions:
        base, name = restriction[0], restriction[1]
        for e in [m.start() for m in re.finditer(base, dna)]:
            instances.append((e, base, name))
    instances.sort()
    ans = [None] * len(dna)
    pos, j = 0, 0
    while pos < len(dna) and j < len(instances):
        while pos > instances[j][0]:
            j += 1
        if pos == instances[j][0]:
            for i in range(len(instances[j][1])):
                ans[pos + i] = (instances[j][1], instances[j][2])
            pos += len(instances[j][1]) - 1
        pos += 1
    return ans

print(find_instances(str, restrictions))
# for i in range(len(str)):
