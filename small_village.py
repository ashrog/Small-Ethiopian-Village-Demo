import pygame as pg
import numpy as np
import display_rendered
import user_scene



class Main_Loop:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.display_obj = display_rendered.RenderedDisplay()

        self.scene = user_scene.ObjectScene()

        self.lastTime = pg.time.get_ticks()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        

        self.mainLoop()

    def mainLoop(self):
        display = True
        while (display):
            # check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    display = False
                # escape key to QUIT
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        display = False

            self.key_move()
            self.mouse_camera()

            self.scene.rotation_updates(self.frameTime * 0.05)

            self.display_obj.render_object(self.scene)

            # timing
            self.framerate_changed_per_camera()
        self.display_obj.unbind()

    def key_move(self):

        keys = pg.key.get_pressed()
        multiple_key_press = 0
        
        # degree of the final pressed keys using pygame keys.
        degree_with_key = 0

        if keys[pg.K_w]:
            degree_with_key = 0
               
        if keys[pg.K_a]:
           degree_with_key = 90
        if keys[pg.K_s]:
            degree_with_key = 180
        if keys[pg.K_d]:
            degree_with_key = 270
        if keys[pg.K_w] and keys[pg.K_a]:
            degree_with_key = 45
        if keys[pg.K_w] and keys[pg.K_a]:
            degree_with_key = 315
        if keys[pg.K_a] and keys[pg.K_s]:
            degree_with_key = 135
        if keys[pg.K_d] and keys[pg.K_s]:
            degree_with_key = 225
        if keys[pg.K_w] and keys[pg.K_a] and keys[pg.K_s]:
            degree_with_key = 90
        if keys[pg.K_w] and keys[pg.K_a] and keys[pg.K_d]:
            degree_with_key = 0
        if keys[pg.K_w] and keys[pg.K_s] and keys[pg.K_d]:
            degree_with_key = 270
        if keys[pg.K_a] and keys[pg.K_s] and keys[pg.K_d]:
            degree_with_key = 180
       
    #    key usage implememntation first
            theta_cos_keyC = np.cos(np.deg2rad(self.scene.demoView.theta + degree_with_key))
            theta_sin_keyC = np.sin(np.deg2rad(self.scene.demoView.theta + degree_with_key))
            
            # frame time being the time it takes to create the new found position
            # when using the keys to move around.
            # move_position is the changing x,y direction with key to move in four directions.
            move_position = [
                self.frameTime * 0.025 * theta_cos_keyC ,
                self.frameTime * 0.025 * theta_sin_keyC,
                0
            ]

            self.scene.move_with_keys(move_position)

    def mouse_camera(self):

        (x, y) = pg.mouse.get_pos()
        
        theta_initial = self.width // 2
        gamma_initial =  self.height // 2
        
        # using the spherical co-ordinates "theta" and "gamma"
        # theta being for the x co-ordinate
        # gamma for the y- co-ordinate
        theta_increment = self.frameTime * 0.05 * ((self.width // 2) - x)
        gamma_increment = self.frameTime * 0.05 * ((self.height // 2) - y)
        
        
        self.scene.mouse_turns(theta_increment, gamma_increment)
        pg.mouse.set_pos((theta_initial, gamma_initial))

    def framerate_changed_per_camera(self):

        self.currentTime = pg.time.get_ticks()
        delta = self.currentTime - self.lastTime
        
        if (delta >= 1000):
            framerate = max(1, int(1000.0 * self.numFrames / delta))
            
            # the title to show the framerate change
            self.lastTime = self.currentTime
            self.numFrames = -1
            
            self.frameTime = float(1000.0 / max(1, framerate))
        self.numFrames += 1

        
myApp = Main_Loop(700, 500)