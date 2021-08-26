# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 09:23:41 2021

@author: alber
"""

import numpy as np


dicti = {'dev/abjxc.wav':1,'dev/ioasm.wav':3, 'dev/zidwg.wav':7}


np.save('voxconverse_labels',dicti)

a=np.load('voxconverse_labels.npy',allow_pickle=True)
print(type(a))