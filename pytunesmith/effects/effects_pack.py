import numpy as np

from .base_effects import ConvolutionEffect

class EffectsPack:
    class Echo(ConvolutionEffect):
        """Prebuilt echo effect using a convolution with a specific impulse response."""
        def __init__(self, delay, decay, fs):
            impulse_response = np.zeros(int(delay * fs))
            impulse_response[0] = 1
            impulse_response[-1] = decay
            super().__init__(impulse_response)

    # Add more prebuilt effects here
