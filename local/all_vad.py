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
  parser.add_argument('vad_path', type = str, help = 'vad folder')
  parser.add_argument('wav_file', type = str, help = 'wav file')
  parser.add_argument('output_path', type = str, help = 'Output VAD dictionary')
  args = parser.parse_args()
  return args

def main():
  args = get_args()
  
  if not os.path.isdir(args.vad_path):
    sys.exit(args.vad_path + ' not found or is not dir')

  f = open(args.wav_file,'r')
  wav_dict = {}
  for line in f.readlines():
    wav_line = Wav_line(line)
    if wav_line.audio not in wav_dict:
      wav_dict[wav_line.audio] = wav_line.wav
  f.close()

  
  f_scp = open(args.output_path + '/vad.scp', 'w')
  for subdir, dirs, files in os.walk(args.vad_path):
    for file in files:
      ark_file= args.vad_path+"/"+ file
      for key,vec in kaldi_io.read_vec_flt_ark(ark_file):
        print(key + ' ' + os.path.abspath(ark_file) + ':' + str(len(key)+1))
        f_scp.write(key + ' ' + os.path.abspath(ark_file) + ':' + str(len(key)+1) + '\n')
  f_scp.close()
if __name__ == '__main__':
  main()
