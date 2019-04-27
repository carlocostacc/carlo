import pygame as pg
import sys
from os import path
from settings import voiture_img
from spritesforselfdrive import *
from mapclass import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((display_width, display_height))
        #pg.display.set_caption("voitures autonomes")
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def load_data(self):
        self.voiture_img = pg.image.load(voiture_img)
        self.voiture_img = pg.transform.scale(self.voiture_img, (Tilesize, int(2*Tilesize/3)))
        self.map = Map(path.join("C:/Users/Bessy/PycharmProjects/project self driving", "map.txt"))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.buildings = pg.sprite.Group()
        self.voiture = pg.sprite.Group()
        self.intersection = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Building(self, col, row)
                if tile == "p":
                    Voitures(self, (Tilesize) * (col + 1), (row+1) * (Tilesize) - int(Tilesize/2))


                if tile == "i":
                    Intersection(self, col, row)



    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def draw_grid(self):
        for x in range(0, display_width, Tilesize):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, display_height))
        for y in range(0, display_height, Tilesize):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (display_width, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(white)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()