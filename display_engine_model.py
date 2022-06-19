import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import numpy as np
import pyrr
import blender_obj_use
import  texture_image


class GraphicsEngine:

    def __init__(self):
        # initialise pygame
        pg.init()
        pg.mouse.set_visible(False)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode((1850, 970), pg.OPENGL | pg.DOUBLEBUF)
        # initialise opengl
        glClearColor(1.0, 1.0, 1.0, 1.0)
        # self.prog = self.createShader("shaders_file/triangle.vertex.shader", "shaders_file/triangle.fragment.shader")
        self.prog = self.shader_program()
        glUseProgram(self.prog)
        glUniform1i(glGetUniformLocation(self.prog, "imageTexture"), 0)
        glEnable(GL_DEPTH_TEST)

        self.wood_texture = texture_image.Material("images/door_2.jpg")
        self.cube_mesh = blender_obj_use.Mesh("model/3_house_village_1.obj")


        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=0.1, far=50, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.prog, "projection"),
            1, GL_FALSE, projection_transform
        )
        self.modelMatrixLocation = glGetUniformLocation(self.prog, "model")
        self.viewMatrixLocation = glGetUniformLocation(self.prog, "view")


    def shader_program(self):
        vertex_path = open("shaders_file/triangle.vertex.shader" , 'r').readlines()
        fragment_path = open("shaders_file/triangle.fragment.shader" , 'r').readlines()

        vertex_shader = compileShader(vertex_path, GL_VERTEX_SHADER)

        fragment_shader = compileShader(fragment_path, GL_FRAGMENT_SHADER)

        program = compileProgram(vertex_shader,fragment_shader)

        return program

    def render(self, scene):
        # refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.prog)

        view_transform = pyrr.matrix44.create_look_at(
            eye=scene.player.position,
            target=scene.player.position + scene.player.forwards,
            up=scene.player.up,
            dtype=np.float32
        )
        glUniformMatrix4fv(self.viewMatrixLocation, 1, GL_FALSE, view_transform)

        for cube in scene.cubes:
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(cube.eulers),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(cube.position),
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            self.wood_texture.use()
            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            pg.display.flip()

    def unbind(self):
        self.cube_mesh.unbind()
        self.wood_texture.unbind()
        glDeleteProgram(self.prog)
        pg.quit()