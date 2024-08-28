import MazeCreate
import statistics

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

def mazeSolverBFS(maze, start = None, end = None):
    global iterations
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
            
        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            searchQueue.append(x)
            path[x] = path[curLocation] + [x]
 
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

        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            searchStack.append(x)
            path[x] = path[curLocation] + [x]
        
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

def addToHeap(heap, curPos, key=lambda x : x):
    item = heap[curPos] #store item to move
    while curPos > 0:
        parentPos = (curPos - 1) >> 1
        parentItem = heap[parentPos]
        if key(item) < key(parentItem):
            heap[curPos] = parentItem
            curPos = parentPos
            continue
        break
    heap[curPos] = item #reinsert item

def mazeSolverAStar(maze, start = None, end = None):
    global iterations
    if start is None or end is None:
        temp = findStartEnd(maze)
        start = temp[0]
        end = temp[1]

    def fetchHeuristicVal(pos):
        nonlocal heuristicTable
        return heuristicTable[pos[0]][pos[1]]

    iterations = 0
    # Maze solving
    path = {start : [start]} # Dictionary to store path taken to all points
    heap = [start] # Queue containing elements to search
    heuristicTable = generateHeuristic(maze, end)

    while len(heap) > 0:
        curLocation = heap.pop(0)
        iterations += 1

        for x in findUnsearchedNodes(maze, curLocation, path):
            if x == end:
                return path[curLocation] + [end]
            heap.append(x)
            addToHeap(heap, len(heap) - 1, fetchHeuristicVal)
            path[x] = path[curLocation] + [x]
        
    raise RuntimeError("Could not reach END")
    

if __name__ == "__main__":
    mazeLength = int(input("Enter length of maze: "))
    mazeWidth = int(input("Enter width of maze: "))
    attempts = int(input("Enter how many attempts: "))

    iterations = 0
    iterationsArray = [[],[],[]]
    for x in range(1, attempts + 1):
        maze = MazeCreate.createMaze(mazeLength, mazeWidth)
        temp = findStartEnd(maze)
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