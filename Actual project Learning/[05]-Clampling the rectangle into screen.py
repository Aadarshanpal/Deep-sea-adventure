"""
Making the player stay in bounds/ Stay in screen.
"""

import pygame as pg    

WIDTH, HEIGHT = 800,600

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))

clock = pg.time.Clock()


PlayerX = WIDTH // 2
PlayerY = HEIGHT // 2
Player_Size = 40

velocity_x = 0
velocity_y = 0

acceleration = 1200
friction = 8


def draw(surface):
    pg.draw.rect(surface, (255, 255, 255),
                 (PlayerX, PlayerY, Player_Size, Player_Size))


def input(dt):
    global velocity_x, velocity_y

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        velocity_x -= acceleration * dt
    if keys[pg.K_RIGHT]:
        velocity_x += acceleration * dt

    if keys[pg.K_UP]:
        velocity_y -= acceleration * dt
    if keys[pg.K_DOWN]:
        velocity_y += acceleration * dt


def apply_physics(dt):
    global PlayerX, PlayerY, velocity_x, velocity_y

    velocity_x -= velocity_x * friction * dt
    velocity_y -= velocity_y * friction * dt

    PlayerX += velocity_x * dt
    PlayerY += velocity_y * dt

    #Clamp player inside screen bounds
    if PlayerX < 0:
        PlayerX = 0
        velocity_x = 0

    if PlayerX > WIDTH - Player_Size:
        PlayerX = WIDTH - Player_Size
        velocity_x = 0

    if PlayerY < 0:
        PlayerY = 0
        velocity_y = 0

    if PlayerY > HEIGHT - Player_Size:
        PlayerY = HEIGHT - Player_Size
        velocity_y = 0


running = True
while running:
    dt = clock.tick(60) / 1000

    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    input(dt)
    apply_physics(dt)
    draw(screen)

    pg.display.flip()
