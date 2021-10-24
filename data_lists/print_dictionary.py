#!/usr/bin/env python3

# Alberto Villalvazo
# Tecnologico de Monterrey
# July 2021

import os
import numpy as np
import sys

in_dict=sys.argv[1]

dictionary = np.load(in_dict, allow_pickle=True)
print(dictionary)
