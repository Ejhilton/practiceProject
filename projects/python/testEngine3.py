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
player = Rectangle(window, Vector(width/2, height/2), Vector(0, 0), playerSize, "Green")

#ball info
balls = [
]
in_collision = set()
previousVelocities = []

# rectangle info
rectangles = [
    Rectangle(window,Vector(0,0), Vector(0,0), (width,20), "Red"),
    Rectangle(window,Vector(width - 20,0), Vector(0,0), (20,height), "Red"),
    Rectangle(window,Vector(0,0), Vector(0,0), (20,height), "Red"),
    Rectangle(window,Vector(0,height - 20), Vector(0,0), (width,20), "Red")
]

#player controls
increaseSpeed = 10
for i in range(0,10):
    color = []
    for i in range(3):
        color.append(random.randint(0,255))
    balls.append(Ball(window,Vector(random.randint(0,width),random.randint(0,height)), Vector(random.randint(10,30),random.randint(10,30)), random.randint(10,30), color))

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
                vectorNeeded = Vector((mouseX - player.centre.x), (mouseY - player.centre.y))
                size = random.randint(10,50)
                color = []
                for i in range(3):
                    color.append(random.randint(0,255))
                newBall = Ball(window,Vector(mouseX,mouseY), -vectorNeeded, size, (color[0], color[1], color[2]))
                balls.append(newBall)

            if event.button == pygame.BUTTON_RIGHT:
                balls = []


        # if mouse moved
        elif event.type == pygame.MOUSEMOTION:
            mouseX,mouseY = event.pos
            player.pos = Vector(mouseX - player.width/2,mouseY - player.height/2)

    # update
    dt = window.getDt()
    if pause == False:
        player.update(dt)
        for ball in balls:
            ball.update(dt)

        for rectangle in rectangles:
            rectangle.update(dt)


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
                    b1.push(player.supposedVelocity)
                    player.velocity = Vector(0, 0)

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

            #check if ball hits a boundary
            for rectangle in rectangles:
                if rectangle.hit(b1):
                    rectangleb1 = (rectangle, b1) in in_collision
                    if not (rectangleb1):
                        normal = rectangle.calculate_normal(b1)
                        b1.bounce(normal)
                        rectangle.velocity = Vector(0,0)
                    in_collision.add((rectangle, b1))
                else:
                    in_collision.discard((rectangle, b1))
            # Update ball position




    # render
    window.clear()
    player.draw()
    for ball in balls:
        ball.draw()
    for rectangle in rectangles:
        rectangle.draw()
    window.swapBuffers()
pygame.quit()
