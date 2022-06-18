import pygame as pg
import numpy as np
import display_engine_model
import user_scene



class App:

    def __init__(self, screenWidth, screenHeight):

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.renderer = display_engine_model.GraphicsEngine()

        self.scene = user_scene.Scene()

        self.lastTime = pg.time.get_ticks()
        self.currentTime = 0
        self.numFrames = 0
        self.frameTime = 0
        self.lightCount = 0

        self.mainLoop()

    def mainLoop(self):
        running = True
        while (running):
            # check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            self.handleKeys()
            self.handleMouse()

            self.scene.update(self.frameTime * 0.05)

            self.renderer.render(self.scene)

            # timing
            self.calculateFramerate()
        self.quit()

    def handleKeys(self):

        keys = pg.key.get_pressed()
        combo = 0
        directionModifier = 0

        # w: 1 -> 0 degrees
        # a: 2 -> 90 degrees
        # w & a: 3 -> 45 degrees
        # s: 4 -> 180 degrees
        # w & s: 5 -> x
        # a & s: 6 -> 135 degrees
        # w & a & s: 7 -> 90 degrees
        # d: 8 -> 270 degrees
        # w & d: 9 -> 315 degrees
        # a & d: 10 -> x
        # w & a & d: 11 -> 0 degrees
        # s & d: 12 -> 225 degrees
        # w & s & d: 13 -> 270 degrees
        # a & s & d: 14 -> 180 degrees
        # w & a & s & d: 15 -> x


        if keys[pg.K_w]:
            combo += 1
        if keys[pg.K_a]:
            combo += 2
        if keys[pg.K_s]:
            combo += 4
        if keys[pg.K_d]:
            combo += 8

        if combo > 0:
            if combo == 3:
                directionModifier = 45
            elif combo == 2 or combo == 7:
                directionModifier = 90
            elif combo == 6:
                directionModifier = 135
            elif combo == 4 or combo == 14:
                directionModifier = 180
            elif combo == 12:
                directionModifier = 225
            elif combo == 8 or combo == 13:
                directionModifier = 270
            elif combo == 9:
                directionModifier = 315

            dPos = [
                self.frameTime * 0.025 * np.cos(np.deg2rad(self.scene.player.theta + directionModifier)),
                self.frameTime * 0.025 * np.sin(np.deg2rad(self.scene.player.theta + directionModifier)),
                0
            ]

            self.scene.move_player(dPos)

    def handleMouse(self):

        (x, y) = pg.mouse.get_pos()
        theta_increment = self.frameTime * 0.05 * ((self.screenWidth // 2) - x)
        phi_increment = self.frameTime * 0.05 * ((self.screenHeight // 2) - y)
        self.scene.spin_player(theta_increment, phi_increment)
        pg.mouse.set_pos((self.screenWidth // 2, self.screenHeight // 2))

    def calculateFramerate(self):

        self.currentTime = pg.time.get_ticks()
        delta = self.currentTime - self.lastTime
        if (delta >= 1000):
            framerate = max(1, int(1000.0 * self.numFrames / delta))
            pg.display.set_caption(f"Running at {framerate} fps.")
            self.lastTime = self.currentTime
            self.numFrames = -1
            self.frameTime = float(1000.0 / max(1, framerate))
        self.numFrames += 1

    def quit(self):

        self.renderer.unbind()





myApp = App(700, 500)