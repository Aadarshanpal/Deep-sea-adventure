import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 1920, 1080
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("arial", 36)

# -------- LOAD IMAGES --------
player_img = pg.image.load("Project Codes/Images/player.png").convert_alpha()
enemy_img = pg.image.load("Project Codes/Images/enemy.png").convert_alpha()
treasure_img = pg.image.load("Project Codes/Images/treasure.png").convert_alpha()
background_img = pg.image.load("Project Codes/Images/background5.jpeg").convert()

player_img = pg.transform.scale(player_img,(100,100))
enemy_img = pg.transform.scale(enemy_img,(100,100))
treasure_img = pg.transform.scale(treasure_img,(50,50))
background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))

bg_x = 0
bg_speed = 120

# ---------------- ENEMY ----------------
class Enemy:
    def __init__(self, y1, y2):
        self.y1 = y1
        self.y2 = y2
        self.reset()

    def reset(self):
        self.rect = pg.Rect(
            WIDTH + random.randint(0, 300),
            random.randint(self.y1, self.y2),
            40, 40
        )
        self.velocity = random.randint(200, 350)

    def update(self, dt):
        self.rect.x -= self.velocity * dt
        if self.rect.right < 0:
            self.reset()

    def draw(self, surface):
        surface.blit(enemy_img, self.rect)

# ---------------- TREASURE ----------------
class Treasure:
    def __init__(self, y1, y2):
        self.y1 = y1
        self.y2 = y2
        self.reset()

    def reset(self):
        self.rect = pg.Rect(
            WIDTH + random.randint(200, 600),
            random.randint(self.y1, self.y2),
            30, 30
        )
        self.velocity = random.randint(180, 320)

    def update(self, dt):
        self.rect.x -= self.velocity * dt
        if self.rect.right < 0:
            self.reset()

    def draw(self, surface):
        surface.blit(treasure_img, self.rect)

# ---------------- PLAYER ----------------
class Player:
    def __init__(self):
        self.rect = pg.Rect(WIDTH//2, HEIGHT//2, 40, 40)
        self.vel_x = 0
        self.vel_y = 0

        self.max_speed = 400
        self.accel = 1800
        self.friction = 12

        self.lives = 3
        self.score = 0
        self.hit_cd = 0

    def input(self, dt):
        keys = pg.key.get_pressed()

        ax = 0
        ay = 0

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            ax = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            ax = 1
        if keys[pg.K_w] or keys[pg.K_UP]:
            ay = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            ay = 1

        self.vel_x += ax * self.accel * dt
        self.vel_y += ay * self.accel * dt

        if ax == 0:
            self.vel_x -= self.vel_x * self.friction * dt
        if ay == 0:
            self.vel_y -= self.vel_y * self.friction * dt

        if abs(self.vel_x) < 5:
            self.vel_x = 0
        if abs(self.vel_y) < 5:
            self.vel_y = 0

    def update(self, dt):
        self.vel_x = max(-self.max_speed, min(self.vel_x, self.max_speed))
        self.vel_y = max(-self.max_speed, min(self.vel_y, self.max_speed))

        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt
        self.rect.clamp_ip(pg.Rect(0,0,WIDTH,HEIGHT))

        if self.hit_cd > 0:
            self.hit_cd -= dt

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
        surface.blit(player_img, self.rect)

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

    # ----- BACKGROUND DRAW -----
    bg_x -= bg_speed * dt
    if bg_x <= -WIDTH:
        bg_x = 0

    screen.blit(background_img, (bg_x, 0))
    screen.blit(background_img, (bg_x + WIDTH, 0))

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
