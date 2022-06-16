# import pygame
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from pygame.locals import *
# import numpy as np


# def init():
#     pygame.init()
#     display = (1800, 900)
#     pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    





# def main():
#     init()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#         draw()
#         pygame.display.flip()
#         pygame.time.wait(10)

# main()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np



def init():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)




def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(5)
    #glBegin(GL_LINES)
    #glVertex2f(0.0, -1.0)
    #glVertex2f(0.0, 1.0)
    #glVertex2f(1.0, 0.0)
    #glVertex2f(-1.0, 0.0)

    #glEnd()
    #glFlush()
    t=1
    v=np.array([0.3,0.4])
    u=np.multiply(v,t)

    po=np.array([0.1,0.1])
    p=np.add(u,po)


    po1=np.array([-0.9,0.1])
    p1=np.add(u,po1)

    po2 = np.array([-0.9, -0.9])
    p2 = np.add(u, po2)

    po3 = np.array([0.1, -0.9])
    p3 = np.add(u, po3)
    
    po4 = np.array([-0.4, 0.5])
    p4 = np.add(u, po4)

    glBegin(GL_LINE_STRIP)
    glVertex2fv(p)
    glVertex2fv(p1)
    glVertex2fv(p2)
    glVertex2fv(p3)
    glVertex2fv(p)
    glVertex2fv(p4)
    glVertex2fv(p1)


    glEnd()
    glFlush()


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