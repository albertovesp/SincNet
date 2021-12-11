#!/usr/bin/env python3
# Copyright 2021 Alberto Villalvazo
# Apache 2.0
import argparse, os, sys
import numpy as np
import math

class Segment_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    self.recording = words[0]
    self.begin = round(float(words[2]), 2)
    self.end   = round(float(words[3]), 2)
  def __str__(self):
    return 'segment_line -> begin: ' + str(self.begin) + ' end: ' + str(self.end)

class Wav_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    self.recording = words[0]
    if len(words)>2:
      self.path = words[5]
    else:
      self.path = words[1]
  def __str__(self):
    return 'wav_line -> begin: ' + self.recording + ' end: ' + self.path

def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('segments_file', type = str, help = 'segments file')
  parser.add_argument('wav_file', type = str, help = 'Wav.scp file')
  parser.add_argument('output_list', type = str, help = 'Output path')
  args = parser.parse_args()
  return args


def main():
  args = get_args()

  if not os.path.isfile(args.segments_file) or not os.path.isfile(args.wav_file):
    sys.exit(args.segments_file + ' not found or is not file or ' + args.wav_file + ' not exit')


  if not os.path.exists(args.output_list):
    os.makedirs(args.output_list)

  #read wav file
  wav_f = open(args.wav_file,'r')
  wav_dict = {}
  for line in wav_f.readlines():
    wav_line = Wav_line(line)
    if wav_line.recording not in wav_dict:
      wav_dict[wav_line.recording] = wav_line.path
  wav_f.close()

  #create a new wav.scp file
  wav_out = open(args.output_list+'/wav.scp', 'w')
  for key in wav_dict.keys():
    wav_str = "{} {}\n".format(key, wav_dict[key])
    wav_out.write(wav_str)
  wav_out.close()

  # read the segments file
  f = open(args.segments_file, 'r')
  segments_dict = {}
  for line in f.readlines():
    segment_line = Segment_line(line)
    if segment_line.recording not in segments_dict:
      segments_dict[segment_line.recording] = [(segment_line.begin,segment_line.end)]
    else:
      segments_dict[segment_line.recording].append((segment_line.begin,segment_line.end))
  f.close()
  

  #save dictionary
  np.save(args.output_list + '/segments_dict.npy',segments_dict)
  
if __name__ == '__main__':
  main()
         
