import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import ctypes


class App:


    #init python
    def __init__(self):
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #init opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        self.shader = self.creatShader("Texturs/shaders/vert.vert", "Texturs/shaders/frag.frag")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        self.triangle = Tri()
        self.wood_texture = Material("Texturs/textur/wood.jpeg")
        self.mainLoop()
    

    def creatShader(self, vertexFilePath, fragmentFilePath):

        with open(vertexFilePath, 'r') as v:
            vertex_src = v.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader


    def mainLoop(self):
        running = True
        while (running):
            #check events 
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            self.wood_texture.use()
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            #time
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit() 


class Tri:


    def __init__(self):

        #x, y, z, r, g, b, s, t
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 
             0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
             0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0
        )
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def destroy(self):

        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


class Material:

    def __init__(self, filePath):
        
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filePath).convert()
        image_with, image_hight = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_with, image_hight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)


    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))




if __name__ == "__main__":
    myApp = App()

