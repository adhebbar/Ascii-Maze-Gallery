# Recursive backtracker algorithm from https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
# The depth-first search algorithm of maze generation implemented using backtracking:

# for backtracking:
# The maze is stored 2D array of (Nwall, Ewall, Swall, Wwall) tuples, where each element in the tuple is a boolean. 
# All walls initialized to True, but some are removed in the course of the backtracking to create the maze
# A stack/array thing stores solution/path

from Tkinter import *
import random
from PIL import Image, ImageDraw

def initMaze(rows, cols):
	maze = []                                                         
	for row in range(rows): maze+=[[None]*cols]
	for row in range(rows):
		for col in range(cols):
			box = [1,1,1,1] # initial values of (Nwall, Ewall, Swall, Wwall)   
			maze[row][col]= box
	return maze

def initVisitedCells(rows, cols):
	a = []
	for row in range(rows): a+=[[False]*cols] # inititalized to false
	return a

def removeWalls(maze, cell1, cell2): # where cell1 and cell2 are (row, col) tuples
	# assuming cell1 and cell2 are neighbours
	((row1, col1),(row2, col2))= (cell1, cell2)
	(removeWall1, removeWall2) = (None, None) 
	# hold the position of the wall tuple that must be removes
	if row1 == row2-1: removeWall1, removeWall2 = (2,0) #cell1 is to the north of cell2
	if row1 == row2+1: removeWall1, removeWall2 = (0,2) #cell1 is to the South of cell2
	if col1 == col2+1: removeWall1, removeWall2 = (3,1) #cell1 is to the East of cell2
	if col1 == col2-1: removeWall1, removeWall2 = (1,3) #cell1 is to the West of cell2
	maze[row1][col1][removeWall1] = 0
	maze[row2][col2][removeWall2] = 0
	#since backtracking never undoes the removal of walls, it is okay to detructrively modify 

def drawMaze(canvas, maze, width, height, offsetX, offsetY): # simultaneously create a jpeg picture using PIL, to test it. works!
	(rows, cols) = ( len(maze), len(maze[0]) )
	boxWidth = width/cols
	boxHeight = height/rows
	for row in range(rows):
		for col in range(cols):
			walls = maze[row][col]
			#drawing walls:
			if (walls[0]==1): #Nwall
				(startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, (col+1)*boxWidth, row*boxHeight)
				canvas.create_line(startX+ offsetX, startY+ offsetY, endX+ offsetX, endY+ offsetY, width = 2)
				draw.line((startX, startY, endX, endY), fill = 1) 
			if (walls[1]==1): #Ewall
				(startX, startY, endX, endY) =((col+1)*boxWidth, row*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight)
				canvas.create_line(startX+ offsetX, startY+ offsetY, endX+ offsetX, endY+ offsetY, width = 2) 
				draw.line((startX, startY, endX, endY), fill = 1)
			if (walls[2]==1): #Swall
				(startX, startY, endX, endY) =(col*boxWidth, (row+1)*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight)
				canvas.create_line(startX+ offsetX, startY+ offsetY, endX+ offsetX, endY+ offsetY, width = 2) 
				draw.line((startX, startY, endX, endY), fill = 1)
			if (walls[3]==1): #Wwall
				(startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, col*boxWidth, (row+1)*boxHeight)
				canvas.create_line(startX+ offsetX, startY+ offsetY, endX+ offsetX, endY+ offsetY, width = 2)
				draw.line((startX, startY, endX, endY), fill = 1)

def createImage(maze, width, height): #kinda like a test function for PIL drawCell and colour cell
	im = Image.new('RGB', (width+2, height+2) , "white")
	(rows, cols) = ( len(maze), len(maze[0]) )
	boxWidth = width/cols
	boxHeight = height/rows
	for row in range(rows-2):
		for col in range(cols):
			drawCell(im, maze, row, col, boxWidth, boxHeight,height)
	colourCell(im,"lightGreen", 3, 4,boxWidth,boxHeight,height)


def drawCell(image, maze, row, col, boxWidth, boxHeight,height): #for  PIL, not tkinter
	#col = len(maze[0])-1-col #bc AsciiGallery maze flips it over
	#row = len(maze)-1-row
	walls = maze[row][col]
	draw = ImageDraw.Draw(image) 
	#drawing walls:
	if (walls[0]==1): #Nwall
		(startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, (col+1)*boxWidth, row*boxHeight)
		draw.line((startX, height-endY, endX, height-startY), fill = 2) 
	if (walls[1]==1): #Ewall
		(startX, startY, endX, endY) =((col+1)*boxWidth, row*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight)
		draw.line((startX, height-endY, endX, height-startY), fill = 2)
	if (walls[2]==1): #Swall
		(startX, startY, endX, endY) =(col*boxWidth, (row+1)*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight)
		draw.line((startX, height-endY, endX, height-startY), fill = 2)
	if (walls[3]==1): #Wwall
		(startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, col*boxWidth, (row+1)*boxHeight)
		draw.line((startX, height-endY, endX, height-startY), fill = 2)
	image.save("out.jpg")

def colourCell(image,colour, row, col,boxWidth,boxHeight,height):
	draw = ImageDraw.Draw(image)
	(startX, startY, endX, endY) =(col*boxWidth +1, row*boxHeight+1, (col+1)*boxWidth-1, (row+1)*boxHeight-1)
	draw.rectangle((startX, height-endY, endX, height-startY), fill=colour)
	image.save("out.jpg")

def drawSolution(canvas, solution, maze, width, height, offsetX, offsetY):
	(rows, cols) = ( len(maze), len(maze[0]) )
	boxWidth = width/cols
	boxHeight = height/rows
	for box in solution:
		(row,col) = box
		(startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight)
		if row==0 and col==0:
			fill = "red"
		else: fill = "blue"
		canvas.create_rectangle(startX+ offsetX, startY+ offsetY, endX+ offsetX, endY+ offsetY, fill = fill, width = 0) 


def hasUnvisitedNeighbours(hasVisited,row,col):
	dirs = ( (0,1),(0,-1),(1,0),(-1,0) )
	for d in dirs:
		tRow, tCol = row+d[0], col+d[1]
		if 0<=tRow<len(hasVisited) and 0<=tCol<len(hasVisited[0]):
			if(hasVisited[tRow][tCol]==False):
				return True
	return False

def getRandomUnvisitedNeighbour(hasVisited, row, col): # assumes had unvisited
	dirs = ( (0,1),(0,-1),(1,0),(-1,0) )
	found = False
	while not found:
		i = random.randint(0,3)
		d = dirs[i]
		tRow, tCol = row+d[0], col+d[1]
		if 0<=tRow<len(hasVisited) and 0<=tCol<len(hasVisited[0]) and (hasVisited[tRow][tCol]==False):
			return(tRow, tCol)

def generateRandomMaze(rows, cols):
	maze = initMaze(rows, cols)
	hasVisited = initVisitedCells(rows, cols)
	stack = []
	currentCell = startCell = (0,0)
	#maze, stack = callWithLargeStack(backtracker,maze, hasVisited, stack, currentCell)
	maze, stack = backtracker(maze, hasVisited, stack, currentCell)
	#visualizeMaze(maze, stack)
	return (maze, stack)

def backtracker(maze, hasVisited, stack, currentCell): # currentCell is a tuple
	# print(maze)
	# print(hasVisited)
	# print(currentCell)
	(row,col) = currentCell
	hasVisited[row][col]=True 
	if not any(False in sublist for sublist in hasVisited): # checking if any unvisited cells, base case
		return maze, stack #stack is solution to maze 
	else:
		if hasUnvisitedNeighbours(hasVisited,row,col): 
			newCell = getRandomUnvisitedNeighbour(hasVisited, row, col) 
			stack.append(currentCell)
			removeWalls(maze, newCell, currentCell)
			currentCell = newCell
		else:
			currentCell = stack.pop()
		return backtracker(maze, hasVisited, stack, currentCell)

def testdrawMazeRemoveWalls(canvas, width, height): # helps visually test drawMaze and removeWalls
    maze = initMaze(5,5) # tested step 1, working

    # testing removewall:
    removeWalls(maze,(0,1),(0,2)) # vertical wall... works! cel11 west of cell2
    removeWalls(maze,(0,4),(0,3)) # vertical wall... works! cel11 East of cell2
    removeWalls(maze,(1,1),(2,1)) # horizaontal wall... works! cell1 north of cell2
    removeWalls(maze,(2,2),(1,2)) # horizaontal wall... works! cell1 South of cell2

    offsetX, offsetY = 5,5 
    drawMaze(canvas,maze,width-10,height-10, offsetX, offsetY) 
    # reducing height and width and adding offset of 5 because my tkinter is weird and omitts top left corner

def testHasUnvisitedNeighbours():
	hasVisited = initVisitedCells(2,2)
	hasVisited[0][0]=True
	hasVisited[0][1]=True
	print(hasUnvisitedNeighbours(hasVisited,1,1),True)
	hasVisited[1][0]=True
	print(hasUnvisitedNeighbours(hasVisited,1,1), False)

def generateDifficultMaze(rows, cols):
	# i want to generate a maze with a solution which is
	# a) not too short (avoiding left right intersections)
	# b) not too long (one straight path)
	# option 1:  keep generating mazes until I have a medium sized solution.
	# Also want maze (of size 5x5 and bigger) to have atleast 2 turns, where a wrong turn is possible
	boxes = rows*cols
	# assuming medium sized solution covers 60-80% of maze:
	minimum = int(0.4*boxes)
	maximum = int(0.6*boxes)
	found = False
	while not found:
		maze, stack = generateRandomMaze(rows,cols)
		if minimum<= len(stack) <= maximum:
			found = True
	return maze, stack

def draw(canvas, width, height): # only for debugging purpose; i'm not actually going to use a 2D image in the game
	rows, cols = 7,7
	maze, stack = generateDifficultMaze(rows, cols)
	#testHasUnvisitedNeighbours()
	offsetX, offsetY = 5,5 
	drawSolution(canvas, stack, maze, width-10, height-10, offsetX, offsetY)
	drawMaze(canvas,maze,width-10,height-10, offsetX, offsetY)

def runDrawing(width=300, height=300):
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    draw(canvas, width, height) 
    root.mainloop()
    print("bye!")

def visualizeMaze(maze, stack, width=300, height=300): # draws specefic solution and maze
    root = Tk()
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    (offsetX, offsetY) = (7,7) 
    drawSolution(canvas, stack, maze, width-10, height-10, offsetX, offsetY)
    drawMaze(canvas,maze,width-10,height-10, offsetX, offsetY) 
    root.mainloop()
    print("bye!")

#runDrawing()

(maze, stack) = generateRandomMaze(5, 5)
createImage(maze,400, 400)
