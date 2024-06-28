import scipy.io.wavfile as wavfile
import numpy

def to_16bit_wav(filepath):
  sr, data = wavfile.read(filepath)
  wavfile.write(filepath, sr, numpy.int16(data))
  print("Converted file to 16-bit audio")

def main():
    file =  "./samples/hihat.wav"
    to_16bit_wav(file)

if __name__=="__main__": 
    main() 