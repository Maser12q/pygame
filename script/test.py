import random

import pygame

# Game initialisation
pygame.init()

# Screen variables
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

# Global variables
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

width, height = 200, 200


# class Bomb(pygame.sprite.Sprite):
#     image = pygame.image.load("../image/снаряд.png")
#     image_boom = pygame.image.load("../image/ракета.png")
#
#     def __init__(self, group):
#         # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
#         super().__init__(group)
#         self.image = Bomb.image
#         self.rect = self.image.get_rect()
#         self.rect.x = random.randrange(width)
#         self.rect.y = random.randrange(height)
#
#     def update(self, *args):
#         self.rect = self.rect.move(random.randrange(3) - 1, random.randrange(3) - 1)
#         if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
#             self.image = self.image_boom


for i in range(50):
    # можно сразу создавать спрайты с указанием группы
    bomb = pygame.sprite.Sprite(all_sprites)
    bomb.image = bomb_image
    bomb.rect = bomb.image.get_rect()

    # задаём случайное местоположение бомбочке
    bomb.rect.x = random.randrange(width)
    bomb.rect.y = random.randrange(height)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.get_event(event)

        all_sprites.draw(screen)
    all_sprites.update()
