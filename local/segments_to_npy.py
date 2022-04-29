#!/usr/bin/env python3
# Copyright 2022 Alberto Villalvazo
# Apache 2.0

import argparse, os, sys
import numpy as np

class Seg_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    name = words[0].split('-')
    self.name= words[1]
    self.begin = words[2]
    self.end = words[3]
  def __str__(self):
      return 'Seg_line ->' 'Name: ' + str(self.name) + ' begin: ' + str(self.begin) + ' end: '+ str(self.end)

class Wav_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    self.audio = words[0]
    self.wav= words[1]
  def __str__(self):
      return 'Wav_line ->' + 'Audio: ' + str(self.audio) + 'wav: ' + str(self.wav)  

def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('segments_file', type = str, help = 'Path to segments file')
  parser.add_argument('wav_file', type = str, help = 'Path to wav file')
  parser.add_argument('output_file', type = str, help = 'Path to output dictionary')
  args = parser.parse_args()
  return args


def main():
  args = get_args()

  if not os.path.isfile(args.segments_file):
    sys.exit(args.segments_file + ' not found or is not file')

  f = open(args.segments_file, 'r')
  
  segments_dict = {}
  for line in f.readlines():
    seg_line = Seg_line(line)
    if seg_line.name not in segments_dict:
      segments_dict[seg_line.name] = [(seg_line.begin,seg_line.end)]
    else:
      segments_dict[seg_line.name].append((seg_line.begin,seg_line.end))

  f.close()
  f2 = open(args.wav_file,'r')
  wav_dict = {}
  for line in f2.readlines():
    wav_line = Wav_line(line)
    if wav_line.audio not in wav_dict:
      wav_dict[wav_line.audio] = wav_line.wav
  
  new_seg = {}
  for key in wav_dict.keys():
    if wav_dict[key] not in new_seg:
      new_seg[wav_dict[key]] = segments_dict[key]
  
  np.save(args.output_file,new_seg)

if __name__ == '__main__':
  main()
