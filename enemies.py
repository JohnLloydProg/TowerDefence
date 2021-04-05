import pygame


class Enemy:
    def __init__(self, grid):
        self.x = None
        self.y = None
        self.w = 90
        self.h = 90
        self.path_coordinates = []
        self.end_coordinate = None
        self.color = (0, 0, 0)
        self.plan_path(grid)
        self.health = 100
        self.full_health = self.health
        self.orig_image = pygame.image.load('images/enemies/Light_Enemy_img.png')
        self.image = self.orig_image

    def plan_path(self, grid):
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == "path":
                    self.path_coordinates.append((c, r))
                elif grid[r][c] == "start":
                    self.x = (c*100)+5
                    self.y = (r*100)+5
        self.path_coordinates.sort(key=lambda x: x[0])

    def is_finished(self):
        if len(self.path_coordinates) == 0:
            return True

    def move(self):
        if self.x < self.path_coordinates[0][0]*100:
            self.x += 5
            self.image = self.orig_image
        elif self.x > self.path_coordinates[0][0]*100:
            self.x -= 5
            self.image = pygame.transform.rotate(self.orig_image, 180)
        else:
            if self.y < self.path_coordinates[0][1] * 100:
                self.y += 5
                self.image = pygame.transform.rotate(self.orig_image, -90)
            elif self.y > self.path_coordinates[0][1] * 100:
                self.y -= 5
                self.image = pygame.transform.rotate(self.orig_image, 90)
            else:
                if len(self.path_coordinates) > 0:
                    self.path_coordinates.pop(0)

    def get_pos(self):
        return self.x, self.y

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y-15, self.w, 10))
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y-15, int((self.health/self.full_health)*self.w), 10))
        win.blit(self.image, (self.x, self.y))


class LightEnemy(Enemy):
    def __init__(self, grid):
        Enemy.__init__(self, grid)
        self.gold_drop = 35
        self.health = 500
        self.armor = 50
        self.color = (255, 0, 255)
        self.full_health = self.health
        self.orig_image = pygame.image.load('images/enemies/Light_Enemy_img.png')
        self.image = self.orig_image


class HeavyEnemy(Enemy):
    def __init__(self, grid):
        Enemy.__init__(self, grid)
        self.health = 750
        self.gold_drop = 150
        self.armor = 150
        self.color = (0, 255, 255)
        self.full_health = self.health
        self.orig_image = pygame.image.load('images/enemies/Heavy_Enemy_img.png')
        self.image = self.orig_image


class MediumEnemy(Enemy):
    def __init__(self, grid):
        Enemy.__init__(self, grid)
        self.health = 500
        self.gold_drop = 75
        self.armor = 100
        self.color = (255, 255, 0)
        self.full_health = self.health
        self.orig_image = pygame.image.load('images/enemies/Medium_Enemy_img.png')
        self.image = self.orig_image
