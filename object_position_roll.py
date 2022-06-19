import numpy as np


class OneJoinedVillage:

    # eulers take value of the roll angle
    # in x, y , and z order
    # in "yaw", "pitch", and "fall"

    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)