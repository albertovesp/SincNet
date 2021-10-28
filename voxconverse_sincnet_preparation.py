#!/usr/bin/env python3
# Copyright 2021 Alberto Villalvazo
# Apache 2.0
import argparse, os, sys
import numpy as np
import shutil
import soundfile as sf
import sox
import math

class Segment_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    self.recording = words[1]
    self.begin = round(float(words[2]), 2)
    self.end = round(self.begin + float(words[3]), 2)
  def __str__(self):
    return 'segment_line -> begin: ' + str(self.begin) + ' end: ' + str(self.end)

#Compute the overlapping window, with 30% of overlap
def overlap(pair,duration,window):
    overlapped_list = []
    overlap_percent = 0.75
    #number of overlapped segments
    segments= math.floor(duration/(window*(1-overlap_percent)))
    overlapped_list = [(pair[0],pair[0]+window)]
    for i in range(segments):
      t0 = round(pair[0]+window*(1-overlap_percent)*(i+1),2)
      t1 = round(t0 + window,2)
      if t0 >= pair[1]:
        continue
      if t1 >= pair[1]:
        t1 = pair[1]
      overlapped_list.append((t0,t1))
    return overlapped_list

def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('segments_file', type = str, help = 'segments file')
  parser.add_argument('wav_path', type = str, help = 'Path to wav files')
  parser.add_argument('output_list', type = str, help = 'Output path')
  args = parser.parse_args()
  return args


def main():
  args = get_args()

  if not os.path.isfile(args.segments_file) or not os.path.isdir(args.wav_path) :
    sys.exit(args.segments_file + ' not found or is not file or ' + args.wav_path + " not found")


  if not os.path.exists(args.output_list):
    os.makedirs(args.output_list)
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
   
  #creates a dictionary with overlapping timestamps, each segment has a 1.5s duration
  wav_f = open(args.output_list + "/wav.scp", "w")
  overlapped_dict = {}
  for key in segments_dict.keys():
    wav_file = args.wav_path + '/' + str(key) + ".wav"
    wav_str = "{}\n".format(wav_file)
    wav_f.write(wav_str)
    for pair in segments_dict[key]:
      duration = pair[1] - pair[0]
      overlapped_list = overlap(pair,duration,1.5)
      if key not in overlapped_dict:
        overlapped_dict[key] = overlapped_list
      else:
        overlapped_dict[key].extend(overlapped_list)
  wav_f.close()

  #save dictionary
  np.save(args.output_list + '/overlapped_dict.npy',overlapped_dict)
  
if __name__ == '__main__':
  main()
         
