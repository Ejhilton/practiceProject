import pygame
import time
from vector import *

class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data


class QTRectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        return (self.x - self.w <= point.x < self.x + self.w and
                self.y - self.h <= point.y < self.y + self.h)

    def intersects(self, other):
        return not (other.x - other.w > self.x + self.w or
                    other.x + other.w < self.x - self.w or
                    other.y - other.h > self.y + self.h or
                    other.y + other.h < self.y - self.h)


class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        self.northeast = Quadtree(QTRectangle(x + w, y - h, w, h), self.capacity)
        self.northwest = Quadtree(QTRectangle(x - w, y - h, w, h), self.capacity)
        self.southeast = Quadtree(QTRectangle(x + w, y + h, w, h), self.capacity)
        self.southwest = Quadtree(QTRectangle(x - w, y + h, w, h), self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True

        return False

    def query(self, other, found):
        if not self.boundary.intersects(other):
            return found

        for p in self.points:
            if other.contains(p):
                found.append(p)

        if self.divided:
            self.northwest.query(other, found)
            self.northeast.query(other, found)
            self.southwest.query(other, found)
            self.southeast.query(other, found)

        return found

class Window:
    def __init__(self, width, height, fullscreen, title):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height), fullscreen)
        pygame.display.set_caption(title)
        self.previousTime = time.time()

    def swapBuffers(self):
        pygame.display.flip()

    def clear(self):
        self.window.fill((0, 0, 0))

    def getDt(self):
        currentTime = time.time()
        dt = currentTime - self.previousTime
        self.previousTime = currentTime
        return dt

class Rectangle:
    def __init__(self,window, pos, velocity,size, color):
        self.window = window
        self.windowSurface = window.window
        self.pos = pos
        self.velocity = velocity
        self.supposedVelocity = Vector(0,0)
        self.width, self.height = size
        self.color = color
        self.centre = Vector((self.pos.x + (self.width/2)), (self.pos.y + (self.height/2)))
        self.lastPos = Vector(0,0)
        self.lastTime = time.time()
        self.dampeningFactor = Vector(0,20)

    def update(self,dt):
        self.pos += self.velocity * dt
        self.centre = Vector((self.pos.x + self.width/2), (self.pos.y + self.height/2))
        self.prevPos = self.pos
        self.supposedVelocity = self.getMouseVelocity(self.pos) / 10

    def draw(self):
        pygame.draw.rect(self.windowSurface, self.color, (self.pos.x,self.pos.y, self.width, self.height))

    def hit(self, other):
         # Calculate the closest point on the rectangle to the circle's center
        closest_x = max(self.pos.x, min(other.pos.x, self.pos.x + self.width))
        closest_y = max(self.pos.y, min(other.pos.y, self.pos.y + self.height))

        # Calculate the distance between the circle's center and the closest point
        distance_x = other.pos.x - closest_x
        distance_y = other.pos.y - closest_y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        # Check if the distance is less than the circle's radius
        return distance < other.radius

    def calculate_normal(self, other):
        # Calculate the closest point on the rectangle to the circle's center
        closest_x = max(self.pos.x, min(other.pos.x, self.pos.x + self.width))
        closest_y = max(self.pos.y, min(other.pos.y, self.pos.y + self.height))

        # Calculate the distance between the circle's center and the closest point
        distance_x = other.pos.x - closest_x
        distance_y = other.pos.y - closest_y

        # Determine which side of the rectangle the circle hit
        if abs(distance_x) > abs(distance_y):
            # The circle hit the left or right side of the rectangle
            if distance_x > 0:
                return Vector(1, 0)  # Right side
            else:
                return Vector(-1, 0)  # Left side
        else:
            # The circle hit the top or bottom side of the rectangle
            if distance_y > 0:
                return Vector(0, 1)  # Bottom side
            else:
                return Vector(0, -1)  # Top side

    def getMouseVelocity(self, currentMousePos):
        currentTime = time.time()
        timeElapsed = currentTime - self.lastTime
        distanceMoved = currentMousePos - self.lastPos
        self.lastTime = currentTime
        self.lastPos = currentMousePos

        if timeElapsed > 0:
            return distanceMoved / timeElapsed
        return Vector(0,0)



class Ball:
    def __init__(self,window, pos, velocity, radius, color):
        self.pos = pos
        self.window = window
        self.windowSurface = window.window
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.centre = Vector((self.pos.x + self.radius), (self.pos.y + self.radius))
        self.lastPos = self.pos
        self.gravity = Vector(0,0.9)
        self.affectedByGravity = True

    def update(self,dt):
        if self.affectedByGravity:
            self.velocity += self.gravity

        self.pos += self.velocity * dt
        self.centre = Vector((self.pos.x + self.radius), (self.pos.y + self.radius))
        self.lastPos = self.pos

    def draw(self):
        pygame.draw.circle(self.windowSurface, self.color, (self.pos.x, self.pos.y), self.radius)

    def hit(self, ball):
        distance = ball.centre.copy().subtract(self.centre).length()
        return distance <= (self.radius + ball.radius)

    def hitInside(self,ball):
        distance = ball.pos.copy().subtract(self.pos).length()
        return distance >= self.radius - ball.radius

    def bounce(self, normal):
        self.velocity.reflect(normal)

    def bounceDF(self, normal,dampeningFactor):
        self.velocity -= dampeningFactor
        self.velocity.reflect(normal)

    def push(self,supposedVelocity):
        self.velocity += supposedVelocity

    def calculateIntersection(self, point):
        vectorToPoint = Vector(point.x - self.pos.x, point.y - self.pos.y)
        distance = math.sqrt(vectorToPoint.x **2 + vectorToPoint.y **2)
        normalisedVector = Vector(vectorToPoint.x / distance, vectorToPoint.y / distance)

        intersectionPos = (self.pos.x + normalisedVector.x * self.radius, self.pos.y + normalisedVector.y * self.radius)

        return intersectionPos

class Rope:
    def __init__(self, window, start, end, width):
        self.start = start
        self.end = end
        self.width = width
        self.window = window
        self.windowSurface = window.window
    def draw(self):
        pygame.draw.line(self.windowSurface, "Green", self.start, self.end, 10)


def collide(self,other):
    normal = self.pos.copy().subtract(other.pos).normalize()

    v1_par = self.velocity.get_proj(normal)
    v1_perp = self.velocity.copy().subtract(v1_par)

    v2_par = other.velocity.get_proj(normal)
    v2_perp = other.velocity.copy().subtract(v2_par)

    self.velocity = v2_par + v1_perp
    other.velocity = v1_par + v2_perp


def calculateNormal(self,other):
    return self.pos.copy().subtract(other.pos).normalize()

