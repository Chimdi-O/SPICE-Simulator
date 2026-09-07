
import math 
from SIunit import SI_prefix 

class Sinewave(): 
    def __init__(self, amplitude, frequency): 
        self.name = "sine"
        self.amplitude = amplitude 
        self.frequency = frequency

    def __repr__(self):
        return f"sine( {SI_prefix(self.amplitude)} {SI_prefix(self.frequency)})"

    def value(self,time): 
        return self.amplitude*math.sin(2*math.pi*self.frequency*time)
