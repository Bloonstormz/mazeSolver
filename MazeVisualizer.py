import pygame
from sys import exit
import ctypes
import mazeCreate
import maze as Maze
from enum import Enum
import time

class Timer():
    def __init__(self):
        self.__hour = 0
        self.__min = 0
        self.__sec = 0
        self.__startTime = None

    def start(self):
        if self.__startTime:
            return
        self.__startTime = time.time()
    
    def duration(self):
        temp = time.time() - self.__startTime
        self.__sec = str(round(temp % 60, 2))
        self.__min = str(int((temp//60)%60))
        self.__hour = int(temp//3600)

        if len(self.__sec.split(".")[0]) == 1:
            self.__sec = "0" + self.__sec
        if len(self.__min) == 1:
            self.__min = "0" + self.__min
    
    def __str__(self) -> str:
        return f"{self.__hour}:{self.__min}:{self.__sec}"

class ADTEnum(Enum):
    QUEUE = 0
    STACK = 1
    MINHEAP = 2

class ADT():
    def __init__(self, val, type : ADTEnum):
        self.vals = [val]
        self.__length = 1
        self.type = type

    def add(self, val, key=lambda x : x):
        self.__length += 1
        match self.type.name:
            case "QUEUE":
                self.vals.append(val)
            case "STACK":
                self.vals.append(val)
            case "MINHEAP":
                self.vals.append(val)
                curPos = self.__length - 1
                item = self.vals[curPos] #store item to move
                while curPos > 0:
                    parentPos = (curPos - 1) >> 1
                    parentItem = self.vals[parentPos]
                    if key(item) < key(parentItem):
                        self.vals[curPos] = parentItem
                        curPos = parentPos
                        continue
                    break
                self.vals[curPos] = item #reinsert item
            case _:
                raise ValueError(f"Unexpected type provided: {self.type}")

    def remove(self):
        self.__length -= 1
        return self.vals.pop(0) if self.type.name == "QUEUE" or self.type.name == "ASTAR" else self.vals.pop()
    
    def peek(self):
        return self.vals[0] if self.type.name == "QUEUE" or self.type.name == "ASTAR" else self.vals[-1]
    
    def length(self):
        return self.__length

def roundDown(x, n):
    return x if x%(10**n) == 0 else x - x%(10**n)

def calcPixel(mazeLength, mazeWidth):
    user32 = ctypes.windll.user32
    pxSize = min(roundDown(user32.GetSystemMetrics(0),2)//mazeWidth, roundDown(user32.GetSystemMetrics(1),2)//mazeLength)
    if pxSize < 1:
        raise ValueError("Maze Dimensions too large! Unable to render pixel")
    border = True if pxSize > 5 else False

    return pxSize, pxSize*mazeWidth, pxSize*mazeLength, border

#Draw an individual cell in a maze
def drawCell(screen, pxSize, colour, borderColour, xCoord, yCoord, border=False):
    a = pygame.draw.rect(screen, colour, [xCoord*pxSize, yCoord*pxSize, pxSize, pxSize])
    if border:
        b = pygame.draw.rect(screen, borderColour, [xCoord*pxSize, yCoord*pxSize, pxSize, pxSize], 1)
    return [a,b] if border else [a]

#Only draws the path taken for the search (saves cpu)
def drawPath(screen, pxSize, curLoc, path, curColour=(0,0,255), pathColour=(0,255,0), bgColour=(0,0,0), border=True):
    rectList = []
    for yCoord, xCoord in path:
        rectList.extend(drawCell(screen, pxSize, pathColour, bgColour, xCoord, yCoord, border))
    rectList.extend(drawCell(screen, pxSize, curColour, bgColour, curLoc[1], curLoc[0], border))
    pygame.display.update(rectList)

def clearPath(screen, pxSize, path):
    rectList = []
    for yCoord, xCoord in path:
        rectList.extend(drawCell(screen, pxSize, (0,0,0), (0,0,0), xCoord, yCoord, False))
    pygame.display.update(rectList)

#Draws the entire maze
def renderMaze(screen : pygame.Surface, maze, pxSize, curLoc=None, path=None, wallColour = (255,255,255), bgColour = (0,0,0), startEndColour=(255,0,0), curColour=(0,0,255), pathColour=(0,255,0), border=True):
    start, end = Maze.findStartEnd(maze)
    screen.fill(bgColour)
    for yCoord, row in enumerate(maze):
        for xCoord, val in enumerate(row):
            if (yCoord, xCoord) == start or (yCoord, xCoord) == end:
                drawColour = startEndColour
            elif val == 1:
                drawColour = wallColour
            else:
                continue
            drawCell(screen, pxSize, drawColour, bgColour, xCoord, yCoord, border)
    pygame.display.update()

#Solving Algorithm
def mazeSolver(maze, method : ADTEnum, screen, cellBorder, cellSize):
    global speed
    fpsTime, keyTime = 0,0

    temp = Maze.findStartEnd(maze)
    start = temp[0]
    end = temp[1]

    path = {start : [start]} # Dictionary to store path taken to all points
    nextNode = ADT(start, method) # Abstract Date Type 

    while nextNode.length() > 0:
        curLocation = nextNode.remove()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_EQUALS] and keyTime > 100:
            speed += 1
            keyTime = 0
        elif key[pygame.K_MINUS] and keyTime > 100:
            if speed > 0:
                speed -= 1
            keyTime = 0

        if fpsTime > 1000:
            print(f"Max FPS: {speed}     FPS: {clock.get_fps()}", end="\r")
            fpsTime = 0

        timer.duration()
        pygame.display.set_caption(f"Solving Maze... Time taken: {timer}")

        keyTime += clock.get_time()
        fpsTime += clock.get_time()

        drawPath(screen, cellSize, curLocation, path[curLocation], border=cellBorder)
        clock.tick(speed)

        for x in Maze.findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            nextNode.add(x)
            path[x] = path[curLocation] + [x]

        if not(Maze.isConnected(nextNode.peek(), curLocation)):
            clearPath(screen, cellSize, path[curLocation])
        
    raise RuntimeError("Could not reach END")

def mazeSolving(maze, type : str, screen : pygame.Surface, cellBorder : bool, cellSize : int):
    match type.lower():
        case "bfs":
            method = ADTEnum.QUEUE
        case "dfs":
            method = ADTEnum.STACK
        case "astar":
            method = ADTEnum.MINHEAP
        case _:
            raise ValueError("Unknown/Unimplemented Solving Method")
    mazeSolver(maze, method, screen, cellBorder, cellSize)

#Main Code
if __name__ == "__main__":
    mazeLength = int(input("Enter length of maze: "))
    mazeWidth = int(input("Enter width of maze: "))

    try:
        pxSize, screenwidth, screenheight, border = calcPixel(mazeLength, mazeWidth)
    except ValueError:
        print("Unable to render maze. Dimensions too large")
        exit()

    maze = mazeCreate.createMaze(mazeLength, mazeWidth)
    temp = Maze.findStartEnd(maze)

    screen = pygame.display.set_mode([screenwidth,screenheight])
    pygame.display.set_caption("Solving Maze... Time taken: 0:00:00.0")
    clock = pygame.time.Clock()
    renderMaze(screen, maze, pxSize, border=border)
    speed = 60

    timer = Timer()
    timer.start()
    foo = mazeSolving
    foo(maze, "dfs", screen, border, pxSize)
    timer.duration()
    pygame.display.set_caption(f"Solved! Time taken: {timer}")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        clock.tick(20)