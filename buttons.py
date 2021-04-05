import pygame


class Button:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = (0, 0, 0)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))

    def is_inside(self):
        mx, my = pygame.mouse.get_pos()
        if self.x+self.w >= mx >= self.x and self.y+self.h >= my >= self.y:
            return True


class TowerButton(Button):
    def __init__(self, x, y, w, h, image):
        Button.__init__(self, x, y, w, h)
        self.image = image
        self.cant_afford_screen = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.cant_afford_screen.fill((0, 0, 0, 125))
        self.affordable = True

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        if not self.affordable:
            win.blit(self.cant_afford_screen, (self.x, self.y))


class GUIButton(Button):
    def __init__(self, x, y, w, h, text, text_color, text_hover_color, text_pos, image, hover_image):
        Button.__init__(self, x, y, w, h)
        self.font = pygame.font.SysFont("None", 50)
        self.text = text
        self.orig_image = image
        self.image = image
        self.hover_image = hover_image
        self.orig_text_color = text_color
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.text_pos = text_pos

    def draw(self, win):
        win.blit(pygame.transform.scale(self.image, (self.w, self.h)), (self.x, self.y))
        win.blit(self.font.render(self.text, True, self.text_color), (self.x+self.text_pos[0], self.y+self.text_pos[1]))

