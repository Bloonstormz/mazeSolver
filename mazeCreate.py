def findAdjacentNodes(maze, cell, corner=False, wall = True):
    mazeLen = len(maze)
    mazeWidth = len(maze[0])

    leftX = cell[1] - 1
    downY = cell[0] + 1
    rightX = cell[1] + 1
    upY = cell[0] - 1
    neighbours = []
    if wall:
        comp = 1
    else:
        comp = 0

    if downY <= len(maze) - 2 and maze[downY][cell[1]] == comp:
        neighbours.append((downY, cell[1]))
    if upY >= 1 and maze[upY][cell[1]] == comp:
        neighbours.append((upY, cell[1]))
    if leftX >= 1 and maze[cell[0]][leftX] == comp:
        neighbours.append((cell[0], leftX))
    if (downY < len(maze)) and rightX <= len(maze[downY]) - 2 and maze[cell[0]][rightX] == comp:
        neighbours.append((cell[0], rightX))
    return neighbours

def createMaze(length, width, corner = False, start = None):
    maze = [[1 for x in range(width)] for y in range(length)]
    potentialPath = set() #stores coords of cells that could become 0
    if start is None:
        start = (1, 1)
    maze[start[0]][start[1]] = 0
    visited = {start}
    potentialPath.update(findAdjacentNodes(maze, start, wall=True))

    while len(potentialPath) > 0:
        temp = potentialPath.pop()
        count = 0
        for x in findAdjacentNodes(maze, temp, wall=False):
            if x in visited:
                count += 1
        if count == 1:
            maze[temp[0]][temp[1]] = 0
            visited.add(temp)
            for x in findAdjacentNodes(maze, temp, wall=True):
                if x not in potentialPath:
                    potentialPath.add(x)
    
    maze = pickStartEnd(maze)

    return maze

def pickStartEnd(maze):
    for x in range(len(maze[0])):
        if maze[1][x] == 0:
            maze[0][x] = "S"
            break
    for x in range(len(maze[0]) - 2, -1, -1):
        if maze[-2][x] == 0:
            maze[-1][x] = "E"
            break
    return maze
    

def printMaze(maze):
    for x in maze:
        print(x)

if __name__ == "__main__":
    length = int(input("Enter length of maze: "))
    width = int(input("Enter width of maze: "))
    maze = createMaze(length, width)
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
            
            clock.tick(1)

    else:
        printMaze(maze)