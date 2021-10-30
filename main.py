import pygame
import os
import random

pygame.mixer.init(frequency=44100, size=-16, channels=10, buffer=2 ** 12)
pygame.init()

size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
screen_rect = (0, 0, width, height)
pygame.display.set_caption("braindead tf2 clicker by fatnet")

config = open("data/userdata/config.txt", 'r+')  # \\
counter = int(config.readline())

GRAVITY = 1


def load_image(name, colorkey=None):
    try:
        path = 'data/' + name  # \\
        image = pygame.image.load(path)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, var):
        if var == 'blood':
            super().__init__(blood)
            self.fire = [load_image("sprites/particles/blood.png")]  # \\
            for scale in (1, 2, 4, 8, 12, 16, 25):
                self.fire.append(
                    pygame.transform.scale(self.fire[0], (scale, scale)))
        if var == 'fire':
            super().__init__(fire)
            self.fire = [load_image("sprites/particles/fire_red.png"),
                         load_image("sprites/particles/fire_orange.png"),
                         load_image("sprites/particles/fire_yellow.png")]  # \\
            for scale in (1, 2, 4, 8, 12, 16):
                self.fire.append(
                    pygame.transform.scale(self.fire[random.choice([0, 1, 2])],
                                           (scale, scale)))
        if var == 'steel':
            super().__init__(steel)
            self.fire = [load_image("sprites/particles/steel.png")]  # \\
            for scale in (1, 2, 4, 8, 12, 16):
                self.fire.append(
                    pygame.transform.scale(self.fire[0], (scale, scale)))
        if var == 'meat':
            super().__init__(meat)
            self.fire = [load_image("sprites/playermodels/dead.png")]  # \\
            for scale in (1, 2, 4, 8, 16, 24, 32, 48, 60):
                self.fire.append(
                    pygame.transform.scale(self.fire[0], (scale, scale)))

        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
        if self.rect.colliderect(floor1.rect):
            self.kill()
        if self.rect.colliderect(floor2.rect):
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bullet)
        self.image = load_image("sprites/particles/bullet.png")  # \\
        self.rect = self.image.get_rect()

        self.velocity = 18
        self.rect.x, self.rect.y = (160, 525)

    def update(self):
        self.rect.x += self.velocity
        if not self.rect.colliderect(screen_rect):
            self.kill()
        if self.rect.colliderect(floor1.rect):
            self.kill()
        if self.rect.colliderect(floor2.rect):
            self.kill()
        if self.rect.colliderect(en.rect):
            pygame.mixer.Channel(random.choice((5, 6, 7))).play(
                pygame.mixer.Sound("data/sounds/death.wav"))  # \\
            create_particles((0, 0), 'blood')
            create_particles((999, 0), 'blood')
            create_particles((499, 0), 'blood')
            create_particles((825, 425), 'meat')
            en.image = random.choice(enemies)
            self.kill()


def create_particles(position, var):
    if var == 'blood':
        particle_count = 80
        width_fire = range(-8, 10)
        height_fire = range(-8, 10)
    if var == 'fire':
        particle_count = 150
        width_fire = range(-2, 3)
        height_fire = range(-75, 0)
    if var == 'steel':
        particle_count = 50
        width_fire = range(-8, 10)
        height_fire = range(-8, 10)
    if var == 'meat':
        particle_count = 60
        width_fire = range(-8, 10)
        height_fire = range(-8, 10)
    for _ in range(particle_count):
        Particle(position, random.choice(width_fire),
                 random.choice(height_fire), var)


def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()


background_image = load_image("maps/1.jpg")  # \\
flags_bg = [True, True, True, True, True, True, True, True]

flags_wp = []
for i in range(21):
    flags_wp.append(True)

enemies = [load_image('sprites/playermodels/a.png'),
           load_image('sprites/playermodels/b.png'),
           load_image('sprites/playermodels/c.png')]  # \\

blood = pygame.sprite.Group()
meat = pygame.sprite.Group()
steel = pygame.sprite.Group()
fire = pygame.sprite.Group()
bottom = pygame.sprite.Group()
enemy = pygame.sprite.Group()
wpn = pygame.sprite.Group()
me = pygame.sprite.Group()
bullet = pygame.sprite.Group()

en = pygame.sprite.Sprite()
en.image = random.choice(enemies)
en.rect = en.image.get_rect()
en.rect.right = 900
en.rect.bottom = 675
en.add(enemy)

floor1 = pygame.sprite.Sprite()
floor1.image = load_image("sprites/buildings/floor.png")  # \\
floor1.rect = floor1.image.get_rect()
floor1.rect.x = 750
floor1.rect.y = 675
floor2 = pygame.sprite.Sprite()
floor2.image = load_image("sprites/buildings/floor.png")  # \\
floor2.rect = floor2.image.get_rect()
floor2.rect.x = 0
floor2.rect.y = 675
bottom.add(floor1)
bottom.add(floor2)

weapon = pygame.sprite.Sprite()
weapon.image = load_image("sprites/weapons/1.png")  # \\
weapon.rect = weapon.image.get_rect()
weapon.rect.x = 230
weapon.rect.y = 50
wpn.add(weapon)

player = pygame.sprite.Sprite()
player.image = load_image("sprites/playermodels/player.png")
player.rect = player.image.get_rect()
player.rect.x = 50
player.rect.y = 430
me.add(player)

clock = pygame.time.Clock()
running = True

pygame.mixer.Channel(0).play(pygame.mixer.Sound("data/music/background.mp3"),
                             loops=-1)  # \\

mouse_group = pygame.sprite.Group()
mouse_image = load_image('userdata/arrow.png')  # \\
mouse_image = pygame.transform.scale(mouse_image, (40, 40))
mouse_sprite = pygame.sprite.Sprite(mouse_group)
mouse_sprite.image = mouse_image
mouse_sprite.rect = mouse_sprite.image.get_rect()

pygame.mouse.set_visible(False)

basicfont = pygame.font.Font("data/userdata/font.ttf", 96)  # \\
text1 = basicfont.render(str(counter), True, (255, 165, 0))
textrect1 = text1.get_rect()
textrect1.x = 0
textrect1.y = 0
text2 = basicfont.render("Rank:", True, (255, 165, 0))
textrect2 = text2.get_rect()
textrect2.x = 0
textrect2.y = 100

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            deleteContent(config)
            config.write(str(counter))
        if event.type == pygame.MOUSEBUTTONDOWN or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            counter += 1
            create_particles(pygame.mouse.get_pos(), 'steel')
            Bullet()
            text1 = basicfont.render(str(counter), True, (255, 165, 0))
            textrect1 = text1.get_rect()
            pygame.mixer.Channel(random.choice((1, 2, 3, 4))).play(
                pygame.mixer.Sound("data/sounds/shotgun.wav"))  # \\
        if event.type == pygame.MOUSEMOTION:
            mouse_sprite.rect.x = event.pos[0]
            mouse_sprite.rect.y = event.pos[1]
    if pygame.mouse.get_focused():
        mouse_group.draw(screen)

    if counter >= 1e6 and flags_wp[20]:
        weapon.image = load_image("sprites/weapons/22.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 20))
        for i in range(20 - 20):
            flags_wp.append(True)
    elif counter >= 5e5 and flags_wp[19]:
        weapon.image = load_image("sprites/weapons/21.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 19))
        for i in range(20 - 19):
            flags_wp.append(True)
    elif counter >= 2e5 and flags_wp[18]:
        weapon.image = load_image("sprites/weapons/20.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 18))
        for i in range(20 - 18):
            flags_wp.append(True)
    elif counter >= 1e5 and flags_wp[17]:
        weapon.image = load_image("sprites/weapons/19.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 17))
        for i in range(20 - 17):
            flags_wp.append(True)
    elif counter >= 5e4 and flags_wp[16]:
        weapon.image = load_image("sprites/weapons/18.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 16))
        for i in range(20 - 16):
            flags_wp.append(True)
    elif counter >= 2e4 and flags_wp[15]:
        weapon.image = load_image("sprites/weapons/17.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 15))
        for i in range(20 - 15):
            flags_wp.append(True)
    elif counter >= 1e4 and flags_wp[14]:
        weapon.image = load_image("sprites/weapons/16.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 14))
        for i in range(20 - 14):
            flags_wp.append(True)
    elif counter >= 9e3 and flags_wp[13]:
        weapon.image = load_image("sprites/weapons/15.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 13))
        for i in range(20 - 13):
            flags_wp.append(True)
    elif counter >= 7e3 and flags_wp[12]:
        weapon.image = load_image("sprites/weapons/14.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 12))
        for i in range(20 - 12):
            flags_wp.append(True)
    elif counter >= 5e3 and flags_wp[11]:
        weapon.image = load_image("sprites/weapons/13.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 11))
        for i in range(20 - 11):
            flags_wp.append(True)
    elif counter >= 3e3 and flags_wp[10]:
        weapon.image = load_image("sprites/weapons/12.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 10))
        for i in range(20 - 10):
            flags_wp.append(True)
    elif counter >= 1e3 and flags_wp[9]:
        weapon.image = load_image("sprites/weapons/11.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 9))
        for i in range(20 - 9):
            flags_wp.append(True)
    elif counter >= 8e2 and flags_wp[8]:
        weapon.image = load_image("sprites/weapons/10.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 8))
        for i in range(20 - 8):
            flags_wp.append(True)
    elif counter >= 5e2 and flags_wp[7]:
        weapon.image = load_image("sprites/weapons/9.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 7))
        for i in range(20 - 7):
            flags_wp.append(True)
    elif counter >= 4e2 and flags_wp[6]:
        weapon.image = load_image("sprites/weapons/8.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 6))
        for i in range(20 - 6):
            flags_wp.append(True)
    elif counter >= 3e2 and flags_wp[5]:
        weapon.image = load_image("sprites/weapons/7.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 5))
        for i in range(20 - 5):
            flags_wp.append(True)
    elif counter >= 2e2 and flags_wp[4]:
        weapon.image = load_image("sprites/weapons/6.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 4))
        for i in range(20 - 4):
            flags_wp.append(True)
    elif counter >= 1e2 + 5e1 and flags_wp[3]:
        weapon.image = load_image("sprites/weapons/5.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 3))
        for i in range(20 - 3):
            flags_wp.append(True)
    elif counter >= 1e2 and flags_wp[2]:
        weapon.image = load_image("sprites/weapons/4.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 2))
        for i in range(20 - 2):
            flags_wp.append(True)
    elif counter >= 5e1 and flags_wp[1]:
        weapon.image = load_image("sprites/weapons/3.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 1))
        for i in range(20 - 1):
            flags_wp.append(True)
    elif counter >= 1e1 and flags_wp[0]:
        weapon.image = load_image("sprites/weapons/2.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_wp = [False] * (21 - (20 - 0))
        for i in range(20 - 0):
            flags_wp.append(True)

    if counter >= 2e5 and flags_bg[7]:
        background_image = load_image("maps/9.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 7))
        for i in range(7 - 7):
            flags_bg.append(True)
    elif counter >= 1e5 + 5e4 and flags_bg[6]:
        background_image = load_image("maps/8.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 6))
        for i in range(7 - 6):
            flags_bg.append(True)
    elif counter >= 1e5 and flags_bg[5]:
        background_image = load_image("maps/7.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 5))
        for i in range(7 - 5):
            flags_bg.append(True)
    elif counter >= 5e4 and flags_bg[4]:
        background_image = load_image("maps/6.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 4))
        for i in range(7 - 4):
            flags_bg.append(True)
    elif counter >= 1e4 and flags_bg[3]:
        background_image = load_image("maps/5.png")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 3))
        for i in range(7 - 3):
            flags_bg.append(True)
    elif counter >= 5e3 and flags_bg[2]:
        background_image = load_image("maps/4.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 2))
        for i in range(7 - 2):
            flags_bg.append(True)
    elif counter >= 1e3 and flags_bg[1]:
        background_image = load_image("maps/3.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 1))
        for i in range(7 - 1):
            flags_bg.append(True)
    elif counter >= 5e2 and flags_bg[0]:
        background_image = load_image("maps/2.jpg")  # \\
        create_particles((249, 1000), 'fire')
        create_particles((499, 1000), 'fire')
        create_particles((749, 1000), 'fire')
        flags_bg = [False] * (8 - (7 - 0))
        for i in range(7 - 0):
            flags_bg.append(True)

    screen.blit(background_image, [0, 0])

    blood.update()
    fire.update()
    steel.update()
    meat.update()
    bullet.update()

    me.draw(screen)
    enemy.draw(screen)
    meat.draw(screen)
    blood.draw(screen)
    fire.draw(screen)
    bottom.draw(screen)
    steel.draw(screen)
    bullet.draw(screen)
    wpn.draw(screen)
    mouse_group.draw(screen)

    screen.blit(text1, textrect1)
    screen.blit(text2, textrect2)

    pygame.display.flip()
    clock.tick(50)

config.close()
pygame.quit()
