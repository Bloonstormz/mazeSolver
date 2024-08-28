import pygame
from sys import exit
import ctypes
import MazeCreate
import Maze
from enum import Enum

class ADTEnum(Enum):
    QUEUE = 0
    STACK = 1
    MINHEAP = 2

class ADT():
    def __init__(self, val, type : ADTEnum):
        self.vals = [val]
        self.type = type

    def add(self, val, key=lambda x : x):
        match self.type.name:
            case "QUEUE":
                self.vals.append(val)
            case "DFS":
                self.vals.append(val)
            case "ASTAR":
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
        return self.vals.pop(0) if self.type.name == "QUEUE" or self.type.name == "ASTAR" else self.vals.pop()
    
    def peek(self):
        return self.vals[0] if self.type.name == "QUEUE" or self.type.name == "ASTAR" else self.vals[-1]
    
    def length(self):
        return self.vals.__len__()

def roundDown(x, n):
    return x if x%(10**n) == 0 else x - x%(10**n)

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

    maze = MazeCreate.createMaze(mazeLength, mazeWidth)

    temp = Maze.findStartEnd(maze)
    user32 = ctypes.windll.user32
    pxSize = min(roundDown(user32.GetSystemMetrics(0),2)//mazeWidth, roundDown(user32.GetSystemMetrics(1),2)//mazeLength)
    border = True if pxSize > 5 else False

    screenwidth, screenheight = pxSize*mazeWidth, pxSize*mazeLength
    screen = pygame.display.set_mode([screenwidth,screenheight])
    pygame.display.set_caption("Solving Maze...")
    clock = pygame.time.Clock()
    renderMaze(screen, maze, pxSize, border=border)
    speed = 60

    foo = mazeSolving
    foo(maze, "BFS", screen, border, pxSize)
    pygame.display.set_caption("Solved!")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()