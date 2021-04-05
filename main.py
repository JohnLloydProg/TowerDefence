import pygame
import projectiles
import buttons
import math
import pandas
import towers
import enemies
import os


class Game:
    def __init__(self, width, height, name):
        pygame.init()
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.main()

    def main(self):
        play_button = buttons.GUIButton(790, 630, 200, 75, "Play", (143, 120, 92), (178, 145, 107), (65, 20),
                                        pygame.image.load('images/buttons/gui_button_img.png'), pygame.image.load('images/buttons/gui_button_hoverimg.png'))
        exit_button = buttons.GUIButton(790, 715, 200, 75, "Exit", (143, 120, 92), (178, 145, 107), (65, 20),
                                        pygame.image.load('images/buttons/gui_button_img.png'), pygame.image.load('images/buttons/gui_button_hoverimg.png'))
        background_img = pygame.image.load('images/background_img.jpeg')
        background_screen = pygame.Surface((1000, 800), pygame.SRCALPHA)
        background_screen.fill((0, 0, 0, 125))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if play_button.is_inside():
                    play_button.image = play_button.hover_image
                    play_button.text_color = play_button.text_hover_color
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.map_selection()
                elif exit_button.is_inside():
                    exit_button.image = exit_button.hover_image
                    exit_button.text_color = exit_button.text_hover_color
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.quit()
                        quit()
                else:
                    play_button.image = play_button.orig_image
                    play_button.text_color = play_button.orig_text_color
                    exit_button.image = exit_button.orig_image
                    exit_button.text_color = exit_button.orig_text_color

            self.win.blit(pygame.transform.scale(background_img, (1000, 800)), (0, 0))
            self.win.blit(background_screen, (0, 0))
            play_button.draw(self.win)
            exit_button.draw(self.win)
            pygame.display.update()
            self.clock.tick(60)

    def map_selection(self):
        maps = []
        for i, name in enumerate(os.listdir(os.curdir+'/maps')):
            maps.append(buttons.GUIButton(690, 10+(110*i), 300, 75, name, (143, 120, 92), (178, 145, 107), (20, 20),
                                          pygame.image.load('images/buttons/map_selection_img.png'), pygame.image.load('images/buttons/map_selection_hoverimg.png')))
        back_button = buttons.GUIButton(10, 10, 130, 65, "Back", (143, 120, 92), (178, 145, 107), (25, 15),
                                        pygame.image.load('images/buttons/gui_button_img.png'), pygame.image.load('images/buttons/gui_button_hoverimg.png'))
        background_img = pygame.image.load('images/background_img.jpeg')
        background_screen = pygame.Surface((1000, 800), pygame.SRCALPHA)
        background_screen.fill((0, 0, 0, 125))
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if back_button.is_inside():
                    back_button.image = back_button.hover_image
                    back_button.text_color = back_button.text_hover_color
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        run = False
                        self.main()
                else:
                    back_button.image = back_button.orig_image
                    back_button.text_color = back_button.orig_text_color
                for choice_map in maps:
                    if choice_map.is_inside():
                        choice_map.image = choice_map.hover_image
                        choice_map.text_color = choice_map.text_hover_color
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            self.game(choice_map.text)
                    else:
                        choice_map.image = choice_map.orig_image
                        choice_map.text_color = choice_map.orig_text_color

            self.win.blit(pygame.transform.scale(background_img, (1000, 800)), (0, 0))
            self.win.blit(background_screen, (0, 0))
            back_button.draw(self.win)
            for choice_map in maps:
                choice_map.draw(self.win)
            pygame.display.update()
            self.clock.tick(60)

    def game(self, name):
        cannon_button = buttons.TowerButton(910, 715, 80, 80, pygame.image.load('images/buttons/Cannon_Button_img.png'))
        archer_button = buttons.TowerButton(820, 715, 80, 80, pygame.image.load('images/buttons/Archer_Button_img.png'))
        mage_button = buttons.TowerButton(730, 715, 80, 80, pygame.image.load('images/buttons/Mage_Button_img.png'))
        start_button = buttons.TowerButton(10, 715, 80, 80, pygame.image.load('images/buttons/Start_Button_img.png'))
        path_img = pygame.image.load(f'maps/{name}/path_img.jpg')
        land_img = pygame.image.load(f'maps/{name}/land_img.jpg')
        archer_tower_img = pygame.image.load('images/towers/Archer_Tower_img.jpg')
        mage_tower_img = pygame.image.load('images/towers/Mage_Tower_img.jpg')
        cannon_tower_img = pygame.image.load('images/towers/Cannon_Tower_img.jpg')
        grid_df = pandas.read_excel(f'maps/{name}/grid_layout.xlsx')
        grid = [grid_df.iloc[0], grid_df.iloc[1], grid_df.iloc[2], grid_df.iloc[3], grid_df.iloc[4], grid_df.iloc[5],
                grid_df.iloc[6]]
        round_df = pandas.read_excel(f'maps/{name}/rounds.xlsx')
        not_placeable_screen = pygame.Surface((100, 100), pygame.SRCALPHA)
        not_placeable_screen.fill((255, 0, 0, 125))
        planted_towers = []
        spawned_enemies = []
        enemies_to_spawn = []
        spawned_projectiles = []
        wave = 0
        lives = 3
        gold = 800
        selected = None
        placeable = False
        tick = pygame.USEREVENT+1
        spawn = pygame.USEREVENT+2
        pygame.time.set_timer(tick, 100)
        font = pygame.font.SysFont("None", 50)
        round_playing = False
        run = True
        while run:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y < 700:
                r = mouse_y // 100
            else:
                r = 6
            c = mouse_x // 100
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if selected and mouse_y < 700:
                    if not grid[r][c]:
                        placeable = True
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if selected == "cannon":
                                planted_towers.append(towers.Cannon(c, r))
                                gold -= 300
                            elif selected == "archer":
                                planted_towers.append(towers.Archer(c, r))
                                gold -= 200
                            else:
                                planted_towers.append(towers.Mage(c, r))
                                gold -= 400
                            grid[r][c] = True
                            selected = None
                    else:
                        placeable = False
                if event.type == tick:
                    for tower in planted_towers:
                        tower.attack_speed_bar += tower.attack_speed
                if event.type == spawn:
                    if enemies_to_spawn[2] > 0:
                        spawned_enemies.append(enemies.LightEnemy(grid))
                        enemies_to_spawn[2] -= 1
                    elif enemies_to_spawn[1] > 0:
                        spawned_enemies.append(enemies.MediumEnemy(grid))
                        enemies_to_spawn[1] -= 1
                    else:
                        spawned_enemies.append(enemies.HeavyEnemy(grid))
                        enemies_to_spawn[0] -= 1

                if gold >= 300:
                    cannon_button.affordable = True
                    if cannon_button.is_inside():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            selected = "cannon"
                else:
                    cannon_button.affordable = False
                if gold >= 200:
                    archer_button.affordable = True
                    if archer_button.is_inside():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            selected = "archer"
                else:
                    archer_button.affordable = False
                if gold >= 400:
                    mage_button.affordable = True
                    if mage_button.is_inside():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            selected = "mage"
                else:
                    mage_button.affordable = False
                if start_button.is_inside() and not round_playing:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        try:
                            enemies_to_spawn = round_df.iloc[wave]
                            number_loop = enemies_to_spawn[0] + enemies_to_spawn[1] + enemies_to_spawn[2]
                            pygame.time.set_timer(spawn, 500, number_loop)
                            round_playing = True
                        except IndexError:
                            run = False
                            self.map_selection()

            if round_playing and len(spawned_enemies) == 0:
                round_playing = False
                wave += 1
            if lives <= 0:
                run = False
                self.map_selection()

            self.win.fill((255, 255, 255))
            for row in range(len(grid)):
                for col in range(len(grid[r])):
                    if grid[row][col] == "path" or grid[row][col] == "start":
                        self.win.blit(path_img, (col*100, row*100))
                    else:
                        self.win.blit(land_img, (col*100, row*100))
            for tower in planted_towers:
                tower.draw(self.win)
                for enemy in spawned_enemies:
                    dx = (tower.c*100)+50 - enemy.x+(enemy.w/2)
                    dy = (tower.r*100)+50 - enemy.y+(enemy.h/2)
                    if math.hypot(dx, dy) <= tower.range:
                        tower.attack(spawned_projectiles, enemy.get_pos())
            for enemy in spawned_enemies:
                enemy.move()
                if enemy.is_finished():
                    spawned_enemies.remove(enemy)
                    lives -= 1
                if enemy.health <= 0:
                    spawned_enemies.remove(enemy)
                    gold += enemy.gold_drop
                enemy.draw(self.win)
            for projectile in spawned_projectiles:
                projectile.move()
                if isinstance(projectile, projectiles.CannonBall):
                    if projectile.target_reached():
                        for enemy in spawned_enemies:
                            dx = projectile.x+25 - enemy.x + (enemy.w / 2)
                            dy = projectile.y+25 - enemy.y + (enemy.h / 2)
                            if math.hypot(dx, dy) <= projectile.aoe_range:
                                if projectile.penetration >= enemy.armor:
                                    enemy.health -= projectile.damage
                                else:
                                    enemy.health -= projectile.damage - (enemy.armor - projectile.penetration)
                        spawned_projectiles.remove(projectile)
                elif isinstance(projectile, projectiles.Arrow):
                    for enemy in spawned_enemies:
                        dx = projectile.x + 25 - enemy.x + (enemy.w / 2)
                        dy = projectile.y + 10 - enemy.y + (enemy.h / 2)
                        if math.hypot(dx, dy) <= 60:
                            if projectile.penetration >= enemy.armor:
                                enemy.health -= projectile.damage
                            else:
                                enemy.health -= (projectile.damage - (enemy.armor - projectile.penetration))
                            spawned_projectiles.remove(projectile)
                            break
                else:
                    for i, enemy in enumerate(spawned_enemies):
                        dx = projectile.x + 25 - enemy.x + (enemy.w / 2)
                        dy = projectile.y + 10 - enemy.y + (enemy.h / 2)
                        if math.hypot(dx, dy) <= 60:
                            for chained_enemy in spawned_enemies[i:i+3]:
                                if projectile.penetration >= chained_enemy.armor:
                                    chained_enemy.health -= projectile.damage
                                else:
                                    chained_enemy.health -= (projectile.damage - (chained_enemy.armor - projectile.penetration))
                            spawned_projectiles.remove(projectile)
                            break
                if 0 > projectile.x > 1000 or 0 > projectile.y > 800:
                    spawned_projectiles.remove(projectile)
                projectile.draw(self.win)
            if selected:
                if selected == "cannon":
                    self.win.blit(cannon_tower_img, (c*100, r*100))
                elif selected == "archer":
                    self.win.blit(archer_tower_img, (c*100, r*100))
                else:
                    self.win.blit(mage_tower_img, (c * 100, r * 100))
                if not placeable:
                    self.win.blit(not_placeable_screen, (c*100, r*100))
            self.win.blit(pygame.image.load('images/Game_GUI_img.png'), (0, 0))
            for life in range(lives):
                self.win.blit(pygame.image.load('images/Heart_img.png'), (10 + (life * 50), 5))
            cannon_button.draw(self.win)
            archer_button.draw(self.win)
            mage_button.draw(self.win)
            start_button.draw(self.win)
            self.win.blit(font.render(str(gold), True, (255, 255, 255)), (980-(len(str(gold))*20), 10))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game(1000, 800, "Tower Defence")
