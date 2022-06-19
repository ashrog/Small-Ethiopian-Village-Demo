import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import numpy as np
import pyrr
import blender_obj_use
import  texture_image


class RenderedDisplay:

    def __init__(self):
       
        pg.init()
        display = (1850, 970)
        pg.display.set_mode(display, pg.OPENGL | pg.DOUBLEBUF)
        
        
        glClearColor(01.0, 1.0, 1.0, 1)
       
        self.prog = self.shader_program()
        glUseProgram(self.prog)
        
        tex_location = glGetUniformLocation(self.prog, "imageTexture")
        glUniform1i(tex_location, 0)
        glEnable(GL_DEPTH_TEST)

        self.wood_texture = texture_image.Texture()
        self.objs_mesh = blender_obj_use.BlenderObject("model/3_house_village_1.obj")


        projection_matrix = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=700 / 500,
            # near and far show where the plane is, behind plane or infront of plane.
            near=0.1, far=50, dtype=np.float32
        )
        
        projection_location =  glGetUniformLocation(self.prog, "projection")
        
        glUniformMatrix4fv(projection_location,
            1, GL_FALSE, projection_matrix
        )
        
        self.modelLocation = glGetUniformLocation(self.prog, "model")
        self.viewLocation = glGetUniformLocation(self.prog, "view")


    def shader_program(self):
        vertex_path = open("shaders_file/triangle.vertex.shader" , 'r').read()
        fragment_path = open("shaders_file/triangle.fragment.shader" , 'r').read()

        vertex_shader = compileShader(vertex_path, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_path, GL_FRAGMENT_SHADER)

        program = compileProgram(vertex_shader,fragment_shader)

        return program

    def render_object(self, scene):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.prog)

        view_matrix = pyrr.matrix44.create_look_at(
            # current view
            eye = scene.demoView.position,
            
            # after moving
            target = scene.demoView.position + scene.demoView.forwards,
            up =scene.demoView.up,
            dtype =np.float32
        )
        glUniformMatrix4fv(self.viewLocation, 1, GL_FALSE, view_matrix)

        for objs in scene.objectsOne:
            # created an identity matrix so it can also work for translation
            model_matrixT = np.array([
                [1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]
            ])
            # get from key incase we added rotation
            
            model_matrixT = pyrr.matrix44.multiply(
                m1=model_matrixT,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(objs.position),
                    dtype=np.float32)
                # m2 = np.array(objs.position, dtype = np.float32)
                
            )
            
            glUniformMatrix4fv(self.modelLocation, 1, GL_FALSE, model_matrixT)
            
            self.wood_texture.use()
            glBindVertexArray(self.objs_mesh.objVAO)
            glDrawArrays(GL_TRIANGLES, 0, self.objs_mesh.vertex_count)

            pg.display.flip()

    def unbind(self):
        self.objs_mesh.unbind()
        self.wood_texture.unbind()
        glDeleteProgram(self.prog)
        pg.quit()