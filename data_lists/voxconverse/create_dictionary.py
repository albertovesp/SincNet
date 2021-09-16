#!/usr/bin/env python3

import numpy as np

vox_dict = {'afjiv':5,'ccokr.wav': 5, 'jsdmu.wav': 1}

np.save('voxconverse_labels.npy',vox_dict,allow_pickle=True)

