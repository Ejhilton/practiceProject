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
player = Ball(window, Vector(width/2, height/2), Vector(0, 0), 20, "Red")
player.affectedByGravity = True
player.lastClickPos = Vector(0,0)

# boundaries
rectangleSize = (200,20)
rectangles = [
    Rectangle(window, Vector(width/2 - rectangleSize[0]/2, height - rectangleSize[1]), Vector(0,0), rectangleSize,"Blue"),
    Rectangle(window, Vector(width/2 - rectangleSize[0]/2, 0), Vector(0,0), rectangleSize,"Blue")
]

#boundary info
boundaries = [
    Rectangle(window, Vector(0, 0), Vector(0, 0), (width, 20), "Red"),
    Rectangle(window, Vector(width - 20, 0), Vector(0, 0), (20, height), "Red"),
    Rectangle(window, Vector(0, 0), Vector(0, 0), (20, height), "Red"),
    Rectangle(window, Vector(0, height - 20), Vector(0, 0), (width, 20), "Red")
]


#collision tracking
in_collision = set()

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
                mouseX,mouseY = event.pos
                player.lastClickPos = Vector(mouseX, mouseY)

            if event.button == pygame.BUTTON_RIGHT:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                currentX, currentY = event.pos
                accelerationVector = -Vector(currentX - player.lastClickPos.x, currentY - player.lastClickPos.y)
                player.velocity += accelerationVector


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

        for boundary in boundaries:
                if boundary.hit(player):
                    if (boundary, player) not in in_collision:
                        normal = boundary.calculate_normal(player)
                        player.bounce(normal)
                    in_collision.add((boundary, player))
                else:
                    in_collision.discard((boundary, player))

                boundary.update(dt)

        player.update(dt)


    # render
    window.clear()
    player.draw()
    for rectangle in rectangles:
        rectangleCentrePoint = (rectangle.centre.x, rectangle.centre.y)
        rope = Rope(window, player.calculateIntersection(rectangle.centre), rectangleCentrePoint, 10)
        rope.draw()
        rectangle.draw()

    for boundary in boundaries:
        boundary.draw()

    window.swapBuffers()
pygame.quit()
