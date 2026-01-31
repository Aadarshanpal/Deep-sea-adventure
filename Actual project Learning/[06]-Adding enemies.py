"""
In this program we add an enemy; he just spawns at a random place to the right of the screen and moves to the left with a random constant speed.
We cant interract with him yet.
"""


import pygame as pg
import random
#Initializatiom
pg.init()
WIDTH,HEIGHT = 1080,720
screen = pg.display.set_mode((WIDTH,HEIGHT))
clock = pg.time.Clock()

#Enemy
class Enemy:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)       #pg.Rect() is a function that helps to represent data more easily

        self.vel = random.randint(100,200) #The enemy will move at a random speed 
    def update(self,dt):
        self.rect.x -= self.vel * dt
    
    def draw(self,surface):
        pg.draw.rect( surface, ( 255, 255, 255), self.rect)

#Player
class Player:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)

        
        self.vel_x = 0
        self.vel_y = 0
        
        
        self.max_speed = 400
        self.accel = 1300
        self.friction = 5
        
    def input(self,dt):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.vel_x -= self.accel * dt
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.vel_x += self.accel * dt
        else:
            self.vel_x -= self.vel_x * self.friction * dt
        
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.vel_y -= self.accel * dt
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            self.vel_y += self.accel * dt
        else:
            self.vel_y -= self.vel_y * self.friction * dt
    
    def update(self,dt):
        self.vel_x = max(-self.max_speed, min(self.vel_x , self.max_speed))
        self.vel_y = max(-self.max_speed, min(self.vel_y , self.max_speed))

        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt

        self.rect.x = max(0, min(self.rect.x,WIDTH - self.rect.w))
        self.rect.y = max(0, min(self.rect.y,HEIGHT - self.rect.h))

    def draw(self,surface):
        pg.draw.rect( surface, ( 255, 255, 255), self.rect)

player = Player(WIDTH//2,HEIGHT//2,40,40)
enemy = Enemy(WIDTH, random.randint(40,HEIGHT-80),random.randint(40,100),40)

running = True
while running:
    screen.fill((0, 80, 80))
    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    player.input(dt)
    enemy.update(dt)
    player.update(dt)
    player.draw(screen)
    enemy.draw(screen)
    pg.display.flip()