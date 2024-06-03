from engine import *
from vector import *
import random

pygame.init()
#window info
useScreen = False
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
width = 1000
height = 1000
window = Window(width,height,0, "Practice project")
if useScreen:
    window = Window(screenWidth, screenHeight, pygame.FULLSCREEN, "Practice project")
    width = screenWidth
    height = screenHeight

# Ball info
radius = 200
mainBall = Ball(window,Vector(width/2, height/2 ), Vector(0, 0), radius, "Blue")
mainBall.affectedByGravity = False
balls = [

]
in_collision = set()
previousVelocities = []

# Mainloop of window
while True:
    # Input
    for event in pygame.event.get():
        # If quitting
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

        # If keydown
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for ball in balls:
                    previousVelocities.append(ball.velocity)
                    ball.velocity = Vector(0, 0)
                    ball.affectedByGravity = False

        # If keyup
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                i = 0
                for ball in balls:
                    ball.velocity += previousVelocities[i]
                    i += 1
                    ball.affectedByGravity = True
                previousVelocities = []

        # If left-click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            mouseX,mouseY = event.pos
            vectorNeeded = Vector((mouseX - width/2), (mouseY - height/2))
            size = random.randint(10,50)
            color = []
            for i in range(3):
                color.append(random.randint(0,255))
            newBall = Ball(window,Vector(mouseX,mouseY), -vectorNeeded, size, (color[0], color[1], color[2]))
            balls.append(newBall)

        # If right-click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            balls = []

    # Update
    dt = window.getDt()

    for ball in balls:
        #if ball goes offscreen
        if ball.centre.x < 0 or ball.centre.x > width or ball.centre.y < 0 or ball.centre.y > height:
            balls.remove(ball)
        ball.update(dt)

     # handling for balls hitting objects
    for b1 in balls:
        #if a ball hits inside of main ball

        if mainBall.hitInside(b1):
            mainBallb1 = (mainBall, b1) in in_collision
            if not mainBallb1:
                dirToCenter = Vector(b1.pos.x - mainBall.pos.x, b1.pos.y - mainBall.pos.y)
                #magnitude of objects current velocity
                magnitude = math.sqrt(b1.velocity.x * b1.velocity.x + b1.velocity.y * b1.velocity.y)
                #angle of the object to the collision point
                angleToCollisionPoint = math.atan2(-dirToCenter.y,dirToCenter.x)
                oldAngle = math.atan2(-b1.velocity.y, b1.velocity.x)
                newAngle = 2 * angleToCollisionPoint - oldAngle
                b1.velocity = Vector(-magnitude * math.cos(newAngle), magnitude * math.sin(newAngle))
            in_collision.add((mainBall,b1))
        else:
            in_collision.discard((mainBall,b1))

        #if a ball hits another ball
        for b2 in balls:
            if b1.hit(b2):
                if b1 == b2:
                    continue
                b1b2 = (b1, b2) in in_collision
                b2b1 = (b2, b1) in in_collision
                if not (b1b2 or b2b1):
                    collide(b1,b2)
                    mainBall.velocity = Vector(0,0)
                in_collision.add((b1,b2))
            else:
                in_collision.discard((b1,b2))
                in_collision.discard((b2,b1))

    mainBall.update(dt)
    # Render
    window.clear()
    mainBall.draw()
    for ball in balls:
        ball.draw()
    window.swapBuffers()
