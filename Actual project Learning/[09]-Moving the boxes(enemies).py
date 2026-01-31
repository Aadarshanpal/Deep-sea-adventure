"""
In this one we add multiple boxes that can be collided with and they will move back to the right of the screen
That is, return to a random position in their range.
"""

import pygame as pg
import random
pg.init()
WIDTH, HEIGHT = 1080, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class Enemy:
    def __init__(self,x,y,w,h,y1,y2):
        self.rect = pg.Rect(x,y,w,h)
        self.velocity = random.randint(150,300)
        self.y1 = y1
        self.y2 = y2
    def collision_detected(self):
        self.rect.x = WIDTH
        self.rect.y = random.randint(self.y1, self.y2)

    def movement(self, dt):
        self.rect.x -= self.velocity * dt
        if self.rect.x < -40:
            self.collision_detected()
    def draw(self,surface):
        pg.draw.rect(surface, (255, 50, 50), self.rect)

Enemies = [Enemy(WIDTH,random.randint(40,200),40,40,40,200),
         Enemy(WIDTH,random.randint(200,360),40,40,200,360),
         Enemy(WIDTH,random.randint(360,520),40,40,360,520),
         Enemy(WIDTH,random.randint(520,680),40,40,520,680)]

class Player:
    def __init__(self,x,y,w,h):
        self.rect = pg.Rect(x,y,w,h)

        self.vel_x = 0
        self.vel_y = 0
        
        self.max_speed = 400
        self.accel = 1300
        self.friction = 8
        
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

    def collision_check(self,enemy):
        if self.rect.colliderect(enemy.rect):
            enemy.collision_detected()
            

    def draw(self,surface):
        pg.draw.rect( surface, ( 50, 255, 50), self.rect)

player = Player(WIDTH//2,HEIGHT//2,40,40)

running = True
while running:
    screen.fill((0, 80, 80))
    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    player.input(dt)
    player.update(dt)
    for enemy in Enemies:
        enemy.movement(dt)
        player.collision_check(enemy)
        enemy.draw(screen)
    player.draw(screen)
    pg.display.flip()