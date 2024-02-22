import numpy as np
from pytunesmith.core import Effect

class ConvolutionEffect(Effect):
    """Effect that applies a convolution with an impulse response."""
    def __init__(self, impulse_response):
        self.impulse_response = impulse_response

    def apply(self, audio, fs):
        return np.convolve(audio, self.impulse_response, mode='same')

class GainEffect(Effect):
    """Effect that applies a gain to the audio."""
    def __init__(self, gain):
        self.gain = gain

    def apply(self, audio, fs):
        return audio * self.gain
