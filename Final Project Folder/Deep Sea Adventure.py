import pygame as pg
import random
import sys

# Importing your custom logic
from bresenham import draw_bresenham
from Floodfill import flood_fill

# Increase recursion depth for Flood Fill (needed for small shapes)
sys.setrecursionlimit(10000)

pg.init()
WIDTH, HEIGHT = 1080, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("arial", 36)

# ---------------- HELPER DRAWING FUNCTION ----------------
def draw_filled_rect(surface, rect, color):
    """Draws a rectangle using Bresenham lines and safely fills it."""
    if not surface.get_rect().colliderect(rect):
        return

    draw_bresenham(surface, rect.left, rect.top, rect.right, rect.top, color)
    draw_bresenham(surface, rect.left, rect.bottom, rect.right, rect.bottom, color)
    draw_bresenham(surface, rect.left, rect.top, rect.left, rect.bottom, color)
    draw_bresenham(surface, rect.right, rect.top, rect.right, rect.bottom, color)
    
    if 0 <= rect.centerx < WIDTH and 0 <= rect.centery < HEIGHT:
        try:
            flood_fill(surface, rect.centerx, rect.centery, color)
        except RecursionError:
            pass

# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self, y1, y2):
        self.w = 30
        self.h = 30
        self.y1 = y1
        self.y2 = y2
        self.reset()

    def reset(self):
        self.rect = pg.Rect(
            WIDTH + random.randint(0, 300),
            random.randint(self.y1, self.y2),
            self.w,
            self.h
        )
        self.velocity = random.randint(200, 350)

    def update(self, dt):
        self.rect.x -= self.velocity * dt
        if self.rect.right < 0:
            self.reset()

    def draw(self, surface):
        draw_filled_rect(surface, self.rect, (255, 60, 60))

# ---------------- TREASURE ----------------
class Treasure:
    def __init__(self, y1, y2):
        self.size = 20
        self.y1 = y1
        self.y2 = y2
        self.reset()

    def reset(self):
        self.rect = pg.Rect(
            WIDTH + random.randint(200, 600),
            random.randint(self.y1, self.y2),
            self.size,
            self.size
        )
        self.velocity = random.randint(180, 320)

    def update(self, dt):
        self.rect.x -= self.velocity * dt
        if self.rect.right < 0:
            self.reset()

    def draw(self, surface):
        draw_filled_rect(surface, self.rect, (255, 215, 0))

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.rect = pg.Rect(WIDTH//2, HEIGHT//2, 30, 30)
        self.vel_x = 0
        self.vel_y = 0
        self.max_speed = 450
        self.accel = 2200
        self.friction = 8  # Adjusted for better feel
        self.lives = 3
        self.score = 0
        self.hit_cd = 0

    def input(self, dt):
        keys = pg.key.get_pressed()
        ax, ay = 0, 0
        if keys[pg.K_a] or keys[pg.K_LEFT]: ax = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]: ax = 1
        if keys[pg.K_w] or keys[pg.K_UP]: ay = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]: ay = 1

        # Apply acceleration based on input
        self.vel_x += ax * self.accel * dt
        self.vel_y += ay * self.accel * dt

    def update(self, dt):
        # Apply friction/drag continuously
        self.vel_x *= (1 - self.friction * dt)
        self.vel_y *= (1 - self.friction * dt)

        # Clamp speed to max_speed
        if abs(self.vel_x) > self.max_speed:
            self.vel_x = (self.vel_x / abs(self.vel_x)) * self.max_speed
        if abs(self.vel_y) > self.max_speed:
            self.vel_y = (self.vel_y / abs(self.vel_y)) * self.max_speed

        # Stop tiny movements to prevent drift jitter
        if abs(self.vel_x) < 1: self.vel_x = 0
        if abs(self.vel_y) < 1: self.vel_y = 0

        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt
        self.rect.clamp_ip(pg.Rect(0,0,WIDTH,HEIGHT))
        
        if self.hit_cd > 0: self.hit_cd -= dt

    def enemy_collision(self, enemy):
        if self.rect.colliderect(enemy.rect) and self.hit_cd <= 0:
            self.lives -= 1
            self.hit_cd = 1
            enemy.reset()

    def treasure_collision(self, treasure):
        if self.rect.colliderect(treasure.rect):
            self.score += 1
            treasure.reset()

    def draw(self, surface):
        draw_filled_rect(surface, self.rect, (60, 255, 60))

# ---------------- SETUP ----------------
lanes = [(40,200),(200,360),(360,520),(520,680)]
enemies = [Enemy(y1,y2) for (y1,y2) in lanes]
treasures = [Treasure(y1,y2) for (y1,y2) in lanes]
player = Player()
state = "MENU"

# ---------------- LOOP ----------------
running = True
while running:
    dt = clock.tick(60)/1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if state == "MENU" and event.key == pg.K_SPACE:
                state = "PLAY"
            if state == "GAMEOVER" and event.key == pg.K_r:
                player = Player()
                enemies = [Enemy(y1,y2) for (y1,y2) in lanes]
                treasures = [Treasure(y1,y2) for (y1,y2) in lanes]
                state = "PLAY"

    screen.fill((0,80,80))

    if state == "MENU":
        t = font.render("Press SPACE to Start", True, (255,255,255))
        screen.blit(t,(WIDTH//2-180,HEIGHT//2))

    elif state == "PLAY":
        player.input(dt)
        player.update(dt)

        for e in enemies:
            e.update(dt)
            player.enemy_collision(e)
            e.draw(screen)

        for tr in treasures:
            tr.update(dt)
            player.treasure_collision(tr)
            tr.draw(screen)

        player.draw(screen)

        screen.blit(font.render(f"Lives: {player.lives}",True,(255,255,255)),(20,20))
        screen.blit(font.render(f"Score: {player.score}",True,(255,255,255)),(20,60))

        if player.lives <= 0:
            state = "GAMEOVER"

    elif state == "GAMEOVER":
        screen.blit(font.render("GAME OVER",True,(255,50,50)),(WIDTH//2-100,HEIGHT//2-40))
        screen.blit(font.render(f"Score: {player.score}",True,(255,255,255)),(WIDTH//2-80,HEIGHT//2))
        screen.blit(font.render("Press R to Restart",True,(255,255,255)),(WIDTH//2-140,HEIGHT//2+50))

    pg.display.flip()

pg.quit()