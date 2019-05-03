import pygame
import os
from config import PATH, size, width

lobsterR = []
lobsterL = []
for i in range(5):
    img = pygame.image.load(PATH+os.path.join('data', 'enemies', 'lobster', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size*1.5), int(h*size*1.5)))
    lobsterR.append(img)
    lobsterL.append(pygame.transform.flip(img, True, False))

spiderR = []
spiderL = []
for i in range(72):
    img = pygame.image.load(PATH+os.path.join('data', 'enemies', 'spider', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size*.5), int(h*size*.5)))
    spiderR.append(img)
    spiderL.append(pygame.transform.flip(img, True, False))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.shots = []

class Lobster(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.health = 200
        self.frameCounter = 0
        self.frameCounterMax = 5
        self.frameDelay = 0
        self.w, self.h = lobsterL[0].get_rect().size

    def info(self):
        return 'Lobster('+str(self.x)+'+x, '+str(self.y)+')'

    def draw(self, win, player, movement):
        self.frameDelay += 1
        if self.frameDelay > 3:
            self.frameDelay = 0
            self.frameCounter += 1
            if self.frameCounter >= self.frameCounterMax:
                self.frameCounter = 0
        if player.x < self.x:
            img = lobsterR[self.frameCounter]
        else:
            img = lobsterL[self.frameCounter]
        loc = img.get_rect()
        loc.center = (self.x, self.y)
        win.blit(img, loc)
        if self.health < 200:
            pygame.draw.rect(win, (0,200,0), pygame.Rect(self.x-100, self.y-self.h-15, self.health, 10))
            pygame.draw.rect(win, (200,0,0), pygame.Rect(self.x-100+self.health,self.y-self.h-15,200-self.health, 10))

class Spider(Lobster):
    def __init__(self, x, y):
        Lobster.__init__(self, x, y)
        self.health = 100
        self.frameCounterMax = 72
        self.shots = []
        self.w, self.h = spiderR[0].get_rect().size

    def info(self):
        return 'Spider('+str(self.x)+'+x, '+str(self.y)+')'
    
    def draw(self, win, player, movement):
        self.frameCounter += 1
        if self.frameCounter >= self.frameCounterMax:
            self.frameCounter = 0
        if self.frameCounter == 42:
            if player.x < self.x:
                vel = -12
            else:
                vel = 12
            if -200 < self.x < width+200:
                self.shots.append(Shot(self.x, self.y, vel))
        for i in self.shots:
            for x in movement:
                i.x += x
            i.draw(win)
        if player.x < self.x:
            img = spiderL[self.frameCounter]
        else:
            img = spiderR[self.frameCounter]
        loc = img.get_rect()
        loc.center = (self.x, self.y)
        win.blit(img, loc)
        if self.health < 100:
            pygame.draw.rect(win, (0,200,0), pygame.Rect(self.x-50, self.y-self.h-15, self.health, 10))
            pygame.draw.rect(win, (200,0,0), pygame.Rect(self.x-50+self.health,self.y-self.h-15,100-self.health, 10))

class Shot:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
    def draw(self, win):
        pygame.draw.circle(win, (0,255,0), (int(self.x), int(self.y)), 10)
        self.x += self.vel