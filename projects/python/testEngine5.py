from engine import *
from vector import *
import random

pygame.init()
#window info
useScreen = True
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
width = 1000
height = 1000
window = Window(width,height,0, "Practice project")
if useScreen:
    window = Window(screenWidth, screenHeight, pygame.FULLSCREEN, "Practice project")
    width = screenWidth
    height = screenHeight

#player info
playerSize = (200, 100)
playerSpeed = 500
player = Ball(window, Vector(width/2 - playerSize[0]/2, height/2 - playerSize[1]/2), Vector(0, 0), 20, "Red")

# boundaries
rectangles = [
    Rectangle(window, Vector(width/2 - 200, height - 20), Vector(0,0), (200,20),"Blue")
]

pause = False
running = True
# mainloop of window
while running:
    # input
    for event in pygame.event.get():
        # if quitting
        if event.type == pygame.QUIT:
            running = False

        # if keydown
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_LEFT:
                player.velocity += Vector(-playerSpeed,0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(playerSpeed,0)

            elif event.key == pygame.K_SPACE:
                pause = True

            elif event.key == pygame.K_UP:
                pass

            elif event.key == pygame.K_DOWN:
                pass


        # if keyup
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.velocity += Vector(playerSpeed,0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(-playerSpeed,0)

            elif event.key == pygame.K_SPACE:
                pause = False

        # if mouse pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pass

            if event.button == pygame.BUTTON_RIGHT:
                pass


        # if mouse moved
        elif event.type == pygame.MOUSEMOTION:
            pass

    # update
    dt = window.getDt()
    if pause == False:

        for rectangle in rectangles:
            if rectangle.hit(player):
                player.bounce(rectangle.calculate_normal(player))

            rectangle.update(dt)

        player.update(dt)


    # render
    window.clear()
    player.draw()
    for rectangle in rectangles:
        rectangle.draw()
    window.swapBuffers()
pygame.quit()
