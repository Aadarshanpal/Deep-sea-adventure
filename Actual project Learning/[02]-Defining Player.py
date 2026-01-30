import pygame as pg    

WIDTH, HEIGHT = 800,600

pg.init()

screen = pg.display.set_mode((WIDTH,HEIGHT))  


#Defining Player
PlayerX = WIDTH // 2  #Returns an integer value (We learnt in BLA that floating arithmetic is expesive and moreover, floating pixels dont exist)
PlayerY = HEIGHT // 2  #These are basically the initial positions of the player we are about to define
Player_Size = 40      #Basically the size of the player in pixels


#Defining a function to draw the player
def draw(surface):
    pg.draw.rect(surface, (255, 255, 255), (PlayerX, PlayerY, Player_Size, Player_Size))    #Where we are drawing, color of the rectangle, (initial points [x,y], width, height)

running = True
while running:
    screen.fill(( 0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    draw(screen)
    
                       
    pg.display.flip()                         