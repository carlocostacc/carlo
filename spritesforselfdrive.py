from settings import*
import pygame
import math
import time
from math import tan, radians, degrees, copysign, sqrt
import random
vec = pygame.math.Vector2


class Voitures(pygame.sprite.Sprite):

    def __init__(self, game, x, y, angle=0.0):
        self.groups = game.all_sprites, game.voiture
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.decision = 1
        self.game = game
        self.image = game.voiture_img
        self.image_clean = self.image.copy()
        self.rect = self.image_clean.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.speed = vec(0.0, 0.0)
        self.x_speed = self.speed.x
        self.max_speed = 100
        self.acc = vec(8, 0)
        self.max_acceleration = 7.5
        self.rot = 0
        self.last_update = pygame.time.get_ticks()
        self.steering = 0.0
        self.width = 25
        self.height = car_height
        self.angle = angle
        self.ppu = 100
        self.brake = 3
        self.speed_vector = [self.pos]

    def update_speed_vector(self, newpos):
        if len(self.speed_vector) == 1:
            self.speed_vector.append(newpos)
        if len(self.speed_vector) == 2:
            del self.speed_vector[0]
            self.speed_vector.append(newpos)


    def collide_with_building(self):
        if self.rect.x < 0:
            return False
        if self.rect.x > display_width - Tilesize:
            return False
        if self.rect.y < 0:
            self.rect.y = 0 + 3*car_height
            return False
        if self.rect.y > display_height - Tilesize:
            return False
        if pygame.sprite.spritecollideany(self, self.game.buildings):
            print("collide")
            return False
        if self.pos.x > (self.rect.x + self.rect.width):
            # collision avec autre voiture
            return False
        elif (self.pos.x + self.width) < self.rect.x:
            # collision avec autre voiture
            return False
        elif (self.pos.y + self.height) < self.rect.y:
            # collision avec autre voiture
            return False
        elif self.pos.y > (self.rect.y + self.rect.height):
            # collision avec autre voiture
            return False
        for building in self.game.buildings :
            if self.rect.x + car_width > building.rect.x and self.rect.x < building.rect.x + 2*Tilesize and self.rect.y + car_height > building.rect.y and self.rect.y < building.rect.y + 2*Tilesize:
                return False

            else:
                return True
    def update(self):
        self.mouvement_x()
        print(self.speed_vector)





    def deceleration_for_x_pos(self, finalpoint):
        self.acc = vec((-(self.speed.x *self.speed.x)/(2*(finalpoint - self.pos.x))), 0)
        print(self.acc)
        while self.speed != vec(0, 0) and self.speed.x > 0.7:
            self.speed += self.acc * self.game.dt
            self.pos = vec((self.pos.x + self.speed.x * self.game.dt + 0.5 * self.acc.x * math.pow(self.game.dt,2)), self.pos.y)
        self.now = pygame.time.Clock().tick()
        self.stop = 0
        if self.speed.x <= 0.7:
            while self.stop - self.now < 1:
                self.stop = pygame.time.Clock().tick()
                self.speed = vec(0, 0)
        self.now = 0
        self.stop = 0
        print("passed")

        self.acc = vec(0.5, 0)
        pass
    def mouvement_y(self):
        if self.collide_with_building():
            self.speed = vec(0, self.speed.x)
            self.speed += self.acc * self.game.dt
            self.speed.y = max(-self.max_speed, min(self.speed.y, self.max_speed))
            if self.steering:
                turning_radius = self.width / tan(radians(self.steering))
                angular_velocity = self.speed.y / turning_radius
                angular_acceleration = (self.acc.x) / turning_radius
            else:
                angular_velocity = 0
                angular_acceleration = 0
            self.angle += degrees(angular_velocity) * self.game.dt + 0.5 * degrees(
                angular_acceleration) * self.game.dt ** 2
            self.pos += self.speed.rotate(self.angle) * self.game.dt + 0.5 * self.acc.rotate(
                self.angle) * self.game.dt ** 2
            self.image = pygame.transform.rotate(self.image_clean, -self.angle)
            self.rect.center = self.pos
            self.rect = self.image.get_rect(center=self.rect.center)

    def mouvement_x(self):
        self.update_speed_vector(self.pos)
        if self.collide_with_building():
            self.speed += self.acc * self.game.dt
            self.speed.x = max(-self.max_speed, min(self.speed.x, self.max_speed))
            if self.steering:
                turning_radius = self.width / tan(radians(self.steering))
                angular_velocity = self.speed.x / turning_radius
                angular_acceleration = (self.acc.x) / turning_radius
            else:
                angular_velocity = 0
                angular_acceleration = 0
            self.angle += degrees(angular_velocity) * self.game.dt + 0.5 * degrees(
                angular_acceleration) * self.game.dt ** 2
            self.pos += self.speed.rotate(self.angle) * self.game.dt + 0.5 * self.acc.rotate(
                self.angle) * self.game.dt ** 2
            self.image = pygame.transform.rotate(self.image_clean, -self.angle)
            self.rect.center = self.pos
            self.rect = self.image.get_rect(center=self.rect.center)

            for intersection in self.game.intersection:
                if 0.75 * Tilesize > intersection.x - self.pos.x:
                    self.brake = -(intersection.x - self.pos.x - 0.75 * Tilesize - ((self.speed.x)) * 2)
                    if 55 > self.brake > 11:
                        if self.speed.x > 0:
                            self.brake = intersection.x - self.pos.x + (
                                        -(self.speed.x) * self.game.dt) * 2 / self.game.dt ** 2
                            self.acc.x = -copysign(self.brake, self.speed.x)
                            self.rect.center = self.pos
                            self.rect = self.image.get_rect(center=self.rect.center)
                    self.acc = vec(5, 0)

                    #
                    self.decision = random.randrange(0, 4)
                if self.decision == 1:
                    # print("drete")
                    self.acc = vec(5, 0)
                elif self.decision == 2:
                    # print("turn left")
                    if 5 * Tilesize < self.pos.x < 6.5 * Tilesize or 10 * Tilesize < self.pos.x < 13 * Tilesize or 15 * Tilesize < self.pos.x < 18 * Tilesize or 20 * Tilesize < self.pos.x < 23 * Tilesize or 25 * Tilesize < self.pos.x < 28 * Tilesize or 30 * Tilesize < self.pos.x < 33 * Tilesize:
                        if self.angle <= 90:
                            self.steering = 30
                            print(self.angle)

                        else:
                            self.steering = 0.0
                            self.angle = 90

                        # print("turn left")
                elif self.decision == 3:
                    # print("turn right")
                    if 5 * Tilesize < self.pos.x < 6.5 * Tilesize or 10 * Tilesize < self.pos.x < 13 * Tilesize or 15 * Tilesize < self.pos.x < 18 * Tilesize or 20 * Tilesize < self.pos.x < 23 * Tilesize or 25 * Tilesize < self.pos.x < 28 * Tilesize or 30 * Tilesize < self.pos.x < 33 * Tilesize:
                        if self.angle <= 90:
                            self.steering = 30
                            print(self.angle)

                        else:
                            self.steering = 0.0
                            self.angle = 90
                    # while self.speed.rotate(self.angle).y < 6:
                    #     self.speed += (self.acc * self.game.dt)
                    #     self.speed.x = max(-self.max_speed, min(self.speed.x, self.max_speed))
                    #     turning_radius = 1.4 * Tilesize
                    #     angular_velocity = self.speed.x / turning_radius
                    #     angular_acceleration = (self.acc.x) / turning_radius
                    #     self.angle += degrees(angular_velocity) * self.game.dt + 0.5 * degrees(
                    #         angular_acceleration) * self.game.dt ** 2
                    #     self.pos += self.speed.rotate(self.angle) * self.game.dt + 0.5 * self.acc.rotate(
                    #         self.angle) * self.game.dt ** 2
                    #     print(self.speed.rotate(self.angle))
                    #     self.image = pygame.transform.rotate(self.image_clean, -self.angle)
                    #     self.rect.center = self.pos
                    #     self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.center = self.pos
        self.rect = self.image.get_rect(center=self.rect.center)


class Building(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.buildings
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((Tilesize, Tilesize))
        self.image.fill(brown)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * Tilesize
        self.rect.y = y * Tilesize

class Intersection(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.intersection
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((2*Tilesize, 2*Tilesize))
        self.image.fill(white)
        self.image.set_alpha(0.11)
        self.rect = self.image.get_rect()
        self.x = x * Tilesize
        self.y = y * Tilesize
        self.rect.x = self.x
        self.rect.y = self.y

