import pygame
from random import randrange
from math import gcd
pygame.init()

width, height = 420, 420
window = pygame.display.set_mode((width, height))
gridSize = 20

def drawGrid(gridSize):
    for c in range(int(width/gridSize)):
        for r in range(int(height/gridSize)):
            pygame.draw.rect(window, (200, 200, 200), ((c * gridSize + 1, r * gridSize + 1), (gridSize - 2, gridSize - 2)))

class Player():
    def __init__(self):
        self.sx, self.sy = 2, 2
        self.rect = pygame.Rect(self.sx * gridSize, self.sy * gridSize, gridSize, gridSize)

        self.colour = (0, 0, 0)

        self.dir = (0, 0)
        self.dirL = []

        self.tails = []

        self.movable = True
    
    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)

    def move(self):
        self.dirL.insert(0, self.dir)
        if len(self.dirL) > len(self.tails) + 1:
            self.dirL.pop()

        self.rect.centerx += gridSize * self.dir[0]
        self.rect.centery += gridSize * self.dir[1]

        self.movable = True
  
        prev_pos = (self.rect.x, self.rect.y)
        for i, tail in enumerate(self.tails):
            tail_pos = (tail.rect.x, tail.rect.y)
            tail.rect.x, tail.rect.y = prev_pos
            prev_pos = tail_pos
            tail.draw()

    def eat(self):
        if len(self.tails) < 1:
            self.tails.append(Tail(self.rect.x - gridSize * self.dir[0] * 1, self.rect.y  - gridSize * self.dir[1] * 1))
        else:
            self.tails.append(Tail(self.tails[-1].rect.x - gridSize * self.dir[0] * 1, self.tails[-1].rect.y  - gridSize * self.dir[1] * 1))
        print(len(self.tails))
    
    def checkCollison(self):
        for i in self.tails:
            if self.tails.index(i) == 0:
                continue
            if i.rect.x == self.rect.x and i.rect.y == self.rect.y:
                return False
        if self.rect.x >= width or self.rect.x < 0 or self.rect.y >= height or self.rect.y < 0:
            return False
        return True

class Tail(Player):
    def __init__(self, x, y):
        self.colour = (100, 100, 100)
        self.rect = pygame.Rect(x, y, 20, 20)
    
    def follow(self, dir):
        self.rect.centerx += gridSize * dir[0]
        self.rect.centery += gridSize * dir[1]
        # print(dir)

class Apple():
    def __init__(self):
        self.x, self.y = randrange(1,round(width/gridSize)), randrange(1,round(height/gridSize))
        self.rect = pygame.Rect(self.x * gridSize, self.y * gridSize, gridSize, gridSize)

        self.colour = (255, 0, 50)
    
    def draw(self):
        pygame.draw.rect(window, self.colour, self.rect)

    def eaten(self, player):
        while True:
            collides = False
            self.rect.x, self.rect.y = randrange(1, round(width/gridSize)) * gridSize, randrange(1, round(height/gridSize)) * gridSize
            for i in player.tails:
                if self.rect.x == i.rect.x and self.rect.y == i.rect.y:
                    collides = True
            if not collides:
                return


player = Player()
apple = Apple()

running = True
clock = pygame.time.Clock()
while running:
    clock.tick(10)
    window.fill((255,255,255))
    drawGrid(gridSize)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player.movable:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT] and player.dir != (-1, 0) or keys[pygame.K_d] and player.dir != (-1, 0):
                    player.dir = (1, 0)
                elif keys[pygame.K_LEFT] and player.dir != (1, 0) or keys[pygame.K_a] and player.dir != (1, 0):
                    player.dir = (-1, 0)
                elif keys[pygame.K_DOWN] and player.dir != (0, -1) or keys[pygame.K_s] and player.dir != (0, -1):
                    player.dir = (0, 1)
                elif keys[pygame.K_UP] and player.dir != (0, 1) or keys[pygame.K_w] and player.dir != (0, 1):
                    player.dir = (0, -1)
                player.movable = False
    
    player.move()
    if player.rect.x == apple.rect.x and player.rect.y == apple.rect.y:
        apple.eaten(player)
        player.eat()
    
    # if running:
    #     running = player.checkCollison()
    if not player.checkCollison():
        player.movable = False
        for i in player.tails:      
            player.tails.remove(i)
        player.tails = []
        player.rect.x, player.rect.y = 2 * gridSize, 2 * gridSize
        player.dir = (0,0)
        player.movable = True

    apple.draw()
    player.draw()
   
    pygame.display.update()

pygame.quit()