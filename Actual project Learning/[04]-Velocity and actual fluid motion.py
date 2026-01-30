import pygame as pg    

WIDTH, HEIGHT = 800,600

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))

clock = pg.time.Clock()   #Used to control FPS and calculate delta time


#Player properties
PlayerX = WIDTH // 2
PlayerY = HEIGHT // 2
Player_Size = 40

#Motion variables
velocity_x = 0            #How fast the player is moving horizontally
velocity_y = 0            #How fast the player is moving vertically

acceleration = 1200       #How fast velocity changes when a key is pressed
friction = 8              #How quickly velocity dies when no key is pressed


def draw(surface):
    pg.draw.rect(surface, (255, 255, 255),
                 (PlayerX, PlayerY, Player_Size, Player_Size))


def input(dt):
    global velocity_x, velocity_y

    keys = pg.key.get_pressed()

    #Horizontal movement
    if keys[pg.K_LEFT]:
        velocity_x -= acceleration * dt
    if keys[pg.K_RIGHT]:
        velocity_x += acceleration * dt

    #Vertical movement
    if keys[pg.K_UP]:
        velocity_y -= acceleration * dt
    if keys[pg.K_DOWN]:
        velocity_y += acceleration * dt


def apply_physics(dt):
    global PlayerX, PlayerY, velocity_x, velocity_y

    #Apply friction (gradually slows the player)
    velocity_x -= velocity_x * friction * dt
    velocity_y -= velocity_y * friction * dt

    #Update position using velocity
    PlayerX += velocity_x * dt
    PlayerY += velocity_y * dt


running = True
while running:
    dt = clock.tick(60) / 1000
    #dt is the time (in seconds) taken for the last frame

    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    input(dt)
    apply_physics(dt)
    draw(screen)

    pg.display.flip()
