
import random
from engine import *

pygame.init()

# Main game loop
# Initialize window
useScreen = False
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
width, height = 1000, 1000
window = Window(width, height, 0, "Practice project")
if useScreen:
    window = Window(screenWidth, screenHeight, pygame.FULLSCREEN, "Practice project")
    width, height = screenWidth, screenHeight

# Player info
playerSize = (200, 100)
playerSpeed = 500
player = Rectangle(window, Vector(width / 2, height / 2), Vector(0, 0), playerSize, "Green")

# Ball info
balls = []
in_collision = set()

# Rectangle info
rectangles = [
    Rectangle(window, Vector(0, 0), Vector(0, 0), (width, 20), "Red"),
    Rectangle(window, Vector(width - 20, 0), Vector(0, 0), (20, height), "Red"),
    Rectangle(window, Vector(0, 0), Vector(0, 0), (20, height), "Red"),
    Rectangle(window, Vector(0, height - 20), Vector(0, 0), (width, 20), "Red")
]

# Initialize balls
for _ in range(500):
    color = [random.randint(0, 255) for _ in range(3)]
    balls.append(Ball(window, Vector(random.randint(0, width), random.randint(0, height)),
                      Vector(random.randint(10, 30), random.randint(10, 30)),
                      random.randint(10, 30), color))

pause = False
running = True

key_velocity_map = {
    pygame.K_LEFT: Vector(-playerSpeed, 0),
    pygame.K_RIGHT: Vector(playerSpeed, 0),
}

def update_collision(b1, b2):
    if b1.hit(b2):
        if (b1, b2) not in in_collision and (b2, b1) not in in_collision:
            collide(b1, b2)
            in_collision.add((b1, b2))
    else:
        in_collision.discard((b1, b2))
        in_collision.discard((b2, b1))

while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key in key_velocity_map:
                player.velocity += key_velocity_map[event.key]
            elif event.key == pygame.K_SPACE:
                pause = not pause
        elif event.type == pygame.KEYUP:
            if event.key in key_velocity_map:
                player.velocity -= key_velocity_map[event.key]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if event.button == 1:  # Left mouse button
                vectorNeeded = Vector((mouseX - player.centre.x), (mouseY - player.centre.y))
                size = random.randint(10, 50)
                color = [random.randint(0, 255) for _ in range(3)]
                newBall = Ball(window, Vector(mouseX, mouseY), -vectorNeeded, size, color)
                balls.append(newBall)
            elif event.button == 3:  # Right mouse button
                balls = []


        elif event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            player.pos = Vector(mouseX - player.width / 2, mouseY - player.height / 2)

    # Update
    if not pause:
        dt = window.getDt()
        player.update(dt)
        for ball in balls:
            ball.update(dt)

        # Update the collision handling
        to_remove = []
        boundary = QTRectangle(width / 2, height / 2, width / 2, height / 2)
        quadtree = Quadtree(boundary, 4)

        for b in balls:
            quadtree.insert(Point(b.centre.x, b.centre.y, b))

        for b1 in balls:
            if b1.centre.x < 0 or b1.centre.x > width or b1.centre.y < 0 or b1.centre.y > height:
                to_remove.append(b1)
            if player.hit(b1):
                if (b1, player) not in in_collision and (player, b1) not in in_collision:
                    normal = player.calculate_normal(b1)
                    b1.bounce(normal)
                    b1.push(player.supposedVelocity)
                    player.velocity = Vector(0, 0)
                    in_collision.add((b1, player))
            else:
                in_collision.discard((b1, player))
                in_collision.discard((player, b1))

            # Retrieve nearby objects in the quadtree
            range_rect = QTRectangle(b1.centre.x, b1.centre.y, b1.radius * 2, b1.radius * 2)
            points = quadtree.query(range_rect, [])
            for point in points:
                b2 = point.data
                if b1 != b2:
                    update_collision(b1, b2)

            for rectangle in rectangles:
                if rectangle.hit(b1):
                    if (rectangle, b1) not in in_collision:
                        normal = rectangle.calculate_normal(b1)
                        b1.bounceDF(normal, Vector(0,1))
                        in_collision.add((rectangle, b1))
                else:
                    in_collision.discard((rectangle, b1))

        for b in to_remove:
            balls.remove(b)

    # Render
    window.clear()
    player.draw()
    for ball in balls:
        ball.draw()
    for rectangle in rectangles:
        rectangle.draw()
    window.swapBuffers()

pygame.quit()
