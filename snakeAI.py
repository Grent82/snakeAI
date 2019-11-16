from turtle import Turtle, Screen 
from snake import Snake, Food
import time

WIDTH = 400
HEIGHT = 400

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

        self.pen = Turtle()
        self.pen.penup()
        self.pen.speed(0)
        self.pen.color("black")
        self.pen.hideturtle()
        self.pen.goto(0, HEIGHT/2 - 40)

        self.snake = Snake()
        self.food = Food()
        self.commandPending = False

        self.writeScore(self.snake.score)
        

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
       
        if self.snake.checkFoodCollision(self.food):
            self.snake.eat()
            self.food.changeLocation()
            self.writeScore(self.snake.score)
        elif self.snake.checkWallCollision() or self.snake.checkSelfCollision():
            self.snake = Snake()
            self.food.changeLocation() 
            self.writeScore(self.snake.score)
        else:
            self.snake.moveOneStep(screen)

        self.food.drawSelf(self.artist)
        self.snake.drawSelf(self.artist)
        self.screen.update()
        self.screen.ontimer(lambda: self.nextFrame(), 100)

    def writeScore(self, score: int):
        self.pen.clear()
        self.pen.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))


# https://www.youtube.com/watch?v=BP7KMlbvtOo

game = Game()

screen = Screen()

screen.ontimer(game.nextFrame(), 100)

screen.mainloop()