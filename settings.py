import pygame

display_width = 1024
display_height = 544
black = (0, 0, 0)
white = (255, 255, 255)
white2 = (252, 244, 239)
red = (255, 0,0)
brown = (127, 58, 12)
LIGHTGREY = (1, 1, 1)
size = 150
FPS = 90
car_x = 0
car_y = 200
bouger = 6
thingsx = 0
voiture_img = ("car.png")
Tilesize = 32
gridwidth = display_width/Tilesize
gridheigt= display_height/Tilesize
car_mass = 4000*1000
force_app = 0
car_acc = force_app*car_mass
car_width = 4
car_height = int(2*Tilesize/3)
int_size = 2*car_width
