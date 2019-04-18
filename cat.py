import pygame
import os
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

    def move(self, player, platforms):
        self.lastY = self.y
        if player.x < self.x:
            self.x -= 5
            self.dir = 'left'
            self.still = False
        elif player.x > self.x:
            self.x += 5
            self.dir = 'right'
            self.still = False
        else:
            self.still = True
        if player.y < self.y:
            self.jump = True
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
        
