import pygame as pg
from OpenGL.GL import *


class App:


    #init python
    def __init__(self) -> None:
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #init opengl
        glClearColor(0.1, 0.2, 0.2, 1)