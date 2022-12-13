import pygame
import pygame_menu

imgPlayers = [
    pygame.image.load('person1.png'),
    pygame.image.load('person2.png')
    ]
zpic = pygame.image.load('zombie.png')
zpic_right = pygame.image.load('zombie_right.png')
zpic_down = pygame.image.load('zombie_down.png')
zpic_left = pygame.image.load('zombie_left.png')
zBossPic = pygame.image.load('zombie_boss.png')
zBossPic_right = pygame.image.load('zombie_boss_right.png')
zBossPic_down = pygame.image.load('zombie_boss_down.png')
zBossPic_left = pygame.image.load('zombie_boss_left.png')
ground = pygame.image.load('ground.png')
brick = pygame.image.load('brick.png')
brick_damaged = pygame.image.load('brick_damaged.png')
blood_image = pygame.image.load('blood.png')
gameover_image = pygame.image.load('gameover.png')

menu_image = pygame_menu.BaseImage('menu_image.png')

gametheme = pygame_menu.Theme(background_color = menu_image, title_background_color = (0,0,0,18), title_font_shadow = True, title_font = pygame_menu.font.FONT_8BIT, title_font_size = (61), title_font_color = (232,252,194), widget_font = pygame_menu.font.FONT_8BIT)

