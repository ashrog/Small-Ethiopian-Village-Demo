import numpy as np

class DemoViewer:

    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        self.theta = 0
        self.gamma = 0
        self.vectors_pos_update()

    # The spherical co-ordiante calculation to set x,y,z with
    # "z" pointing up and "x" our forward
    def vectors_pos_update(self):
        Theta = np.deg2rad(self.theta)
        Gamma = np.deg2rad(self.gamma)
        
        # since x = cos(theta)*cos(gamma)
        # since y = sin(theta)*cos(gamma)
        # since z = sin(gamma)
        self.forwards = np.array(
            [
                np.cos(Theta) * np.cos(Gamma),
                np.sin(Theta) * np.cos(Gamma),
                np.sin(Gamma)
            ],
            dtype=np.float32
        )

        z_Up = np.array([0, 0, 1], dtype=np.float32)

        self.right = np.cross(self.forwards, z_Up)

        self.up = np.cross(self.right, self.forwards)