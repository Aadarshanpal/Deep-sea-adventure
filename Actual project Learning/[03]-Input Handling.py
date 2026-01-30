import pygame as pg    

WIDTH, HEIGHT = 800,600

pg.init()

screen = pg.display.set_mode((WIDTH,HEIGHT))  

#Defining a clock (You will know why)
clock = pg.time.Clock()


#Player properties
PlayerX = WIDTH // 2
PlayerY = HEIGHT // 2
Player_Size = 40
Player_Speed = 5      #How many pixels the player moves per frame (acts like velocity)


#Function to draw the player
def draw(surface):
    pg.draw.rect(surface, (255, 255, 255), (PlayerX, PlayerY, Player_Size, Player_Size))


#Function to take input and update player position
def input():
    global PlayerX,PlayerY   #We use global because we want to MODIFY the PlayerX, PlayerY defined outside the function

    keys = pg.key.get_pressed()  
    #This gives a list of all keys and their current state (pressed or not)

    if keys[pg.K_LEFT]:  
        PlayerX -= Player_Speed  
        #If '<-' is held, we subtract from X → object moves left

    if keys[pg.K_RIGHT]:  
        PlayerX += Player_Speed  
        #If '->' is held, we add to X → object moves right
    
    if keys[pg.K_UP]:  
        PlayerY -= Player_Speed  
        #If 'Up arrow' is held, we subtract from X → object moves left

    if keys[pg.K_DOWN]:  
        PlayerY += Player_Speed  
        #If 'Down arrow' is held, we add to X → object moves right
    PlayerX = max(0,min(PlayerX,WIDTH-Player_Size))
    PlayerY = max(0,min(PlayerY,HEIGHT-Player_Size))

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    input()        #Input is checked every frame so movement feels continuous
    draw(screen)
    clock.tick(60)      #This returns the time difference between the current frame and the last frame 
    pg.display.flip()   #and also limits the fps to 60; for its use, 
                        #we need to understand delta time which isnt possible to explain here, go watch a youtube vid 
