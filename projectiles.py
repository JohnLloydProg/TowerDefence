import pygame
import math


class Projectile:
    def __init__(self, x, y, w, h, target_coordinates):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = 0
        self.target_coordinates = target_coordinates
        distance_x = self.target_coordinates[0] - self.x
        distance_y = self.target_coordinates[1] - self.y
        distance = math.hypot(distance_x, distance_y)
        self.dx = distance_x / distance
        self.dy = distance_y / distance

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed


class CannonBall(Projectile):
    def __init__(self, x, y, w, h, target_coordinates):
        Projectile.__init__(self, x, y, w, h, target_coordinates)
        self.penetration = 50
        self.damage = 150
        self.speed = 20
        self.aoe_range = 300
        self.image = pygame.image.load('images/projectiles/CannonBall_img.png')

    def target_reached(self):
        distance_x = self.target_coordinates[0] - self.x
        distance_y = self.target_coordinates[1] - self.y
        distance = math.hypot(distance_x, distance_y)
        if distance <= 50:
            return True

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Arrow(Projectile):
    def __init__(self, x, y, w, h, target_coordinates):
        Projectile.__init__(self, x, y, w, h, target_coordinates)
        self.penetration = 150
        self.damage = 100
        self.speed = 30
        self.orig_image = pygame.image.load('images/projectiles/Arrow_img.png')
        self.image = self.orig_image
        try:
            degree_rotation = math.degrees(math.atan((y - target_coordinates[1]) / (x - target_coordinates[0])))
            self.image = pygame.transform.rotate(self.orig_image, -degree_rotation)
        except ZeroDivisionError:
            self.image = pygame.transform.rotate(self.orig_image, 90)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Bolt(Projectile):
    def __init__(self, x, y, w, h, target_coordinates):
        Projectile.__init__(self, x, y, w, h, target_coordinates)
        self.penetration = 30
        self.damage = 200
        self.speed = 25
        self.orig_image = pygame.image.load('images/projectiles/LightBolt_img.png')
        self.image = self.orig_image
        try:
            degree_rotation = math.degrees(math.atan((y - target_coordinates[1]) / (x - target_coordinates[0])))
            self.image = pygame.transform.rotate(self.orig_image, -degree_rotation)
        except ZeroDivisionError:
            self.image = pygame.transform.rotate(self.orig_image, 90)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
