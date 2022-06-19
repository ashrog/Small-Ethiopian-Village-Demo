import pygame as pg
from OpenGL.GL import *
import numpy as np
from PIL import Image
import os
class Texture:

    def __init__(self):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open("images/door_2.jpg")
        # TO SEE COLORED FILE DECOMMENT NEXT LINE
        # image = pg.image.load(filepath).convert()
        
        width, height = image.size
        image_data = np.array(list(image.getdata()), dtype= np.uint8)
        # DECOMMENT NEXT LINE FOR USING IMAGE AS "RGBA"
        # img_data = pg.image.tostring(image, 'RGBA')
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        # DECOMMENT NEXT LINE FOR COLORED FORMAT
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        # glGenerateMipmap(GL_TEXTURE_2D)
        

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def unbind(self):
        glBindTexture(GL_TEXTURE_2D,0)