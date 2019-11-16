from turtle import Turtle 
import random
import time

SIZE = 20
WIDTH = 400
HEIGHT = 400

class Square:
    def __init__(self, x, y, color = "black"):
        self.x = x
        self.y = y
        self.color = color

    def drawSelf(self, turtle):
        turtle.goto(self.x - SIZE // 2 - 1, self.y - SIZE // 2 - 1)

        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(SIZE - SIZE // 10)
            turtle.left(90)
            turtle.color(self.color)
        turtle.end_fill()

class Food(Square):
    def __init__(self, x = 0, y = 0, color = "red"):
        self.x = x
        self.y = y
        self.color = color
        self.changeLocation()

    def changeLocation(self):
        self.x = random.randrange(-WIDTH/2 + SIZE, WIDTH/2 - SIZE, SIZE)
        self.y = random.randrange(-HEIGHT/2 + SIZE, HEIGHT/2 - SIZE, SIZE)

class Snake:
    def __init__(self):
        self.head = Square(SIZE, 0)
        self.body = []
        self.nextX = 0
        self.nextY = 0
        self.score = 0

    def eat(self):
        self.body.append(Square(self.head.x, self.head.y))
        self.head.x, self.head.y = self.head.x + SIZE * self.nextX, self.head.y + SIZE * self.nextY
        self.score += 1

    def moveOneStep(self, screen):
        self.body.append(Square(self.head.x, self.head.y))
        del self.body[0]
        self.head.x, self.head.y = self.head.x + SIZE * self.nextX, self.head.y + SIZE * self.nextY

    def moveUp(self):
        if (self.nextX, self.nextY) != (0, -1):
            self.nextX, self.nextY = 0, 1

    def moveLeft(self):
        if (self.nextX, self.nextY) != (1, 0):
            self.nextX, self.nextY = -1, 0

    def moveRight(self):
        if (self.nextX, self.nextY) != (-1, 0):
            self.nextX, self.nextY = 1, 0

    def moveDown(self):
        if (self.nextX, self.nextY) != (0, 1):
            self.nextX, self.nextY = 0, -1

    def drawSelf(self, turtle):
        self.head.drawSelf(turtle)
        for segment in self.body:
            segment.drawSelf(turtle)

    def checkFoodCollision(self, food: Food):
        if (self.head.x, self.head.y) == (food.x, food.y):
                return True
        return False

    def checkWallCollision(self):
        if (self.head.x >= WIDTH/2 - SIZE or
               self.head.y >= HEIGHT/2 - SIZE or
               self.head.x < -WIDTH/2 + SIZE or
               self.head.y < -HEIGHT/2 + SIZE):
                return True
        return False

    def checkSelfCollision(self):
        for body in self.body:
            if body.x == self.head.x and body.y == self.head.y:
                return True
        return False
