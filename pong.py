import random
import time
import os

class Rectangle:
    def __init__(self, xPos, yPos, xSize, ySize):
        self.x_position = xPos
        self.y_position = yPos
        self.x_size = xSize
        self.y_size = ySize
        self.xs = [i for i in range(xPos, xPos + xSize)]
        self.ys = [i for i in range(yPos, yPos + ySize)]
    def updatePos(self):
        self.xs = [i for i in range(self.x_position, self.x_position + self.x_size)]
        self.ys = [i for i in range(self.y_position, self.y_position + self.y_size)]

class Ball(Rectangle):
    def __init__(self, xPos, yPos, direction):
        super().__init__(xPos, yPos, 1, 1)
        self.direction = direction
    def move(self, yMax, leftBorder, rightBorder):
        if self.direction == 1:
            if self.y_position < 2:
                self.direction = 4
                return self.move(yMax, leftBorder, rightBorder)
            if rightBorder.checkForBall(self):
                self.direction = 2
                return self.move(yMax, leftBorder, rightBorder)
            self.y_position = self.y_position - 1
            self.x_position = self.x_position + 1
            
        elif self.direction == 2:
            if self.y_position < 2:
                self.direction = 3
                return self.move(yMax, leftBorder, rightBorder)
            if leftBorder.checkForBall(self):
                self.direction = 1
                return self.move(yMax, leftBorder, rightBorder)
            self.y_position = self.y_position - 1
            self.x_position = self.x_position - 1

        elif self.direction == 3:
            if self.y_position > yMax - 3:
                self.direction = 2
                return self.move(yMax, leftBorder, rightBorder)
            if leftBorder.checkForBall(self):
                self.direction = 4
                return self.move(yMax, leftBorder, rightBorder)
            self.y_position = self.y_position + 1
            self.x_position = self.x_position - 1

        elif self.direction == 4:
            if self.y_position > yMax - 3:
                self.direction = 1
                return self.move(yMax, leftBorder, rightBorder)
            if rightBorder.checkForBall(self):
                self.direction = 3
                return self.move(yMax, leftBorder, rightBorder)
            self.y_position = self.y_position + 1
            self.x_position = self.x_position + 1
        self.updatePos()

class Border(Rectangle):
    def __init__(self, xPos, ySize):
            super().__init__(xPos, 2, 1, ySize)
    
    def checkForBall(self, ball):
        if (ball.x_position - 1 in self.xs and ball.y_position in self.ys) or (ball.x_position + 1 in self.xs and ball.y_position in self.ys):
            return True
        return False

    def play(self, action):
        if action==1:
            self.y_position -= 1
        elif action == 2:
            self.y_position += 1
        self.updatePos()

class Obstacle(Rectangle):
    def __init__(self, xPos, yPos, xLimitLow, xLimitHigh):
            super().__init__(xPos, yPos, 2, 1)
            self.xLimitLow = xLimitLow
            self.xLimitHigh = xLimitHigh
    
    def checkForBall(self, ball):
        return False
        if (ball.y_position - 1 in self.ys and ball.x_position in self.xs) or (ball.y_position + 1 in self.ys and ball.x_position in self.xs):
            return True
        return False

    def play(self):
        x = random.randint(1, 2)
        if x==1 and self.x_position > self.xLimitLow:
            self.x_position -= 1
        elif x == 2 and self.x_position < self.xLimitHigh:
            self.x_position += 1
        self.updatePos()


class Pitch:
    def __init__(self, xSize, ySize, ballXLow, ballXHigh):
        self.xSize = xSize
        self.ySize = ySize
        self.ballxLow = ballXLow
        self.ballxHigh = ballXHigh
        xBall = random.randint(ballXLow, ballXHigh)
        yBall = random.randint(0, ySize - 1)
        direction = random.randint(1, 4)
        self.ball = Ball(xBall, yBall, direction)
        self.leftBorder = Border(0,1)
        self.rightBorder = Border(xSize - 1, ySize - 4)
        self.timer = 0
    
    def updateAll(self):
        self.ball.updatePos()
        self.rightBorder.updatePos()
        self.leftBorder.updatePos()
    
    def reset(self):
        xBall = random.randint(self.ballxLow, self.ballxHigh)
        yBall = random.randint(1, self.ySize-2)
        direction = random.randint(1, 4)
        self.ball = Ball(xBall, yBall, direction)

    def checkLeftLoose(self):
        if self.ball.x_position < 2:
            return True

    def getState(self):
        return((self.ball.x_position, self.ball.y_position), self.leftBorder.y_position)

    def start(self, delay, train=False, action=0):
        while True:
            self.play(delay, train, action)

    def play(self, delay, train=False, action=0):
        self.timer += 1
        if train:
            self.leftBorder.play(action)
            self.ball.move(self.ySize, self.leftBorder, self.rightBorder)
            if self.checkEnd():
                if self.checkLeftLoose():
                    self.reset()
                    self.updateAll()
                    self.reset()
                    return -1
                else:
                    self.reset()
                    return 1
                
            if self.leftBorder.checkForBall(self.ball):
                self.updateAll()
                return 1
            self.updateAll()
            return 0
        else:
            self.leftBorder.play(action)
            time.sleep(delay)
            self.ball.move(self.ySize, self.leftBorder, self.rightBorder)
            if self.checkEnd():
                self.reset()
            self.printPitch()
        self.updateAll()
        return 0

    def checkEnd(self):
        if self.ball.x_position >= self.xSize or self.ball.x_position < 0:
            return True
        return False


    def printPitch(self):
        os.system("cls")
        for j in range(self.ySize):
            for i in range(self.xSize):
                if (i in self.leftBorder.xs) and (j in self.leftBorder.ys):
                    print(" | ",end="")
                elif (i in self.rightBorder.xs) and (j in self.rightBorder.ys):
                    print(" | ",end="")
                elif j == 0 or j == self.ySize - 1:
                    print("___",end="")
                elif (i in self.ball.xs) and (j in self.ball.ys):
                    print(" o ",end="")
                else:
                    print("   ",end="")
            print("\n",end="")

if __name__=="__main__":
    pitch = Pitch(18, 7, 5, 12)
    pitch.start(0.2)
