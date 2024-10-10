import random

def findAdjacentNodes(maze, cell, wall = True, mazeLenLimit = None, mazeWidthLimit = None):
    if mazeLenLimit is None or mazeWidthLimit is None:
        mazeLenLimit, mazeWidthLimit = len(maze) - 2, len(maze[0]) - 2
    leftX = cell[1] - 1
    downY = cell[0] + 1
    rightX = cell[1] + 1
    upY = cell[0] - 1
    neighbours = []
    if wall:
        comp = 1
    else:
        comp = 0

    if downY <= mazeLenLimit and maze[downY][cell[1]] == comp: #Check bottom
        neighbours.append((downY, cell[1]))
    if upY >= 1 and maze[upY][cell[1]] == comp: #Check Up
        neighbours.append((upY, cell[1]))
    if leftX >= 1 and maze[cell[0]][leftX] == comp: #Check Left
        neighbours.append((cell[0], leftX))
    if rightX <= mazeWidthLimit and maze[cell[0]][rightX] == comp: #Check Right
        neighbours.append((cell[0], rightX))
    return neighbours

def createMaze(length, width, start = None, end = None, seed=None):
    if seed is not None:
        random.seed(seed)
    maze = [[1 for x in range(width)] for y in range(length)]
    potentialPath = [] #stores coords of cells that could become 0
    if start is None:
        start = (1, 1)
    elif isinstance(start, str) and start.lower() == "random":
        start = (random.randrange(length), random.randrange(width))
    if end is None:
        end = (length-2, width-2)
    elif isinstance(end, str) and end.lower() == "random":
        end = (random.randrange(length)), random.randrange(width)
        while end == start:
            end = (random.randrange(length), random.randrange(width))
    
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 1
    allPaths = {start} #Stores coords of nodes that are 0 (path cells)
    endAdjacent = {x for x in findAdjacentNodes(maze, end, wall=True, mazeLenLimit=length-2, mazeWidthLimit=width-2)}

    #Selects only one adjacent node to start and end (ensure only one valid path to and from start node and end node)
    potentialPath.append(random.choice(findAdjacentNodes(maze, start, wall=True, mazeLenLimit=length-2, mazeWidthLimit=width-2)))

    while len(potentialPath) > 0:
        temp = potentialPath.pop(random.randrange(0,len(potentialPath)))
        count = 0
        for x in findAdjacentNodes(maze, temp, wall=False, mazeLenLimit=length-2, mazeWidthLimit=width-2):
            if x in allPaths:
                count += 1
        if count == 1: #If there's only one way into temp (i.e one empty cell next to temp) then mark it as empty
            maze[temp[0]][temp[1]] = 0
            allPaths.add(temp)
            if temp in endAdjacent:
                maze[end[0]][end[1]] = 0
                allPaths.add(end)
            potentialPath.extend(findAdjacentNodes(maze, temp, wall=True, mazeLenLimit=length-2, mazeWidthLimit=width-2)) #Add all adjacent walls
    
    #Check if end is not trapped (rare edge case) - usually results in split paths (paths w/ multiple adjacencies)
    if not findAdjacentNodes(maze, end, wall=False):
        endPath = {end}

        potentialPath.append(random.choice(findAdjacentNodes(maze, end, wall=True, mazeLenLimit=length-2, mazeWidthLimit=width-2)))
        while len(potentialPath) > 0:
            temp = potentialPath.pop(random.randrange(0,len(potentialPath)))
            count = 0
            for x in findAdjacentNodes(maze, temp, wall=False, mazeLenLimit=length-2, mazeWidthLimit=width-2):
                if x in allPaths:
                    maze[temp[0]][temp[1]] = 0
                    potentialPath = []
                    break
                if x in endPath:
                    count += 1
            if count == 1: #If there's only one way into temp (i.e one empty cell next to temp) then mark it as empty
                maze[temp[0]][temp[1]] = 0
                allPaths.add(temp)
                potentialPath.extend(findAdjacentNodes(maze, temp, wall=True, mazeLenLimit=length-2, mazeWidthLimit=width-2)) #Add all adjacent walls


    maze = pickStartEnd(maze, start, end)

    return maze

def pickStartEnd(maze, start=None, end=None):
    if start is None:
        for x in range(len(maze[0])):
            if maze[1][x] == 0:
                maze[1][x] = "S"
                break
    else:
        maze[start[0]][start[1]] = "S"
    if end is None:
        for x in range(len(maze[0]) - 2, -1, -1):
            if maze[-2][x] == 0:
                maze[-2][x] = "E"
                break
    else:
        maze[end[0]][end[1]] = "E"
    return maze
    

def printMaze(maze):
    for x in maze:
        print(x)

if __name__ == "__main__":
    length = int(input("Enter length of maze: "))
    width = int(input("Enter width of maze: "))
    maze = createMaze(length, width, "random", "random", seed=1234567890)
    if input("Pygame visualize (Y/N): ").lower() == "y":
        import pygame
        from MazeVisualizer import renderMaze, calcPixel
        pxSize, screenwidth, screenheight, border = calcPixel(length, width)
        screen = pygame.display.set_mode([screenwidth,screenheight])
        renderMaze(screen, maze, pxSize, border=border)
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            clock.tick(60)

    else:
        printMaze(maze)