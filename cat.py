import pygame
import os
from random import randint
from config import PATH, size, width, height

char = {
    'right': [],
    'left': []
}

for i in range(0, 21):
    img = pygame.image.load(PATH+os.path.join('data', 'cat', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size*.45), int(h*size*.45)))
    char['right'].append(img)

for i in range(0,21):
    img = pygame.transform.flip(char['right'][i], True, False)
    char['left'].append(img)

class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastY = y
        self.jump = True
        self.jumpVelStart = 24
        self.jumpVel = 0
        self.dir = 'right'
        self.frameCounter = 0
        self.still = False
        self.health = 100
        self.behavior = 0
        self.gotospot = 0
        self.w, self.h = char['right'][0].get_rect().size

    def draw(self, win):
        self.frameCounter += 1
        if self.frameCounter > 20:
            self.frameCounter = 0
        if self.still:
            self.frameCounter -= 1
            img = char[self.dir][self.frameCounter]
        else:
            img = char[self.dir][self.frameCounter]
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y+20)
        win.blit(img, loc)
        if self.health < 100:
            pygame.draw.rect(win, (100,255,100), pygame.Rect(self.x-50,self.y-100,self.health,20))
            pygame.draw.rect(win, (255,100,100), pygame.Rect(self.x-50+self.health, self.y-100,100-self.health,20))

    def move(self, player, platforms):
        if randint(0,200) == 1:
            self.behavior = randint(0,1)
            if self.behavior == 1:
                plat = platforms[randint(0,len(platforms)-1)]
                x = randint(plat.x, plat.x+plat.w)
                y = plat.y
                self.gotospot = (x, y)
        self.lastY = self.y
        if self.behavior == 0:
            if abs(player.x - self.x) < 50:
                self.still = True
            elif player.x < self.x:
                self.x -= 5
                self.dir = 'left'
                self.still = False
            elif player.x > self.x:
                self.x += 5
                self.dir = 'right'
                self.still = False
            if player.y < self.y and abs(self.x-player.x) < 100:
                self.jump = True
            elif player.y > self.y and abs(self.x-player.x) < 100 and not self.jump:
                self.jump = True
                self.jumpVel = 0
                self.y += 5
                self.lastY = self.y
        elif self.behavior == 1:
            if abs(self.gotospot[0]-self.x) < 10:
                plat = platforms[randint(0,len(platforms)-1)]
                x = randint(plat.x, plat.x+plat.w)
                y = plat.y
                self.gotospot = (x, y)
            if self.gotospot[0] < self.x:
                self.x -= 5
                self.dir = 'left'
                self.still = False
            elif self.gotospot[0] > self.x:
                self.x += 5
                self.dir = 'right'
                self.still = False
            else:
                self.still = True
            if self.gotospot[1] < self.y and abs(self.x-self.gotospot[0]) < 100:
                self.jump = True
            elif self.gotospot[1] > self.y and abs(self.x-self.gotospot[0]) < 100 and not self.jump:
                self.jump = True
                self.jumpVel = 0
                self.y += 5
                self.lastY = self.y
        if self.jump:
            self.y -= self.jumpVel
            self.jumpVel -= 2
            for i in platforms:
                hit, val = i.hit(self.x, self.y, self.lastY)
                if hit:
                    self.jump = False
                    self.y = val
                    self.jumpVel = self.jumpVelStart
        else:
            hovering = True
            for i in platforms:
                if i.xhit(self.x,self.y):
                    hovering = False
                    break
            if hovering:
                self.jump = True
                self.jumpVel = 0
        
