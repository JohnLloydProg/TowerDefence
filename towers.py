import pygame
import projectiles


class Tower:
    def __init__(self, c, r):
        self.r = r
        self.c = c
        self.attack_speed = 0
        self.attack_speed_bar = 0
        self.image = pygame.image.load('images/towers/Default_Tower_img.jpg')

    def draw(self, win):
        win.blit(self.image, (self.c*100, self.r*100))


class Archer(Tower):
    def __init__(self, c, r):
        Tower.__init__(self, c, r)
        self.attack_speed = 1.2
        self.attack_speed_bar = 0
        self.range = 500
        self.image = pygame.image.load('images/towers/Archer_Tower_img.jpg')

    def attack(self, projectiles_list, target_coordinates):
        if self.attack_speed_bar >= 5:
            projectiles_list.append(projectiles.Arrow((self.c*100)+50, (self.r*100)+50, 50, 20, target_coordinates))
            self.attack_speed_bar = 0


class Cannon(Tower):
    def __init__(self, c, r):
        Tower.__init__(self, c, r)
        self.attack_speed = 0.8
        self.attack_speed_bar = 0
        self.range = 300
        self.color = (0, 0, 255)
        self.image = pygame.image.load('images/towers/Cannon_Tower_img.jpg')

    def attack(self, projectiles_list, target_coordinates):
        if self.attack_speed_bar >= 5:
            projectiles_list.append(projectiles.CannonBall((self.c*100)+50, (self.r*100)+50, 50, 50, target_coordinates))
            self.attack_speed_bar = 0


class Mage(Tower):
    def __init__(self, c, r):
        Tower.__init__(self, c, r)
        self.range = 400
        self.attack_speed = 1
        self.attack_speed_bar = 0
        self.color = (0, 255, 0)
        self.image = pygame.image.load('images/towers/Mage_Tower_img.jpg')

    def attack(self, projectiles_list, target_coordinates):
        if self.attack_speed_bar >= 5:
            projectiles_list.append(projectiles.Bolt((self.c*100)+50, (self.r*100)+50, 50, 20, target_coordinates))
            self.attack_speed_bar = 0
