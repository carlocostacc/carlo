import pygame
vec = pygame.math.Vector2
from random import shuffle

pygame.init()
display_width = 1250
display_height = 650
car_width = 25
car_height = 40
black = (0, 0, 0)
white = (255, 255, 255)
white2 = (252, 244, 239)
brown = (127, 58, 12)
size = 150
FPS = 90
car_x = 0
car_y = 200
bouger = 6
thingsx = 0
int_size = 2*car_width
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("voitures autonomes")

clock = pygame.time.Clock()

# creation de la classe voiture
# model = image


class Voitures(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image + ".png")
        self.rect = self.image.get_rect()
        self.image = pygame.transform.smoothscale(self.image, (car_width, car_height))
        self.rot = -90
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.vel = 0
        self.rot_speed = 0
        self.display = screen.blit(self.image, (self.x, self.y))



# fonction de vitesse a l'interieur de la classe voiture

    def speed(self):

        print(self.x)

        if self.x > display_width:
            self.x = 1200




# ne fonctionne pas encore mais cest la fonction pour faire tourner la voiture au interrcection

    def rotate(self):

        global bouger


    def rotation_motion(self):

        self.rot_speed = 20

        num_of_rotation = 0

        while num_of_rotation >= 6:

            #pygame.time.wait(int(rotation/FPS))

            self.model = pygame.transform.rotate(self.model, self.rot_speed)

            num_of_rotation = num_of_rotation + 1

    def update(self):
        pass





# creation de la classe building

# skin = image utiliser


# je cree mes instances de class

car1 = Voitures("car1", 0, 0)

voitures_sprites = pygame.sprite.Group()

voitures_sprites.add(car1)

grid_EXIT = False
#
# all_sprites = pygame.sprite.Group()
# player = Player()
# all_sprites.add(player)
# main loop de l'application ou tt ce fait call

while not grid_EXIT:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            quit()
    screen.fill(white2)
    voitures_sprites.draw(screen)
    clock.tick(FPS)

pygame.quit()
quit()