import time as t
from pygame import *
from random import randint
import os

init()
mixer.init()
font.init()

FPS=60
Game=True



window = display.set_mode((700,500))
display.set_caption("PONG!")
display.set_icon(image.load("icon.png"))
bg = transform.scale(image.load("bg.png"), (700, 500))
clock = time.Clock()

mixer.music.load("music.wav")
t1 = t.time()
mixer.music.play()

Hit1 = mixer.Sound("Hit1.wav") # High pitch
Hit1_ = t.time()
Hit2 = mixer.Sound("Hit2.wav") # Low pitch
Hit2_ = t.time()

class GameSprite(sprite.Sprite):
    def __init__(self, speed, img, size_x, size_y, x, y) -> None:
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img), (size_x, size_y))
        self.speed = speed

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self) -> None:
        window.blit(self.image, (self.rect.x, self.rect.y))

p1 = GameSprite(2, "plat.png", 3, 50, 3, 225)
p2 = GameSprite(2, "plat.png", 3, 50, 695, 225)
ball = GameSprite(4, "", )

Fein = font.SysFont('Arial', 20)

while Game:
    Hit1__ = t.time()
    Hit2__ = t.time()
    t2 = t.time()
    if t2-t1 > 8:
        t1 = t.time()
        mixer.music.play()

    for e in event.get():
        if e.type == QUIT:
            Game = False

    window.blit(bg, (0, 0))
    p1.reset()
    p2.reset()

    keys = key.get_pressed()
    # ------- sfx test -------
    if keys[K_h] and (Hit1__-Hit1_ > 1):
        Hit1_ = t.time()
        Hit1.play()
    if keys[K_g] and (Hit2__-Hit2_ > 1):
        Hit2_ = t.time()
        Hit2.play()

    # ------- movement -------
    if keys[K_w] and p1.rect.y >= 55: p1.rect.y -= p1.speed
    if keys[K_s] and p1.rect.y <= 395: p1.rect.y += p1.speed
    if keys[K_p] and p2.rect.y >= 55: p2.rect.y -= p1.speed
    if keys[K_l] and p2.rect.y <= 395: p2.rect.y += p1.speed

    if keys[K_ESCAPE]: pass

    # ------- ball mov -------
    

    display.update()
    clock.tick(FPS)