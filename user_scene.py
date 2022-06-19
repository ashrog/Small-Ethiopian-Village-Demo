import numpy as np
import up_right_orientation

class ObjectScene:

    def __init__(self):

        # starting position for the viewer is given here
        from object_position_roll import OneJoinedVillage
        self.objectsOne = [
            OneJoinedVillage(
                position=[-10, -10, -20],
                eulers=[1, 0, 0]
            ),
        ]

        self.demoView = up_right_orientation.DemoViewer(
            position=[0, 0, 2]
        )

    def rotation_updates(self, rate):

        # pointing "z" to our screen rotate the whole on "y"
        for obj_new in self.objectsOne:
            obj_new.eulers[1] = obj_new.eulers[1] + (0.25 * rate)
            if obj_new.eulers[1] > 360:
                obj_new.eulers[1] -= 360
                
                
     # spherical co-ordinate in degrees "gamma" and "theta"
    def mouse_turns(self, dTheta, dGamma):

        self.demoView.theta += dTheta
        if self.demoView.theta < 0:
            self.demoView.theta += 360
            
        elif self.demoView.theta > 360:
            self.demoView.theta -= 360

        self.demoView.gamma = min(
            90, max(-90, self.demoView.gamma + dGamma)
        )
        self.demoView.vectors_pos_update()

    def move_with_keys(self, mov_position):

        mov_position = np.array(mov_position, dtype=np.float32)
        self.demoView.position += mov_position

   
