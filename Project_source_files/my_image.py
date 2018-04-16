# CODE IS ABLE TO DO GREYSCALE ALGORRIHTM IE CONVERT FROM INAGE TO ASCII CAHRACTER IMAGE
# HIGH LEVEL ALGORITHM FROM: http://www.jave.de/image2ascii/algorithms.html

import PIL
from PIL import Image
import math
import random 
import decimal

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))
    #FROM CMU 15-112 COURSE WEBSITE

def calculateInstensity(pixels, blockCol, blockRow, block_height, block_width, height, width): #TODO
	startCol = roundHalfUp(blockCol*block_width)
	startRow = roundHalfUp(blockRow*block_height)
	endCol = roundHalfUp(min(startCol+block_width, width))
	endRow = roundHalfUp(min(startRow+block_height, height))
	sum = 0
	blocks = 0
	#print(startRow, startCol, endRow, endCol)
	for i in range(startRow, endRow):
		for j in range(startCol, endCol):
			(R,G,B)= pixels[j, i] #(col, row) bc pixel take (width, height)
			total = R+G+B
			avg = total//3 # pixels only use whole numbers
			sum+= avg
			blocks+=1
	if blocks==0: return 0 #takes care of divide by 0 error
	intensity = roundHalfUp(sum/blocks)
	return intensity

def mapToAscii(intensity):
	ascii_chars = [ '#', 'A', '@', '%', 'S', '+', '<', '*', ':', ',', '.',' '] # highest to lowest 
	# ABOVE ARRAY OBTAINED FROM http://www.jave.de/image2ascii/algorithms.html
	#ascii_chars.reverse() # now lowest to highest
	maxIntensity = 255
	for i in range(len(ascii_chars)):
		lower_bound = roundHalfUp(i*maxIntensity/len(ascii_chars))
		upper_bound = roundHalfUp((i+1)*maxIntensity/len(ascii_chars))
		if lower_bound<=intensity<=upper_bound: 
			return ascii_chars[i]

def readFile(path):
    with open(path, "rt") as f:
        return f.read()
#From http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
#From http://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO

def picToAscii(imageFile,AsciiTextFile):
	img = Image.open(imageFile)          
	maxsize = (150, 150)
	img.thumbnail(maxsize, PIL.Image.ANTIALIAS) # resizing
	width, height = img.size
	#print("dims",height,width)
	pixels = img.load()
	toWrite = ""
	#path = "ASCII_img.txt"
	(block_width, block_height)= (1,2) # ratio helps compress picture in one direction 
	(blockCols, blockRows) = roundHalfUp(width/block_width), roundHalfUp(height/block_height)
	#print(blockCols, blockRows ,block_height, block_width )
	for blockRow in range( blockRows):
		for blockCol in range(blockCols):
			if blockCol ==0 and blockRow!=0: 
				toWrite+="\n" # jumps to a newline at the start of every row
			intensity =  calculateInstensity(pixels, blockCol, blockRow, block_height, block_width, height, width)
			char = mapToAscii(intensity)
			toWrite+= char
	#creating text file:
	#writeFile(AsciiTextFile, toWrite) #for debugging purposes
	# contentsRead = readFile(AsciiTextFile)
	# assert(contentsRead == toWrite)
	#print(toWrite)
	return toWrite

def addMessage(ascii_pic, message ):
	ascii_pic = ascii_pic.splitlines() #converting to 2dish array thing
	rows = len(ascii_pic)
	cols = len(ascii_pic[0])
	dirs = ((1,0),(0,1),(1,1))
	length = len(message)
	found = False
	ascii_chars = [ '#', 'A', '@', '%', 'S', '+', '<', '*', ':', ',', '.',' ']
	while not found:
		direction = dirs[random.randint(0,len(dirs)-1)]
		drow, dcol = direction[0], direction[1]
		startRow = random.randint(0,rows-1)
		endRow = startRow+ length*drow
		startCol = random.randint(0,cols-1)
		endCol = startCol+ length*dcol
		if endRow>=rows or endCol>=cols: continue
		print(rows, cols, startRow, startCol)
		startChar = ascii_pic[startRow][startCol]
		endChar = ascii_pic[endRow][endCol]
		startDark = ascii_chars.index(startChar)
		endDark = ascii_chars.index(endChar)
		tolerance = 5
		if startDark<=tolerance and endDark<=tolerance:
			found = True

	for i in range(length):
		char = message[i]
		row = startRow + drow*i
		col = startCol + dcol*i
		ascii_pic[row] = ascii_pic[row][:col] + char + ascii_pic[row][col+1:]

	ascii_pic= "\n".join(ascii_pic)  # converting back to string
	return(ascii_pic)

#print(picToAscii("pictures/pepe.jpg",'foo')) # testing

	




