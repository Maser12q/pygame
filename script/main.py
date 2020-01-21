import random
import time

import pygame


def start():
    back = pygame.transform.scale(pygame.image.load('../image/background_for_menu.png'), (WIDTH, HEIGHT))
    button_easy = pygame.transform.scale(pygame.image.load('../image/button_easy.png'), (250, 60))
    button_exit = pygame.transform.scale(pygame.image.load('../image/button_exit.png'), (250, 60))
    button_hard = pygame.transform.scale(pygame.image.load('../image/button_hard.png'), (250, 60))
    running = True

    while running:
        screen.blit(back, (0, 0))
        screen.blit(button_easy, (50, 560))
        screen.blit(button_hard, (50, 650))
        screen.blit(button_exit, (50, 740))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()

        if mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(range(560, 621)):
            easy_level()
            pygame.quit()
        elif mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(
                range(650, 711)):
            hard_level()
            pygame.quit()
        elif mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(
                range(740, 801)):
            pygame.quit()
        # print(mouse_pos)
        pygame.display.update()


def easy_level():
    score = 0

    # Создаем игру и окно
    class Background(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(
                pygame.image.load(f'../image/background_{random.randint(1, BACK_END)}.png'), (WIDTH, HEIGHT))
            # self.background = pygame.image.load(f'../image/background{random.randint(1, BACK_END)}.jpg')
            self.rect = self.image.get_rect()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, naprav):
            pygame.sprite.Sprite.__init__(self)
            if naprav == '+':
                self.image = pygame.transform.scale(pygame.image.load('../image/снаряд.png'), (25, 50))
            else:
                self.image = pygame.transform.rotate(
                    pygame.transform.scale(pygame.image.load('../image/ракета.png'), (25, 50)), 180)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10
            self.nap = naprav

        def update(self):
            if self.nap == '+':
                self.speedy = -18
                self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()
            else:
                self.rect.y -= self.speedy
                if self.rect.bottom > HEIGHT:
                    self.kill()

    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('../image/enemy_1.png'), (75, 75))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.times = time.time()

        def update(self):
            if time.time() - self.times >= random.randint(2, 10):
                self.times = time.time()
                self.shoot()

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top, '-')
            all_sprites.add(bullet)
            bullets_their.add(bullet)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('../image/player_shield.png'), (125, 125))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speed_x = 0

        def update(self):
            self.speed_x = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                self.speed_x = -8
            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                self.speed_x = 8

            self.rect.x += self.speed_x

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top, '+')
            all_sprites.add(bullet)
            bullets_my.add(bullet)

    # def is_possible():
    #     global POS
    #     if (x not in POS or x + 75 not in POS) and (y not in POS or y + 75 not in POS):
    #         return x, y
    #     return is_possible()

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets_my = pygame.sprite.Group()
    bullets_their = pygame.sprite.Group()

    player = Player()
    back = Background()

    all_sprites.add(back, player)

    for i in range(random.randint(25, 150)):
        x, y = random.randint(0, WIDTH - 100), random.randint(0, HEIGHT // 2)
        m = Mob(x, y)
        all_sprites.add(m)
        mobs.add(m)

    # Цикл игры
    running = True
    while running:
        m = len(mobs)
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                after(score, 'e')
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    after(score, 'e')
                    pygame.quit()

        # Обновление
        all_sprites.update()
        pygame.sprite.groupcollide(mobs, bullets_my, True, True)
        pygame.sprite.groupcollide(bullets_their, bullets_my, True, True)

        score += m - len(mobs)

        if pygame.sprite.spritecollide(player, bullets_their, False):
            after(score, 'e')
            pygame.quit()

        if not mobs:
            after(score, 'e')
            pygame.quit()

        all_sprites.draw(screen)
        pygame.display.flip()


def hard_level():
    score = 0

    # Создаем игру и окно
    class Background(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(
                pygame.image.load(f'../image/background_{random.randint(1, BACK_END)}.png'), (WIDTH, HEIGHT))
            # self.background = pygame.image.load(f'../image/background{random.randint(1, BACK_END)}.jpg')
            self.rect = self.image.get_rect()

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, naprav):
            pygame.sprite.Sprite.__init__(self)
            if naprav == '+':
                self.image = pygame.transform.scale(pygame.image.load('../image/снаряд.png'), (25, 50))
            else:
                self.image = pygame.transform.rotate(
                    pygame.transform.scale(pygame.image.load('../image/ракета.png'), (25, 50)), 180)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10
            self.nap = naprav

        def update(self):
            if self.nap == '+':
                self.speedy = -36
                self.rect.y += self.speedy
                if self.rect.bottom < 0:
                    self.kill()
            else:
                self.rect.y -= self.speedy
                if self.rect.bottom > HEIGHT:
                    self.kill()

    class Mob(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('../image/enemy_1.png'), (75, 75))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.times = time.time()

        def update(self):
            if time.time() - self.times >= random.randint(2, 10):
                self.times = time.time()
                self.shoot()

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top, '-')
            all_sprites.add(bullet)
            bullets_their.add(bullet)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load('../image/player_shield.png'), (125, 125))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speed_x = 0

        def update(self):
            self.speed_x = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                self.speed_x = -27
            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                self.speed_x = 27

            self.rect.x += self.speed_x

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            bullet = Bullet(self.rect.centerx, self.rect.top, '+')
            all_sprites.add(bullet)
            bullets_my.add(bullet)

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets_my = pygame.sprite.Group()
    bullets_their = pygame.sprite.Group()

    player = Player()
    back = Background()

    all_sprites.add(back, player)

    for i in range(random.randint(50, 100)):
        x, y = random.randint(0, WIDTH - 100), random.randint(0, HEIGHT // 2)
        m = Mob(x, y)
        all_sprites.add(m)
        mobs.add(m)

    # Цикл игры
    running = True
    while running:
        m = len(mobs)
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                after(score, 'h')
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    after(score, 'h')
                    pygame.quit()

        # Обновление
        all_sprites.update()
        pygame.sprite.groupcollide(mobs, bullets_my, True, True)

        score += m - len(mobs)
        if pygame.sprite.spritecollide(player, bullets_their, False):
            after(score, 'h')
            pygame.quit()

        if not mobs:
            after(score, 'h')
            pygame.quit()

        all_sprites.draw(screen)
        pygame.display.flip()


def after(score, d):
    if d == 'h':
        s = score * 10
    else:
        s = score * 3
    print(1)
    back = pygame.transform.scale(pygame.image.load('../image/background_for_menu.png'), (WIDTH, HEIGHT))
    button_easy = pygame.transform.scale(pygame.image.load('../image/button_easy.png'), (250, 60))
    button_exit = pygame.transform.scale(pygame.image.load('../image/button_exit.png'), (250, 60))
    button_hard = pygame.transform.scale(pygame.image.load('../image/button_hard.png'), (250, 60))
    text2 = pygame.font.SysFont(None, 72).render(f'Ваш счет: {s}', 0, (255, 0, 0))
    running = True
    while running:
        screen.blit(back, (0, 0))
        screen.blit(button_easy, (50, 560))
        screen.blit(button_hard, (50, 650))
        screen.blit(button_exit, (50, 740))
        screen.blit(text2, (WIDTH // 2 - 150, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_button = pygame.mouse.get_pressed()

        if mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(range(560, 621)):
            easy_level()
        elif mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(
                range(650, 711)):
            hard_level()
        elif mouse_button == (1, 0, 0) and mouse_pos[0] in list(range(50, 301)) and mouse_pos[1] in list(
                range(740, 801)):
            pygame.quit()
        # print(mouse_pos)
        pygame.display.update()

    pygame.quit()
    start()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Космострелялка)")
    clock = pygame.time.Clock()
    infoObject = pygame.display.Info()
    screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)

    pygame.mixer.music.load('../music/psikhodelika.mp4')
    pygame.mixer.music.play()

    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    FPS = 60
    BACK_END = 2

    # Задаем цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    start()
