import pygame
import random
import time

from pygame.constants import PREALLOC


WIDTH = 600
HEIGHT = 600 
FPS = 5
pygame.init()
pygame.mixer.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
start = True
res = open("score.txt", "r")
score = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
    def Update(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
    def Update(self):
        x = random.randint(40, 560)
        y = random.randint(40, 560)
        self.rect.x = x - (x%20)-10
        self.rect.y = y - (y%20)-10


class zmeika_body(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    def Update(self, x, y):
        self.rect.x = x
        self.rect.y = y


clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
apple = Apple()
all_sprites.add(player)
all_sprites.add(apple)
command = (0, 0)
zmeika_commands = ()
body = {}
timer = 2
body_time = 1
time_zm = 0
ok = True
f1 = pygame.font.Font(None, 36)
sc = res.read()
if sc == "":
    sc = 0
print(sc)



while timer <= len(body)+3:
    clock.tick(20)
    player.Update(command[0], command[1])
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    if player.rect.x > 600:
        player.rect.x = 10
    elif player.rect.x < 0:
        player.rect.x = 590
    elif player.rect.y > 600:
        player.rect.y = 10
    elif player.rect.y < 0:
        player.rect.y = 590
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
    if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
        if command != (20, 0):
            command = (-20, 0)
    elif pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
        if command != (-20, 0):
            command = (20, 0)
    elif pygame.key.get_pressed()[pygame.K_UP] == 1:
        if command != (0, 20):
            command = (0, -20)
    elif pygame.key.get_pressed()[pygame.K_DOWN] == 1:
        if command != (0, -20):
            command = (0, 20)
    if (player.rect.x > apple.rect.x-20 and player.rect.x < apple.rect.x+20) and (player.rect.y > apple.rect.y-20 and player.rect.y < apple.rect.y+20):
        score += 10
        body_time += 1
        if ok:
            zmeika_commands = zmeika_commands[-len(body):] + (player.rect.x, player.rect.y)
            ok = False
        new_body = zmeika_body(zmeika_commands[-2], zmeika_commands[-1])
        all_sprites.add(new_body)
        body[body_time] = new_body
        apple.Update()
    if len(body) >= 1:
        time_zm += 2
        zmeika_commands = zmeika_commands[-len(body):] + (player.rect.x, player.rect.y)
        for i in body.keys():
            if i == 2:
                continue
            if body[i].rect == player.rect:
                if score > int(sc):
                    res2 = open("score.txt", "w")
                    res2.write(str(score))
                timer = 100000
        body[timer].Update(zmeika_commands[-2], zmeika_commands[-1])
        timer += 1
        
        if timer == len(body)+2:
            timer = 2
            time_zm = 0
        if score > int(sc):
            text1 = f1.render("result: "+str(score)+" score: "+str(score), True,
                    (180, 0, 0))
            screen.blit(text1, (10, 50))
        else:
            text1 = f1.render("result: "+str(score)+" score: "+str(sc), True,
                (180, 0, 0))
            screen.blit(text1, (10, 50))
    
    pygame.display.flip()
    