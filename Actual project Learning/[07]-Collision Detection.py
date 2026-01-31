"""
This program contains the basic collision detection system, we will later implement this with an enemy
For now we shall observe for our player and a random rectangle level 
"""

import pygame as pg
import random

# ---------- setup ----------
pg.init()
WIDTH, HEIGHT = 1080, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# ---------- player ----------
player_size = 40
player_speed = 300
player_rect = pg.Rect(WIDTH//2, HEIGHT//2, player_size, player_size)

# ---------- random box ----------
box_size = 40
box_rect = pg.Rect(
    random.randint(0, WIDTH - box_size),
    random.randint(0, HEIGHT - box_size),
    box_size,
    box_size
)

# ---------- game loop ----------
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # ---------- movement ----------
    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        player_rect.y -= player_speed * dt
    if keys[pg.K_s]:
        player_rect.y += player_speed * dt
    if keys[pg.K_a]:
        player_rect.x -= player_speed * dt
    if keys[pg.K_d]:
        player_rect.x += player_speed * dt

    # ---------- collision ----------
    if player_rect.colliderect(box_rect):
        box_rect.x = random.randint(0, WIDTH - box_size)
        box_rect.y = random.randint(0, HEIGHT - box_size)

    # ---------- draw ----------
    screen.fill((30, 30, 30))
    pg.draw.rect(screen, (50, 200, 50), player_rect)
    pg.draw.rect(screen, (200, 50, 50), box_rect)
    pg.display.flip()

pg.quit()
