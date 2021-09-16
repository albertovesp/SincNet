#!/usr/bin/env python3

# Voxconverse_preparation 
# Alberto Villalvazo 
# Tecnologico de Monterrey

# September 2021

# Description: 
# This code prepares Voxconverse for SincNet features. 
# It removes start and end silences according to the information reported in the *.wrd files and normalizes the amplitude of each sentence.
 
# How to run it:
# python Voxconverse_preparation.py $Voxconverse_FOLDER $OUTPUT_FOLDER data_lists/Voxconverse_all.scp 



import shutil
import os
import soundfile as sf
import numpy as np
import sys
import sox

def ReadList(list_file):
 f=open(list_file,"r")
 lines=f.readlines()
 list_sig = []
 name_list = []
 for x in lines:
    words = x.strip().split()
    list_sig.append(words[1])
    name_list.append(words[0])
 f.close()
 return list_sig, name_list

def ReadNewList(list_file):
 f=open(list_file,"r")
 lines=f.readlines()
 list_sig=[]
 for x in lines:
    list_sig.append(x.rstrip())
 f.close()
 return list_sig

def copy_folder(in_folder,out_folder):
 if not(os.path.isdir(out_folder)):
  shutil.copytree(in_folder, out_folder, ignore=ig_f)

def ig_f(dir, files):
 return [f for f in files if os.path.isfile(os.path.join(dir, f))]



in_folder=sys.argv[1]
out_folder=sys.argv[2]
list_file=sys.argv[3]
out_wav = sys.argv[4]
#create directory
if not os.path.exists(out_folder):
  os.makedirs(out_folder)


# Read List file
list_sig,name_list=ReadList(list_file)

wav_f = open(out_wav+'/wav.scp','w')
# Speech Data Reverberation Loop
for i in range(len(list_sig)): 
  # Open the wav file
  wav_file=list_sig[i]
  duration= sox.file_info.duration(wav_file)
  segment = duration//5
  for j in range(0,4):
    tfm = sox.Transformer()
    tfm.trim(j*segment, segment*(j+1))
    wav_str = "{}\n".format(out_folder+"/"+name_list[i]+'_'+str(j)+'.wav')
    wav_f.write(wav_str)
    tfm.build_file(wav_file,out_folder+'/'+name_list[i]+'_'+str(j)+'.wav')
 
  tfm = sox.Transformer()
  tfm.trim(4*segment, duration)
  wav_str = "{}\n".format(out_folder+"/"+name_list[i]+'_4.wav')
  wav_f.write(wav_str)
  tfm.build_file(wav_file,out_folder+'/'+name_list[i]+'_4.wav')
wav_f.close()

new_list = ReadNewList(out_wav+'/wav.scp')
for i in range(len(new_list)):
  wav_file=new_list[i]
  [signal, fs] = sf.read(wav_file)
  signal=signal.astype(np.float64)
  # Signal normalization
  signal=signal/np.max(np.abs(signal))
  sf.write(wav_file, signal, fs)
  print("Done %s" % (wav_file))           
