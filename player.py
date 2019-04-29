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

explosion = []
for i in range(12):
    img = pygame.image.load(PATH+os.path.join('data', 'explosion', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(1.8*w*size), int(1.8*h*size)))
    explosion.append(img)

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
        self.health = 100
        self.explode = False
        self.explodeCounter = 0

        self.shots = []

        self.movement = []
        self.relativeX = x
    
    def move(self, keys, platforms):
        self.lastY = self.y
        self.movement = []
        if keys[K_RIGHT] or keys[K_d]:
            self.dir = 'right'
            self.relativeX += self.speed
            self.movement.append(-self.speed)
        if keys[K_LEFT] or keys[K_a]:
            self.dir = 'left'
            self.relativeX -= self.speed
            self.movement.append(self.speed)
        if keys[K_UP] or keys[K_w]:
            self.jump = True
        if (keys[K_DOWN] or keys[K_s]) and not self.jump:
            self.jump = True
            self.jumpVel = 0
            self.y += 5
            self.lastY = self.y
        if keys[K_SPACE]:
            if self.dir == 'right':
                self.shots.append(Shot(self.x+70, self.y-49, self.dir))
            else:
                self.shots.append(Shot(self.x-70, self.y-49, self.dir))
        if keys[K_RSHIFT] and not self.explode: #right shift
            self.explode = True
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
        return self.movement
    def draw(self, win, movement):
        for i in self.shots:
            i.draw(win, movement)
        self.frameDelay += 1
        if self.frameDelay >= self.frameDelayMax:
            if self.explode:
                self.explodeCounter += 1
                if self.explodeCounter >= 12:
                    self.explode = False
                    self.explodeCounter = 0
            self.frameDelay = 0
            self.frameCounter += 1
            if self.frameCounter > 105:
                self.frameCounter = 0
        if self.explode:
            img = explosion[self.explodeCounter]
            loc = img.get_rect()
            loc.center = (self.x, self.y-50)
            win.blit(img, loc)
        img = char[self.dir][self.frameCounter]
        loc = img.get_rect()
        loc.midbottom = (self.x, self.y+30)
        win.blit(img, loc)
        if self.health < 100:
            pygame.draw.rect(win, (100,255,100), pygame.Rect(self.x-50,self.y-120,self.health,20))
            pygame.draw.rect(win, (255,100,100), pygame.Rect(self.x-50+self.health,self.y-120,100-self.health,20))

class Shot:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.vel = 15

    def draw(self, win, movement):
        for i in movement:
            self.x += i
        pygame.draw.rect(win, (255,0,0), pygame.Rect(self.x, self.y, 10,5))
        if self.dir == 'right':
            self.x += self.vel
        else:
            self.x -= self.vel