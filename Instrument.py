import os
import scipy.io.wavfile as wavfile
import numpy
import wave
import logging 

import Logger

class Instrument:
    def __init__(self, name, file, type, position=None, default_volume=50):
        self.name = name
        self.file = file
        self.type = type

        self.log = Logger.MyLogger(f"{name}", log_level=logging.DEBUG)

        if position is None or not isinstance(position, list):
            self.position = []
            self.log.debug("No position set")
        else:
            self.position = position
        self.default_volume = default_volume

        if not self.verify_sound():
            self.log.error('Sound file does not exist.')
            raise ValueError(f"Sound file '{self.file}' does not exist or is inaccessible.")
    
    def __str__(self):
        return f"Instrument(name={self.name}, file={self.file}, position={self.position}, default_volume={self.default_volume})"

    # check existence of sound file
    def verify_sound(self):
        return os.path.exists(self.file)
    
    # Modify positioning of instrument
    def change_position(self, x, y):
        orig = self.position # track prev position
        self.position = (x, y)
        self.log.info(f"Changed {self.name} position from {orig} to {self.position}")
        return
    
    # Convert to 16-bit audio
    def to_16bit_wav(self, filepath):
        try:
            sr, data = wavfile.read(filepath)
            wavfile.write(filepath, sr, numpy.int16(data))
            self.log.info(f"Converted file {filepath} to 16-bit audio")
            return True
        except Exception as e:
            self.log.warning(f"Unable to convert audio file {filepath} to 16-bit audio")
            return False
    
    # Check if audio file is 16-bit
    def is_16_bit_audio(self, file):
        try:
            with wave.open(file, 'rb') as wave_file:
                sample_width = wave_file.getsampwidth()
                bit_depth = sample_width * 8

                if bit_depth == 16:
                    self.log.info(f"The file '{file}' is a 16-bit audio file.")
                    return True
                else:
                    self.log.debug(f"The file '{file}' is not a 16-bit audio file. Attempting to convert.")
                    check = self.to_16bit_wav(file)
                    return check
        except wave.Error as e:
            print(f"Error: {e}")
            return False
        except FileNotFoundError:
            print(f"Error: The file '{file}' does not exist.")
            return False