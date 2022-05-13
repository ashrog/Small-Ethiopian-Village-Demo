import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np


def init():
    pygame.init()
    display = (1800, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    





def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw()
        pygame.display.flip()
        pygame.time.wait(10)

main()