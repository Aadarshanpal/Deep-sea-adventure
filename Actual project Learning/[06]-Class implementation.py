import pygame as pg


#Initianlizing the Basics
WIDTH, HEIGHT = 1920, 1080


#Initializing pygame
pg.init()


#Initialize the screen
screen = pg.display.set_mode((WIDTH,HEIGHT))


#Player Basics
Player_size = 40 
PlayerX = WIDTH // 2
PlayerY = HEIGHT // 2


#Initializing the clock
clock = pg.time.Clock()


#Initializing the players class:
class Player:
    def __init__(self,x,y,size):
        

        #Positions
        self.x = x
        self.y = y
        self.size = size


        #Velocity [Initial]
        self.vel_x = 0
        self.vel_y = 0
        self.is_on_ground = False

        #Constants
        self.accel = 1300
        self.gravity = 1300
        self.max_speed = 300
        self.friction = 2
        self.jump_strength = 2000 #My boy is flyinggggggggg

    def handle_input(self,dt):
        
        
        #User input
        keys = pg.key.get_pressed()
        
        
        #X-axis input case:
        if keys[pg.K_LEFT]:
            self.vel_x -= self.accel * dt
        elif keys[pg.K_RIGHT]:
            self.vel_x += self.accel * dt
        else:
            self.vel_x -= self.vel_x*self.friction * dt           #Ground friction
        if keys[pg.K_SPACE] and self.is_on_ground == True:
            self.vel_y -= self.jump_strength
            self.is_on_ground = False

        #Y-axis gravity:
        if self.is_on_ground == False:
            self.vel_y += self.gravity * dt                          #Applying Gravity
        self.Integrity_and_Physics(dt)
    
    
    def Integrity_and_Physics(self,dt):                             
        self.vel_x = max( -self.max_speed, min( self.max_speed, self.vel_x))
        #self.vel_y = max( -self.max_speed, min( self.max_speed, self.vel_y))
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        self.x = max( 0, min( self.x, WIDTH-self.size))
        self.y = max( 0, min( self.y, HEIGHT-self.size))
        if self.y >= (HEIGHT - self.size):
            self.y = HEIGHT - self.size
            self.vel_y = 0
            self.is_on_ground = True
    def draw(self,surface):
        pg.draw.rect( surface, ( 255, 255, 255), ( self.x, self.y, self.size, self.size))





player = Player(PlayerX,PlayerY,Player_size)
#Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill(( 0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    player.handle_input(dt)
    player.draw(screen)
    pg.display.flip()
