from turtle import Turtle, Screen 
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

    def eat(self):
        self.body.append(Square(self.head.x, self.head.y))
        self.head.x, self.head.y = self.head.x + SIZE * self.nextX, self.head.y + SIZE * self.nextY

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

class Game(object):
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=WIDTH, height=HEIGHT)
        self.screen.tracer(0)
        self.screen.onkeypress(self.snakeDown, "Down")
        self.screen.onkeypress(self.snakeUp, "Up")
        self.screen.onkeypress(self.snakeLeft, "Left")
        self.screen.onkeypress(self.snakeRight, "Right")
        self.screen.listen()

        self.artist = Turtle(visible=False)
        self.artist.up()
        self.artist.speed("slowest")

        self.snake = Snake()
        self.food = Food()
        self.commandPending = False
        

    def snakeUp(self):
        if not self.commandPending: 
            self.commandPending = True
            self.snake.moveUp()
            self.commandPending = False

    def snakeDown(self):
        if not self.commandPending:
            self.commandPending = True
            self.snake.moveDown()
            self.commandPending = False

    def snakeLeft(self):
        if not self.commandPending:
            self.commandPending = True
            self.snake.moveLeft()
            self.commandPending = False

    def snakeRight(self):
        if not self.commandPending:
            self.commandPending = True
            self.snake.moveRight()
            self.commandPending = False

    def nextFrame(self):
        self.artist.clear()

        #print ("x: " + str(self.snake.head.x) + " - y: " + str(self.snake.head.y))
       
        if self.checkFoodCollision():
            self.snake.eat()
            self.food.changeLocation()
        elif self.checkWallCollision() or self.checkSelfCollision():
            self.snake = Snake()
            self.food.changeLocation() 
        else:
            self.snake.moveOneStep(screen)

        self.food.drawSelf(self.artist)
        self.snake.drawSelf(self.artist)
        self.screen.update()
        self.screen.ontimer(lambda: self.nextFrame(), 100)

    def checkFoodCollision(self):
        if (self.snake.head.x, self.snake.head.y) == (self.food.x, self.food.y):
                return True
        return False

    def checkWallCollision(self):
        if (self.snake.head.x >= WIDTH/2 - SIZE or
               self.snake.head.y >= HEIGHT/2 - SIZE or
               self.snake.head.x < -WIDTH/2 + SIZE or
               self.snake.head.y < -HEIGHT/2 + SIZE):
                return True
        return False

    def checkSelfCollision(self):
        for body in self.snake.body:
            if body.x == self.snake.head.x and body.y == self.snake.head.y:
                return True
        return False



# https://www.youtube.com/watch?v=BP7KMlbvtOo

game = Game()

screen = Screen()

screen.ontimer(game.nextFrame(), 100)

screen.mainloop()