import pygame
from config import PATH, width, height, size
import os
from pygame.locals import *

char = {
    'right': [],
    'left': []
}

for i in range(0,106):
    img = pygame.image.load(PATH+os.path.join('data', 'player', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size), int(h*size)))
    char['right'].append(img)

for i in range(0,106):
    img = char['right'][i]
    img = pygame.transform.flip(img, True, False)
    char['left'].append(img)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastY = y
        self.speed = 10
        self.frameCounter = 0
        self.frameDelay = 0
        self.frameDelayMax = 3
        self.dir = 'right'
        self.jump = True
        self.jumpVelStart = 24
        self.jumpVel = 0

        self.shots = []
    
    def move(self, keys, platforms):
        self.lastY = self.y
        if keys[K_RIGHT]:
            self.dir = 'right'
            self.x += self.speed
        if keys[K_LEFT]:
            self.dir = 'left'
            self.x -= self.speed
        if keys[K_UP]:
            self.jump = True
        if keys[K_SPACE]:
            if self.dir == 'right':
                self.shots.append(Shot(self.x+60, self.y-46, self.dir))
            else:
                self.shots.append(Shot(self.x-60, self.y-46, self.dir))
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
    def draw(self, win):
        self.frameDelay += 1
        if self.frameDelay >= self.frameDelayMax:
            self.frameDelay = 0
            self.frameCounter += 1
            if self.frameCounter > 105:
                self.frameCounter = 0
        img = char[self.dir][self.frameCounter]
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y+30)
        win.blit(img, loc)
        for i in self.shots:
            i.draw(win)

class Shot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.vel = 15

    def draw(self, win):
        pygame.draw.rect(win, (255,0,0), pygame.Rect(self.x, self.y, 10,5))
        if self.dir == 'right':
            self.x += self.vel
        else:
            self.x -= self.vel