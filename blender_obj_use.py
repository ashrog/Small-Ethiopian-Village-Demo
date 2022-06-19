from OpenGL.GL import *
from OpenGL.GL.shaders import *
import numpy as np
import os


class BlenderObject:

    def __init__(self, filename):
        # x, y, z, s, t, nx, ny, nz
        self.vertices = self.loadMesh(filename)
        # self.vertices_2 = self.loadMesh(filename_2)
        self.vertex_count = len(self.vertices) // 8
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.objVAO = glGenVertexArrays(1)
        glBindVertexArray(self.objVAO)

        self.objVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.objVBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))


    def getFileContents(filename):
        p = os.path.join(os.getcwd(), "model", filename)
        return open(p, 'r').readline()
    
    def loadMesh(self, filename):
        v = []
        vt = []
        vn = []

        #v, vt, vn finally become one in vertices
        vertices = []

        # open the obj file and read the data
        
        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]
                if flag == "v":
                    # vertex
                    line = line.replace("v ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)
                elif flag == "vt":
                    # texture coordinate
                    line = line.replace("vt ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)
                elif flag == "vn":
                    # normal
                    line = line.replace("vn ", "")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)
                elif flag == "f":
                    # face, three or more vertices in v/vt/vn form
                    line = line.replace("f ", "")
                    line = line.replace("\n", "")
                    # get the individual vertices for each line
                    line = line.split(" ")
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    for vertex in line:
                        # break out into [v,vt,vn],
                        # correct for 0 based indexing.
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(v[position])
                        texture = int(l[1]) - 1
                        faceTextures.append(vt[texture])
                        normal = int(l[2]) - 1
                        faceNormals.append(vn[normal])
                    #unpack each face with a triangle format.
                   
                    triangles_per_face = len(line) - 2

                    vertex_order = []
                 
                    for i in range(triangles_per_face):
                        vertex_order.append(0)
                        vertex_order.append(i + 1)
                        vertex_order.append(i + 2)
                    for i in vertex_order:
                        for x in faceVertices[i]:
                            vertices.append(x)
                        for x in faceTextures[i]:
                            vertices.append(x)
                        for x in faceNormals[i]:
                            vertices.append(x)
                line = file.readline()
        return vertices

    def unbind(self):
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)