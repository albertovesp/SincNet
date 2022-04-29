#!/usr/bin/env python3
# Copyright 2022 Alberto Villalvazo
# Apache 2.0

import argparse, os, sys
import numpy as np

class Wav_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    name = words[0].split('-')
    self.name= name[0]
    self.speaker_id = words[1]
  def __str__(self):
    return 'wav_line ->' + str(self.speaker_id) + 'Name->' + str(self.name) 


def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('wav_file', type = str, help = 'Path to wav file')
  parser.add_argument('output_file', type = str, help = 'Path to output file')
  args = parser.parse_args()
  return args


def main():
  args = get_args()

  if not os.path.isfile(args.wav_file):
    sys.exit(args.wav_file + ' not found or is not file')

  f = open(args.wav_file, 'r')
  output_file = open(args.output_file, 'w')

  numberid_dict = {}
  speaker_dict = {}
  i = 0
  for line in f.readlines():
    wav_line= Wav_line(line)
    output_file.write(wav_line.speaker_id)
    output_file.write('\n')
    if wav_line.name not in numberid_dict:
      numberid_dict[wav_line.name] = i
      i += 1
    if wav_line.speaker_id not in speaker_dict:
      speaker_dict[wav_line.speaker_id] = numberid_dict[wav_line.name]

  f.close()
  output_file.close()
  np.save("labels.npy",speaker_dict)
if __name__ == '__main__':
  main()
