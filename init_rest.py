import pickle

restrictions = {'GAATTC': 'EcoRI',
                'TCTAGA': 'XbaI',
                'ACTAGT': 'SpeI',
                'CTGCAG': 'PstI',
                'GCGGCCGC': 'NotI',
                'GCTCTTC': 'SapI',
                'GGTCTC': 'BsaI'}

pickle_out = open('restrictions.pickle', 'wb')
pickle.dump(restrictions, pickle_out)
pickle_out.close()
