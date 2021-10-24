import sys
import numpy as np
in_dictionary=sys.argv[1]

array = np.load(in_dictionary,allow_pickle=True)
print(array)
dictionary = {'abjxc.wav': 10 }

np.save('dictio',dictionary,allow_pickle=True)

