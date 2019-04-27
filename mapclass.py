import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open((filename), "rt") as f:
            for line in f:
                self.data.append(line)

        self.tilewidth = len(self.data[0])
        self.tielheight = len(self.data)
        self.width = self.tilewidth * Tilesize
        self.height = self.tielheight * Tilesize