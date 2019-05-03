import pygame
import os
from config import PATH, size

lobsterR = []
lobsterL = []
for i in range(5):
    img = pygame.image.load(PATH+os.path.join('data', 'enemies', 'lobster', str(i)+'.gif'))
    w, h = img.get_rect().size
    img = pygame.transform.scale(img, (int(w*size*1.5), int(h*size*1.5)))
    lobsterR.append(img)
    lobsterL.append(pygame.transform.flip(img, True, False))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100

class Lobster(Enemy):
    def __init__(self, x, y):
        Enemy.__init__(self, x, y)
        self.health = 200
        self.frameCounter = 0
        self.frameCounterMax = 5
        self.frameDelay = 0

    def draw(self, win, player):
        self.frameDelay += 1
        if self.frameDelay > 3:
            self.frameDelay = 0
            self.frameCounter += 1
            if self.frameCounter >= self.frameCounterMax:
                self.frameCounter = 0
        if player.x < self.x:
            win.blit(lobsterL[self.frameCounter], (self.x, self.y))
        else:
            win.blit(lobsterL[self.frameCounter], (self.x, self.y))