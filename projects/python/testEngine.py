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
player = Rectangle(window, Vector(width/2 - playerSize[0]/2, height/2 - playerSize[1]/2), Vector(0, 0), playerSize, "Green")

#ball info
balls = [
]
in_collision = set()
previousVelocities = []


# mainloop of window
while True:
    # input
    for event in pygame.event.get():
        # if quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

        # if keydown
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.velocity += Vector(-playerSpeed,0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(playerSpeed,0)

            elif event.key == pygame.K_SPACE:
                for ball in balls:
                    previousVelocities.append(ball.velocity)
                    ball.velocity = Vector(0,0)
        # if keyup
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.velocity += Vector(playerSpeed,0)

            elif event.key == pygame.K_RIGHT:
                player.velocity += Vector(-playerSpeed,0)

            elif event.key == pygame.K_SPACE:
                i = 0
                for ball in balls:
                    ball.velocity += previousVelocities[i]
                    i+=1
                previousVelocities = []

        # if mouse pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                mouseX,mouseY = event.pos
                vectorNeeded = Vector((mouseX - player.centre.x), (mouseY - player.centre.y))
                size = random.randint(10,50)
                color = []
                for i in range(3):
                    color.append(random.randint(0,255))
                newBall = Ball(window,Vector(mouseX,mouseY), -vectorNeeded, size, (color[0], color[1], color[2]))
                newBall.affectedByGravity = False
                balls.append(newBall)

            if event.button == pygame.BUTTON_RIGHT:
                balls = []


        # if mouse moved
        elif event.type == pygame.MOUSEMOTION:
            pass


    # update
    dt = window.getDt()

       # Update the collision handling
    for b1 in balls:
        #if ball goes offscreen
        if b1.centre.x < 0 or b1.centre.x > width or b1.centre.y < 0 or b1.centre.y > height:
            balls.remove(b1)
        # Check if ball hits the player
        if player.hit(b1):
            b1player = (b1, player) in in_collision
            playerb1 = (player, b1) in in_collision

            if not (b1player or playerb1):
                normal = player.calculate_normal(b1)
                b1.bounce(normal)

            in_collision.add((b1, player))
        else:
            in_collision.discard((b1, player))
            in_collision.discard((player, b1))

        # Check if ball hits another ball
        for b2 in balls:
            if b1.hit(b2):
                if b1 == b2:
                    continue
                b1b2 = (b1, b2) in in_collision
                b2b1 = (b2, b1) in in_collision
                if not (b1b2 or b2b1):
                    collide(b1, b2)
                    in_collision.add((b1, b2))
            else:
                in_collision.discard((b1, b2))
                in_collision.discard((b2, b1))

        # Update ball position
        b1.update(dt)
    player.update(dt)
    # render
    window.clear()
    player.draw()
    for ball in balls:
        ball.draw()
    window.swapBuffers()
