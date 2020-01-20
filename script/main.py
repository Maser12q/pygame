import random

import pygame

# Game initialisation
pygame.init()

# Screen variables
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

# Global variables
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
BACK_END = 2


# main class with static variables
class Object:
    def __init__(self):
        self.fps = 100
        self.x_size = WIDTH
        self.y_size = HEIGHT
        self.vx = -100
        self.vy = -100
        self.color = (255, 255, 255)


# class for background
class Background:
    def __init__(self):
        self.background = pygame.transform.scale(
            pygame.image.load(f'../image/background_{random.randint(1, BACK_END)}.png'), (WIDTH, HEIGHT))
        # self.background = pygame.image.load(f'../image/background{random.randint(1, BACK_END)}.jpg')
        screen.blit(self.background, (0, 0))

    def everything(self):
        screen.blit(self.background, (0, 0))


# Class for bullet
class Bullet(Object):
    def __init__(self, pos):
        super().__init__()
        self.img = pygame.transform.scale(pygame.image.load('../image/плевок.png'), (50, 100))
        self.x, self.y, self.size_x = pos
        screen.blit(self.img, (self.x + self.size_x // 2.7, self.y))

    def move(self):
        if self.y > -100:
            self.y -= int(1000 / self.fps)

    def otrisovka(self):
        screen.blit(self.img, (self.x + self.size_x // 2.7, self.y))

    def return_y(self):
        return self.y


# player's class
class Player(Object):
    def __init__(self):
        super().__init__()
        self.size_x, self.size_y = (175, 175)
        self.img_player = pygame.transform.scale(pygame.image.load('../image/player_shield.png'),
                                                 (self.size_x, self.size_y))
        self.x = (WIDTH - self.size_x) // 2
        self.y = HEIGHT - self.size_y
        screen.blit(self.img_player, (self.x, self.y))

    def move_left(self):
        if (self.x - 5) > 0:
            self.x -= int(1000 / self.fps)

    def move_right(self):
        if (self.x + self.size_x) < WIDTH:
            self.x += int(1000 / self.fps)

    def for_bullet(self):
        return self.x, self.y, self.size_x

    def otrisovka(self):
        screen.blit(self.img_player, (self.x, self.y))


# Enemies class
class Enemy(Object):
    def __init__(self):
        super().__init__()
        self.size_x, self.size_y = (100, 100)
        self.img_enemy = pygame.transform.scale(pygame.image.load('../image/enemy_1.png'),
                                                 (self.size_x, self.size_y))
        self.img_enemy = pygame.transform.rotate(self.img_enemy, 180)

        self.x = 200
        self.y = 200
        screen.blit(self.img_enemy, (self.x, self.y))
        print(self.x, self.y)

    def move_left(self):
        if (self.x - 5) > 0:
            self.x -= int(1000 / self.fps)

    def move_right(self):
        if (self.x + self.size_x) < WIDTH:
            self.x += int(1000 / self.fps)

    def for_bullet(self):
        return self.x, self.y, self.size_x

    def otrisovka(self):
        screen.blit(self.img_enemy, (self.x, self.y))


# Variables for using in loop
n = list()
motion = 'STOP'

# classes for using  in loop
player = Player()
back = Background()
en = Enemy()
while True:
    back.everything()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                motion = 'LEFT'
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                motion = 'RIGHT'
            elif event.key == pygame.K_SPACE:
                n.append(Bullet(player.for_bullet()))

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                motion = 'STOP'

    for i in n:
        i.move()
        if i.return_y() < -100:
            del n[n.index(i)]
        i.otrisovka()

    if motion == 'LEFT':
        player.move_left()
    elif motion == 'RIGHT':
        player.move_right()

    print(n)
    player.otrisovka()
    en.otrisovka()
    pygame.display.flip()
