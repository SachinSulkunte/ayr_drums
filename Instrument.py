import os
import scipy.io.wavfile as wavfile
import numpy

import Logger

class Instrument:
    def __init__(self, name, file, position, type, default_volume=50):
        self.name = name
        self.file = file
        self.position = None # TODO
        self.type = type
        self.default_volume = default_volume

        if not self.verify_sound():
            raise ValueError(f"Sound file '{self.file}' does not exist or is inaccessible.")
    
    def __str__(self):
        return f"Instrument(name={self.name}, file={self.file}, position={self.position}, default_volume={self.default_volume})"

    # check existence of sound file
    def verify_sound(self):
        return os.path.exists(self.file)
    
    # Modify positioning of instrument
    def change_position(self):
        return
    
    # Return message for logger output
    def to_16bit_wav(self, filepath):
        sr, data = wavfile.read(filepath)
        wavfile.write(filepath, sr, numpy.int16(data))
        return ("Converted file to 16-bit audio")


# class HiHat(Instrument):
#     def __init__(self, name, file_open, file_closed, position, open, default_volume=50):
#         super().__init__(name, position, default_volume)
#         self.file_open = file_open
#         self.file_closed = file_closed
#         self.open = open
    
#     def __str__(self):
#         return f"HiHat(name={self.name}, file_open={self.file_open}, file_closed={self.file_closed}, position={self.position}, open={self.open}, default_volume={self.default_volume})"

#     # Move foot position for open/close state
#     def change_position(self):
#         return super().change_position()
    
#     def is_open(self):
#         return self.open