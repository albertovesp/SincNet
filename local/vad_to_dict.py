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

def get_args():
  parser = argparse.ArgumentParser(description = '')
  parser.add_argument('vad_file', type = str, help = 'vad.scp file')
  parser.add_argument('wav_file', type = str, help = 'wav file')
   parser.add_argument('output_file', type = str, help = 'Output VAD dictionary')
  args = parser.parse_args()
  return args

def main():
  args = get_args()
  
  if not os.path.isfile(args.vad_file):
    sys.exit(args.vad_file + ' not found or is not file or ')

  vad_dict = {}
  for key,vec in kaldi_io.read_vec_flt_scp(args.vad_file):
    vad_dict[key] = vec

  f = open(args.wav_file,'r')
  wav_dict = {}
  for line in f.readlines():
    wav_line = Wav_line(line)
    if wav_line.audio not in wav_dict:
      wav_dict[wav_line.audio] = wav_line.wav

  f.close()
  
  new_vad_dict = {}
  for key in vad_dict.keys():
    new_vad = []
    for frame in vad_dict[key]:
      new_vad = np.concatenate((new_vad, [frame]*160), axis=None)
    new_vad = np.concatenate((new_vad, [0]), axis=None)
    new_vad_dict[wav_dict[key]] = new_vad
  
  np.save(args.output_file, new_vad_dict)
if __name__ == '__main__':
  main()
