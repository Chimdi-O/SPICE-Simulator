
import math 
from SIunit import SI_prefix 

class Sinewave(): 
    def __init__(self, dc_offset, amplitude, frequency): 
        self.dc_offset = dc_offset
        self.amplitude = amplitude 
        self.frequency = frequency

    def __repr__(self):
        return f"sine({SI_prefix(self.dc_offset)} {SI_prefix(self.amplitude)} {SI_prefix(self.frequency)})"

    def value(self,time): 
        return self.dc_offset + self.amplitude*math.sin(2*math.pi*self.frequency*time)
