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
player.currentMousePos = Vector(0,0)
player.showDirectionDrag = False

# boundaries
boundaryColor = "Blue"

# map details
map = Map(window,Vector(0, 0), 10000, 10000, "Red", 10)
map.addOutsideBoundaries()

# camera
camera = Camera(player, width, height)


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
                player.velocity += Vector(-playerSpeed, 0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(playerSpeed, 0)

            elif event.key == pygame.K_SPACE:
                pause = True

            elif event.key == pygame.K_UP:
                pass

            elif event.key == pygame.K_DOWN:
                pass


        # if keyup
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.velocity += Vector(playerSpeed, 0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(-playerSpeed, 0)

            elif event.key == pygame.K_SPACE:
                pause = False

        # if mouse pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouseX,mouseY = event.pos
                player.lastClickPos = Vector(mouseX, mouseY)
                player.showDirectionDrag = True

            if event.button == pygame.BUTTON_RIGHT:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                currentX, currentY = event.pos
                accelerationVector = -Vector(currentX - player.lastClickPos.x, currentY - player.lastClickPos.y)
                player.velocity += accelerationVector
                player.showDirectionDrag = False

        # if mouse moved
        elif event.type == pygame.MOUSEMOTION:
            mouseX,mouseY = event.pos
            player.currentMousePos = Vector(mouseX, mouseY)

    # update
    dt = window.getDt()
    if pause == False:

        for boundary in map.boundaries:
            if boundary.hit(player):
                if (boundary, player) not in in_collision:
                    normal = boundary.calculate_normal(player)
                    player.bounce(normal)
                    player.pos = player.lastPos
                in_collision.add((boundary, player))
            else:
                in_collision.discard((boundary, player))

            boundary.update(dt)

        player.update(dt)
        camera.update()

    # render
    window.clear()

    playerPos = camera.apply(player.pos)
    player.pos = playerPos
    player.draw()

    for boundary in map.boundaries:
        boundaryPos = camera.apply(boundary.pos)
        boundary.pos = boundaryPos
        rectangleCentrePoint = (boundary.centre.x, boundary.centre.y)
        rope = Rope(window, player.calculateIntersection(boundary.centre), rectangleCentrePoint, 10)
        rope.draw()
        boundary.draw()

    if player.showDirectionDrag:
        #drawing line from initial click to current mouse position
        startPoint = (player.currentMousePos.x,player.currentMousePos.y)
        endPoint = (player.lastClickPos.x, player.lastClickPos.y)
        pygame.draw.line(window.window, "Green", startPoint, endPoint, 10)
    window.swapBuffers()
pygame.quit()
