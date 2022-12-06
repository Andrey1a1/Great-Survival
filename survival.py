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
gameover_value = 0
font = pygame.font.SysFont("ariel", 40)

imgPlayers = [
    pygame.image.load('person1.png'),
    pygame.image.load('person2.png')
    ]
zpic = pygame.image.load('zombie.png')
zBossPic = pygame.image.load('zombie_boss.png')
ground = pygame.image.load('ground.png')
forest = pygame.image.load('forest_5.png')
blood_image = pygame.image.load('blood.png')
gameover_image = pygame.image.load('gameover.png')

menu_image = pygame_menu.BaseImage('menu_image.png')

gametheme = pygame_menu.Theme(background_color = menu_image, title_background_color = (0,0,0,18), title_font_shadow = True, title_font = pygame_menu.font.FONT_8BIT, title_font_size = (61), title_font_color = (232,252,194), widget_font = pygame_menu.font.FONT_8BIT)



DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

class Player:
    def __init__(self, color, px, py, direct, keyList, hp):
        objects.append(self)
        self.type = 'player'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.speed = 2
        self.hp = hp
        self.hpmax = hp
        self.kills = 0
        self.shotTimer = 0
        self.shotDelay = 15
        self.death = 0
        self.bulletSpeed = 12
        self.bulletDamage = 1
        self.killsForShotgun  = 10
        self.shotgunBullets = 5
        self.killsForBoss = 13
        self.bossDelay = 10
        self.killsAd = 5
        self.bossWarningDelay = 300

        self.px = 50
        self.py = 50
        self.isBoss = False



        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        self.congratulatedelay = 400
        self.congratulatedelay2 = 400
        self.congratulatedelay3 = 400
    
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
            if (obj != self) and (obj.type != 'zombie') and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
        
        if self.rect.x < 0:
            self.rect.topleft = oldX, oldY
        if self.rect.y < 0:
            self.rect.topleft = oldX, oldY
        if self.rect.x > WIDTH - TILE:
            self.rect.topleft = oldX, oldY
        if self.rect.y > HEIGHT - TILE:
            self.rect.topleft = oldX, oldY
            #+ DIRECTS[self.direct][1]+16
        
        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            
            if self.kills >= self.killsForShotgun:
                
                for i in range(self.shotgunBullets):
                    Bullet(self, self.rect.centerx+ DIRECTS[self.direct][1]+10, self.rect.centery+ DIRECTS[self.direct][0]+10, dx+ randint(-10,10)/5, dy+ randint(-10,10)/5, self.bulletDamage)
                self.shotTimer = self.shotDelay*3
            elif self.kills >= self.killsForShotgun*2:
                for i in range(self.shotgunBullets*2):
                    Bullet(self, self.rect.centerx+ DIRECTS[self.direct][1]+10, self.rect.centery+ DIRECTS[self.direct][0]+10, dx+ randint(-10,10)/5, dy+ randint(-10,10)/5, self.bulletDamage)
                self.shotTimer = self.shotDelay*2
            elif self.kills >= self.killsForShotgun*3:
                for i in range(self.shotgunBullets*3):
                    Bullet(self, self.rect.centerx+ DIRECTS[self.direct][1]+10, self.rect.centery+ DIRECTS[self.direct][0]+10, dx+ randint(-10,10)/5, dy+ randint(-10,10)/5, self.bulletDamage)
                self.shotTimer = self.shotDelay*1.5
             
            else:

                Bullet(self, self.rect.centerx+DIRECTS[self.direct][1]+10, self.rect.centery + DIRECTS[self.direct][0]+10, dx + randint(-10,10)/10, dy + randint(-10,10)/10, self.bulletDamage)
                self.shotTimer = self.shotDelay

            if self.kills >= self.killsForBoss:
                x = randint(40, 600)
                y = randint(60, 400)
                zrect = pygame.Rect(x, y, TILE, TILE)
                check = True
                for obj in objects:
                    if zrect.colliderect(obj.rect): 
                        check = False
                        break
                if check == True:   
                    Zombie(pygame.transform.rotate(zBossPic, self.direct * 90), x, y, 0, 10)
                    self.killsForBoss += self.killsAd
                    if self.killsAd > 3 : self.killsAd -= 1
                    self.isBoss = True
                    self.bossWarningDelay = 300
                    
                    

        plr = 0 
        for obj in objects:
            if obj.type == self.type:
                plr += 1
                if obj == self: break


        if self.shotTimer > 0: self.shotTimer -= 1
        self.image = pygame.transform.rotate(imgPlayers[plr-1], -self.direct * 90)

        if self.hp < self.hpmax:
            self.hp += 6 / FPS
        


    def draw(self):
        window.blit(self.image, self.rect)
        pygame.draw.line(window, 'green', (self.rect.x, self.rect.y), (self.rect.x+32*self.hp/self.hpmax,self.rect.y), 5)
        label = font.render(f"Kills: {self.kills}", True, "white")
        window.blit(label, [50, 10])

        if self.congratulatedelay >= 0 and self.kills >= self.killsForShotgun:
            label = font.render(f"Now you have standart shotgun! Kill {self.killsForShotgun*2} for new super shotgun!", True, "white")
            window.blit(label, [10, 40])
            self.congratulatedelay -=1
        if self.congratulatedelay2 >= 0 and self.kills >= self.killsForShotgun*2:
            label = font.render(f"Now you have super shotgun! Kill {self.killsForShotgun*3} for great shotgun!", True, "white")
            window.blit(label, [10, 40])
            self.congratulatedelay2 -=1
        if self.congratulatedelay3 >= 0 and self.kills >= self.killsForShotgun*3:
            label = font.render(f"Now you have great shotgun! Good luck!", True, "white")
            window.blit(label, [10, 40])
            self.congratulatedelay3 -=1 
        if self.isBoss and (self.bossWarningDelay > 0):
            label = font.render(f"BOSS!", True, "red")
            window.blit(label, [300, 100])
            self.bossWarningDelay -=1 
    def damage(self,value):
        self.hp -= value
        if self.hp <= 0:
            global gameover_value
            gameover_value += 1
            objects.remove(self)


class Zombie:
    def __init__(self, image, px, py, direct, hp):
        objects.append(self)
        self.type = 'zombie'
        

        
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.death_rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.speedx = 1
        self.speedy = 1
        self.hp = hp
        self.hpmax = hp
        #self.px = 400
        #self.py = 200
        self.spawn_timer = 60
        self.zNumber = 0
        self.death = 0
        self.image = image 
        
        self.biteDamage = 1
        
             

    def update(self):
        if self.death == 0:
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
                if (obj.type == 'block' ) and (self.rect.colliderect(obj.rect)):
                    self.rect.topleft = oldX, oldY
                    if self.speedx == -1:
                        self.rect.x += 1*self.speedx
                    if self.speedx == 1:
                        self.rect.x += 1*self.speedx
                    if self.speedy == -1:
                        self.rect.y -= 1*self.speedy
                    if self.speedy == 1:
                        self.rect.y -= 1*self.speedy
            self.image = pygame.transform.rotate(self.image, -self.direct * 90) 
        elif self.death == 1:
            pass
    

    def draw(self):
        if self.death == 0:
            window.blit(self.image, self.rect)
            pygame.draw.line(window, 'red', (self.rect.x, self.rect.y), (self.rect.x+32*self.hp/self.hpmax,self.rect.y), 5)
        elif self.death == 1:
            window.blit(blood_image, self.rect)



    def damage(self,value):
        if self.death == 0:
            self.hp -= value
            if self.hp <= 0:
                self.death = 1
                for obj in objects:
                    if obj.type == 'player':
                        obj.kills += 1
                

            


            

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
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py) and (obj.death == 0):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'black', (self.px, self.py), 2)

class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.death = 0

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


Zombie(zpic, 500, 60, 0, 3)
spawn_timer = 120


level = [
       "1111111111111111111111111",
       "1000000000000000000000001",
       "1000000000000000000000001",
       "1000111111100000010000001",
       "1000100000000000010000001",
       "1000100000000000010000001",
       "1000000100000000010000001",
       "1000000111000000000000001",
       "1000000000000000000000001",
       "1000000000000000000000001",
       "1000000111111110011100001",
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

    menu.add.button('Play Single', game_play_single)
    menu.add.button('Play Coop', game_play_coop)
    menu.add.button('Quit', game_quit)

    menu.mainloop(window)

    pygame.display.update()
    clock.tick(FPS)



def game_play_single():

    Player('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), 100)

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        
        global keys
        keys = pygame.key.get_pressed()
        N = 0
        zNumber = 0
        for obj in objects: 
            obj.update()
            if obj.type == 'zombie': N +=1
        zNumber = N
        
        for bul in bullets: bul.update()
        global spawn_timer
        if spawn_timer > 0: spawn_timer -= 1
        if (spawn_timer <= 0):
            x = randint(40, 600)
            y = randint(60, 400)
            zrect = pygame.Rect(x, y, TILE, TILE)
            check = True
            for obj in objects:
                if zrect.colliderect(obj.rect): 
                    check = False
                    break
            if check == True:   
                Zombie(pygame.transform.rotate(zpic, 0 * 90), x, y, 0, 3)
                spawn_timer = 120 
                
        
        

        press = pygame.key.get_pressed()
        if press[pygame.K_ESCAPE]:
            pygame.quit()

        window.blit(ground, (0,0))
        global gameover_value
        
        
        
        for obj in objects:
            if obj.type != 'player': obj.draw()
        for obj in objects:
            if obj.type == 'player': obj.draw()
        for bul in bullets: bul.draw()
        if gameover_value == 1:
            window.fill('black')
            window.blit(gameover_image, (0,0))
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()



def game_play_coop():
    Player('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), 50)
    Player('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_l), 50)


    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        
        global keys
        keys = pygame.key.get_pressed()
        N = 0
        zNumber = 0
        for obj in objects: 
            obj.update()
            if obj.type == 'zombie': N +=1
        zNumber = N
        
        for bul in bullets: bul.update()
        global spawn_timer
        if spawn_timer > 0: spawn_timer -= 1
        if (spawn_timer <= 0):
            x = randint(40, 600)
            y = randint(60, 400)
            zrect = pygame.Rect(x, y, TILE, TILE)
            check = True
            for obj in objects:
                if zrect.colliderect(obj.rect): 
                    check = False
                    break
            if check == True:   
                Zombie(pygame.transform.rotate(zpic, 0 * 90), x, y, 0, 3)
                spawn_timer = 120 
                
        
        press = pygame.key.get_pressed()
        if press[pygame.K_ESCAPE]:
            pygame.quit()

        window.blit(ground, (0,0))
        global gameover_value
        for obj in objects:
            if obj.type != 'player': obj.draw()
        for obj in objects:
            if obj.type == 'player': obj.draw()
        for bul in bullets: bul.draw()
        
        if gameover_value == 2:
            window.fill('black')
            window.blit(gameover_image, (0,0))
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

def game_quit():
    pygame.quit()




menu_draw()    
