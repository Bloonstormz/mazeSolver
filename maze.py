from pygame.sprite import AbstractGroup
import mazeCreate
import statistics
import pygame
from sys import exit
import ctypes

#Sample Mazes
# maze = [
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     ['S', 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
#     [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
#     [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'E'],
#     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]
# maze = [
#     [1, 'S', 1, 1, 1],
#     [1, 0, 0, 0, 1],
#     [1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 1],
#     [1, 1, 1, 'E', 1]
# ]

def roundDown(x, n):
    return x if x%(10**n) == 0 else x - x%(10**n)

def printTable(array):
    for x in array:
        print(x)

def isConnected(loc1, loc2):
    if abs(loc1[0] - loc2[0]) > 1 or abs(loc1[1] - loc2[1]) > 1:
        return False
    if (abs(loc1[0] - loc2[0])) ^ (abs(loc1[1] - loc2[1])):
        return True
    return False


def pathVerify(maze, startLocation, path):
    if startLocation != path[0]:
        print(startLocation)
        print(path)
        print("Did not start at the right place")
        return False
    cur = startLocation
    for x in range(1,len(path)):
        if not isConnected(cur, path[x]):
            print(path)
            print(cur, path[x])
            print("Path provided is not connected")
            return False
        if path[x][0] < 0 or path[x][0] > len(maze) - 1 or path[x][1] < 0 or path[x][1] > len(maze[path[x][0]]) - 1:
            print("Went out of bounds")
            return False
        if maze[path[x][0]][path[x][1]] == 1:
            print(path[x])
            print("Ran into wall")
            return False
        cur = path[x]
        
    if maze[path[x][0]][path[x][1]] == "E":
        return True
    else:
        print(path[x])
        print("Did not finish at end")
        return False

def findStartEnd(maze):
    sLocation = None
    eLocation = None
    for yIndex, y in enumerate(maze):
        for xIndex, x in enumerate(y):
            if maze[yIndex][xIndex] == 'S':
                sLocation = (yIndex, xIndex)
            elif maze[yIndex][xIndex] == 'E':
                eLocation = (yIndex, xIndex)
            if sLocation is not None and eLocation is not None:
                break
    return (sLocation, eLocation)

def findUnsearchedNodes(maze, location, visited = {}):
    leftX = location[1] - 1
    downY = location[0] + 1
    rightX = location[1] + 1
    upY = location[0] - 1
    neighbours = []
    
    if (downY, location[1]) not in visited and downY <= len(maze) - 1 and maze[downY][location[1]] != 1:
        neighbours.append((downY, location[1]))
    if (upY, location[1]) not in visited and upY >= 0 and maze[upY][location[1]] != 1:
        neighbours.append((upY, location[1]))
    if (location[0], leftX) not in visited and leftX >= 0 and maze[location[0]][leftX] != 1:
        neighbours.append((location[0], leftX))
    if (location[0], rightX) not in visited and rightX <= len(maze[location[0]]) - 1 and maze[location[0]][rightX] != 1:
        neighbours.append((location[0], rightX))
    return neighbours

def directionTaken(srcLocation, dstLocation):
    if dstLocation[0] > srcLocation[0]:
        return ["Down"]
    elif dstLocation[0] < srcLocation[0]:
        return ["Up"]
    elif dstLocation[1] < srcLocation[1]:
        return ["Left"]
    elif dstLocation[1] > srcLocation[1]:
        return ["Right"]
    else:
        return "Error? Same"

def mazeSolverBFS(maze, start = None, end = None, visualize = False):
    global iterations
    if visualize:
        global pxSize, speed, border
        fpsTime, keyTime = 0,0
    if start is None or end is None:
        temp = findStartEnd(maze)
        start = temp[0]
        end = temp[1]

    iterations = 0
    # Maze solving
    path = {start : [start]} # Dictionary to store path taken to all points
    searchQueue = [start] # Queue containing elements to search

    while len(searchQueue) > 0:
        iterations += 1
        curLocation = searchQueue.pop(0)

        if visualize:
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

            drawPath(pxSize, curLocation, path[curLocation])
            clock.tick(speed)
            
        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            searchQueue.append(x)
            path[x] = path[curLocation] + [x]

        if not isConnected(searchQueue[0], curLocation) and visualize:
            clearPath(pxSize, path[curLocation])
        
    raise RuntimeError("Could not reach END")

def mazeSolverDFS(maze, start = None, end = None, visualize=False):
    global iterations
    if visualize:
        global pxSize, speed, border
        fpsTime, keyTime = 0,0
    if start is None or end is None:
        temp = findStartEnd(maze)
        start = temp[0]
        end = temp[1]

    iterations = 0
    # Maze solving
    path = {start : [start]} # Dictionary to store path taken to all points
    searchStack = [start] # Stack containing elements to search

    while len(searchStack) > 0:
        iterations += 1
        curLocation = searchStack.pop()

        if visualize:
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

            drawPath(pxSize, curLocation, path[curLocation])
            clock.tick(speed)

        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            searchStack.append(x)
            path[x] = path[curLocation] + [x]
        
        if not isConnected(searchStack[-1], curLocation) and visualize:
            clearPath(pxSize, path[curLocation])
        
    raise RuntimeError("Could not reach END")

#Don't mind the long function name
#IDK how to make pygame work with recursive functions. Maybe I can do something but it'll look janky
def mazeSolverDFSRecurison(maze, start = None, end = None):
    if start is None or end is None:
        temp = findStartEnd(maze)
        start = temp[0]
        end = temp[1]
    searchedNodes = {start: True} #Using a dictionary for faster searching

    def helper(path, curLocation):
        nonlocal maze, start, end, searchedNodes
        for x in findUnsearchedNodes(maze, curLocation, searchedNodes):
            if x == end:
                return path + [end]
            searchedNodes[x] = True
            if temp := helper(path + [x], x):
                return temp

    return helper([start], start)

def generateHeuristic(maze, end = None):
    if end is None:
        temp = findStartEnd(maze)
        end = temp[1]

    heuristicTable = [[(abs(end[0] - y) + abs(end[1] - x)) for x in range(len(maze[0]))] for y in range(len(maze))]
    return heuristicTable

def addToHeap(array, child, table):
    flag = False
    if child % 2 == 0:
        parent = int((child - 2) / 2)
    else:
        parent = int((child - 1) / 2)
    
    if table[array[child][0]][array[child][1]] < table[array[parent][0]][array[parent][1]]:
        flag = True
    
    if flag:
        array[child], array[parent] = array[parent], array[child]
        addToHeap(array, parent, table)

def mazeSolverAStar(maze, start = None, end = None, visualize=False):
    global iterations
    if visualize:
        global pxSize, speed, border
        keyTime, fpsTime = 0,0
    if start is None or end is None:
        temp = findStartEnd(maze)
        start = temp[0]
        end = temp[1]

    iterations = 0
    # Maze solving
    path = {start : [start]} # Dictionary to store path taken to all points
    heap = [start] # Queue containing elements to search
    heuristicTable = generateHeuristic(maze, end)

    while len(heap) > 0:
        heap[0], heap[-1] = heap[-1], heap[0]
        curLocation = heap.pop(0)
        iterations += 1

        if visualize:
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

            drawPath(pxSize, curLocation, path[curLocation])
            clock.tick(speed)

        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            heap.append(x)
            addToHeap(heap, len(heap) - 1, heuristicTable)
            path[x] = path[curLocation] + [x]

        if not isConnected(heap[0], curLocation) and visualize:
            clearPath(pxSize, path[curLocation])
        
    raise RuntimeError("Could not reach END")
    return path[end]
    
#Draw an individual cell in a maze
def drawCell(pxSize, colour, borderColour, xCoord, yCoord, border=False):
    a = pygame.draw.rect(screen, colour, [xCoord*pxSize, yCoord*pxSize, pxSize, pxSize])
    if border:
        b = pygame.draw.rect(screen, borderColour, [xCoord*pxSize, yCoord*pxSize, pxSize, pxSize], 1)
    return [a,b] if border else [a]

#Only draws the path taken for the search (saves cpu)
def drawPath(pxSize, curLoc, path, curColour=(0,0,255), pathColour=(0,255,0), bgColour=(0,0,0)):
    rectList = []
    for yCoord, xCoord in path:
        rectList.extend(drawCell(pxSize, pathColour, bgColour, xCoord, yCoord, True))
    rectList.extend(drawCell(pxSize, curColour, bgColour, curLoc[1], curLoc[0], True))
    pygame.display.update(rectList)

def clearPath(pxSize, path):
    rectList = []
    for yCoord, xCoord in path:
        rectList.extend(drawCell(pxSize, (0,0,0), (0,0,0), xCoord, yCoord, False))
    pygame.display.update(rectList)

#Draws the entire maze
def renderMaze(maze, pxSize, curLoc=None, path=None, wallColour = (255,255,255), bgColour = (0,0,0), startEndColour=(255,0,0), curColour=(0,0,255), pathColour=(0,255,0)):
    start, end = findStartEnd(maze)
    screen.fill(bgColour)
    for yCoord, row in enumerate(maze):
        for xCoord, val in enumerate(row):
            if (yCoord, xCoord) == start or (yCoord, xCoord) == end:
                drawColour = startEndColour
            elif val == 1:
                drawColour = wallColour
            else:
                continue
            drawCell(pxSize, drawColour, bgColour, xCoord, yCoord, True)
    pygame.display.update()


mazeLength = int(input("Enter length of maze: "))
mazeWidth = int(input("Enter width of maze: "))
visualize = True if input("Visualize (Y/N): ").upper() == "Y" else False

maze = mazeCreate.createMaze(mazeLength, mazeWidth)
# mazeCreate.printMaze(maze)
temp = findStartEnd(maze)

if visualize:
    user32 = ctypes.windll.user32
    pxSize = min(roundDown(user32.GetSystemMetrics(0),2)//mazeWidth, roundDown(user32.GetSystemMetrics(1),2)//mazeLength)
    border = True if pxSize > 8 else False

    screenwidth, screenheight = pxSize*mazeWidth, pxSize*mazeLength
    screen = pygame.display.set_mode([screenwidth,screenheight])
    pygame.display.set_caption("Solving Maze...")
    clock = pygame.time.Clock()
    renderMaze(maze, pxSize)
    speed = 60

    foo = mazeSolverAStar
    directions = foo(maze, visualize=True)
    pygame.display.set_caption("Solved!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
else:
    attempts = int(input("Enter how many attempts: "))

    iterations = 0
    iterationsArray = [[],[],[]]
    for x in range(1, attempts + 1):
        print(f"Iteration ({x}/{attempts})", end="\r")

        foo = mazeSolverAStar
        directions = foo(maze)

        if pathVerify(maze, temp[0], directions):
            iterationsArray[0].append(iterations)
        else:
            raise RuntimeError("A-Star implementation failed")

        foo = mazeSolverBFS
        directions = foo(maze)

        if pathVerify(maze, temp[0], directions):
            iterationsArray[1].append(iterations)
        else:
            raise RuntimeError("BFS implementation failed")

        foo = mazeSolverDFS
        directions = foo(maze)

        if pathVerify(maze, temp[0], directions):
            iterationsArray[2].append(iterations)
        else:
            raise RuntimeError("DFS implementation failed")
    print("                                   ",end="\r")
    print("Done!")
    print("===================================")
    print(f"Average over {x} attempts: ")
    print(f"A-Star:")
    print(f"Mean: {statistics.mean(iterationsArray[0])}")
    print(f"Median: {statistics.median(iterationsArray[0])}")
    print(f"BFS:")
    print(f"Mean: {statistics.mean(iterationsArray[1])}")
    print(f"Median: {statistics.median(iterationsArray[1])}")
    print(f"DFS:")
    print(f"Mean: {statistics.mean(iterationsArray[2])}")
    print(f"Median: {statistics.median(iterationsArray[2])}")