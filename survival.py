import pygame
import pygame_menu
pygame.init()
from random import randint
import numpy as np

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32
spawn_timer = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

imgPlayers = [
    pygame.image.load('person1.png'),
    pygame.image.load('person2.png')
    ]
zpic = pygame.image.load('zombie.png')
ground = pygame.image.load('ground.png')
forest = pygame.image.load('forest_5.png')
blood_image = pygame.image.load('blood.png')

menu_image = pygame_menu.BaseImage('menu_image.png')

gametheme = pygame_menu.Theme(background_color = menu_image, title_background_color = (0,0,0,18), title_font_shadow = True, title_font = pygame_menu.font.FONT_8BIT, title_font_size = (61), title_font_color = (232,252,194), widget_font = pygame_menu.font.FONT_8BIT)



DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

class Player:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'player'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.speed = 2
        self.hp = 50

        self.shotTimer = 0
        self.shotDelay = 10
        self.bulletSpeed = 10
        self.bulletDamage = 1

        self.px = 50
        self.py = 50


        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
    
    def update(self):
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.speed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.speed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.speed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.speed
            self.direct = 2
        elif keys[self.keyLEFT] and keys[self.keyUP]:
            self.rect.y -= self.speed
            self.rect.x -= self.speed
            self.direct = 7
        elif keys[self.keyLEFT] and keys[self.keyDOWN]:
            self.rect.y += self.speed
            self.rect.x -= self.speed
            self.direct = 8
        elif keys[self.keyRIGHT] and keys[self.keyUP]:
            self.rect.y -= self.speed
            self.rect.x += self.speed
            self.direct = 5
        elif keys[self.keyRIGHT] and keys[self.keyDOWN]:
            self.rect.y += self.speed
            self.rect.x += self.speed
            self.direct = 6

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
        
        if self.rect.x < 0:
            self.rect.topleft = oldX, oldY
        if self.rect.y < 0:
            self.rect.topleft = oldX, oldY
        if self.rect.x > WIDTH - TILE:
            self.rect.topleft = oldX, oldY
        if self.rect.y > HEIGHT - TILE:
            self.rect.topleft = oldX, oldY

        
        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
        plr = 0 
        for obj in objects:
            if obj.type == self.type:
                plr += 1
                if obj == self: break


        if self.shotTimer > 0: self.shotTimer -= 1
        self.image = pygame.transform.rotate(imgPlayers[plr-1], -self.direct * 90)


    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self,value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print('game over')


class Zombie:
    def __init__(self, color, px, py, direct):
        objects.append(self)
        self.type = 'zombie'
        

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.death_rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.speedx = 1
        self.speedy = 1
        self.hp = 3
        #self.px = 400
        #self.py = 200
        self.spawn_timer = 60
        self.zNumber = 0
        self.image = pygame.transform.rotate(zpic, self.direct * 90)

        self.biteDamage = 1
        
             

    def update(self):
        oldX, oldY = self.rect.topleft
        plx = 1000
        ply = 1000
        pls = 1000
        for obj in objects:
            if obj.type == 'player':
                if pls > np.sqrt((obj.rect.x - self.rect.x)**2 + (obj.rect.y - self.rect.y)):
                    pls = np.sqrt((obj.rect.x - self.rect.x)**2 + (obj.rect.y - self.rect.y))
                    plx = obj.rect.x
                    ply = obj.rect.y                    
        if self.rect.x > plx:
            self.speedx = -1
            self.direct = 3
        if self.rect.x < plx:
            self.speedx = 1
            self.direct = 1
        if self.rect.y > ply:
            self.speedy = -1
            self.direct = 0
        if self.rect.y < ply:
            self.speedy = 1
            self.direct = 2
        if (self.rect.x > plx) and (self.rect.y < ply):
            self.direct = 6
        if (self.rect.x > plx) and (self.rect.y > ply):
            self.direct = 7
        if (self.rect.x < plx) and (self.rect.y > ply):
            self.direct = 5
        if (self.rect.x < plx) and (self.rect.y < ply):
            self.direct = 4

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        for obj in objects:
                        if (self.rect.colliderect(obj.rect)) and  (obj.type != 'zombie'): 
                            obj.damage(self.biteDamage)

        for obj in objects:
            if (obj.type != self.type) and (self.rect.colliderect(obj.rect)):
                self.rect.topleft = oldX, oldY
                if obj.type != 'zombie':
                    if self.speedx == -1:
                        self.rect.x += 1*self.speedx
                    if self.speedx == 1:
                        self.rect.x += 1*self.speedx
                    if self.speedy == -1:
                        self.rect.y -= 1*self.speedy
                    if self.speedy == 1:
                        self.rect.y -= 1*self.speedy
        self.image = pygame.transform.rotate(zpic, -self.direct * 90) 
   

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self,value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self) 

            


            

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'black', (self.px, self.py), 2)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 600

    def update(self):
        pass

    def draw(self):
        window.blit(forest, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)



bullets = []
objects = []
Player('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Player('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_l))

Zombie('green', 500, 60, 0)
spawn_timer = 120




level = [
       "1111111111111111111111111",
       "1000000000000000000000001",
       "1000000000000000000000001",
       "1000011111100000010000001",
       "1000010000000000010000001",
       "1000010100000000010000001",
       "1000000100000000010000001",
       "1000000100000000000000001",
       "1000000100000000000000001",
       "1000000000000000000000001",
       "1000000111111111011100001",
       "1000000000000000001000001",
       "1000000000000000001000001",
       "1000000010000000001000001",
       "1000000010000000001000001",
       "1001111111100000000000001",
       "1000000000000000000000001",
       "1000000000000000011000001",
       "1111111111111111111111111"]

x=y=0 # координаты
for row in level: # вся строка
    for col in row: # каждый символ
        if col == "1":
            bl = Block(x, y, TILE)
            objects.append(bl)

        x += TILE 
    y += TILE    
    x = 0    
zNumber = 0



def menu_draw():
    menu = pygame_menu.Menu('Great Survival', 800, 600, theme=gametheme)

    menu.add.button('Survive')
    menu.add.selector

    menu.mainloop(window)

    pygame.display.update()
    clock.tick(FPS)

#menu_draw()     #вызовет меню, кнопка не работает, сделать функцию game

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    

    keys = pygame.key.get_pressed()
    N = 0
    zNumber = 0
    for obj in objects: 
        obj.update()
        if obj.type == 'zombie': N +=1
    zNumber = N
    
    for bul in bullets: bul.update()
    if spawn_timer > 0: spawn_timer -= 1
    if (spawn_timer <= 0) and (zNumber <10):
        x = randint(40, 600)
        y = randint(60, 400)
        zrect = pygame.Rect(x, y, TILE, TILE)
        check = True
        for obj in objects:
            if zrect.colliderect(obj.rect): 
                check = False
                break
        if check == True:   
            Zombie('green', x, y, 0)
            spawn_timer = 120 
            zNumber += 1
    
    
    
    
    

    window.blit(ground, (0,0))
    
    for obj in objects: obj.draw()
    for bul in bullets: bul.draw()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



