import pygame as pg    #Just declaring that we will use pg. instead of pygame. to save time 


#Defining screen size
WIDTH, HEIGHT = 800,600


#Initializing pygame
pg.init()


#Initializing screen
screen = pg.display.set_mode((WIDTH,HEIGHT))  #Remember its a tuple inside a bracket, useful for multiple windows (maybe)


#Game loop   <- Heart of the program
running = True
while running:
    for event in pg.event.get():              #Checks all possible events sent out by the user; Event is basically an action the user can perform
        if event.type == pg.QUIT:             #pg.QUIT is equvalent to pressing the X icon on the top right or alt + f4 and event.type just defines the type of event
            running = False
    
    
    screen.fill(( 0, 0, 0))                   #Fills the entire screen with a certain color of RGB 0 being minimum (black) and 255 being max (White if all) *Also a tuple

    
    pg.display.flip()                         #Flips between the two frame buffers [As we studied the frame buffer contains the information on the next frame]