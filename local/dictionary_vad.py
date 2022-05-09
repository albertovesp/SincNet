import argparse, os, sys
import numpy as np
import kaldi_io

class Wav_line:
  def __init__(self, original_line):
    words = original_line.strip().split()
    self.audio = words[0]
    self.wav= words[1]
  def __str__(self):
    return 'Wav_line ->' + 'Audio: ' + str(self.audio) + 'wav: ' + str(self.wav)
class VAD_line:
  def __init__(self,original_line):
    words = original_line.strip().split()
    self.id = words[0]
    ark_1 = words[1].split(':')
    self.ark = ark_1[0] 

def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('vad_file', type = str, help = 'vad file')
  parser.add_argument('wav_file', type = str, help = 'wav file')
  parser.add_argument('output_file', type = str, help = 'Output VAD dictionary')
  args = parser.parse_args()
  return args

def main():
  args = get_args()
  
  if not os.path.isfile(args.vad_file):
    sys.exit(args.vad_file + ' not found or is not dir')

  f = open(args.wav_file,'r')
  wav_dict = {}
  for line in f.readlines():
    wav_line = Wav_line(line)
    if wav_line.audio not in wav_dict:
      wav_dict[wav_line.audio] = wav_line.wav
  f.close()
  
  vad_dict= {}
  f_vad = open(args.vad_file, 'r')
  for line in f_vad.readlines():
    vad_line = VAD_line(line)
    if vad_line.id not in vad_dict:
      vad_dict[wav_dict[vad_line.id]] = vad_line.ark

  np.save(args.output_file,vad_dict)
    
    
if __name__ == '__main__':
  main()
