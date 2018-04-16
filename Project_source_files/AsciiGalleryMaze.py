###SOME CODE TAKEN FROM 112 PANDA3D DEMO https://drive.google.com/drive/folders/0B-l6oO5PZ7hTWjlUMVFaV01tSE0
### SOME CAMERAVIEW FUNCTION CODE TAKEN FROM https://www.panda3d.org/manual/index.php/Controlling_the_Camera

from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import maze
import random
from my_image import addMessage
from pandac.PandaModules import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from my_image import picToAscii
from PIL import Image, ImageDraw
import os
import time

def probability(n): #probabilty of function returning true is 1/n
    i = random.randint(1,n)
    return (i==n)

def listFiles(path = "pictures"): # FROM http://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#listFiles
    if (os.path.isdir(path) == False):
        # base case:  not a folder, but a file, so return singleton list with its path
        return [path]
    else:
        # recursive case: it's a folder, return list of all paths
        files = [ ]
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

class MyApp(ShowBase):
    def __init__(self, rows, cols,instance = 0,picturesConcentration = 5,trial = 0):
        self.trial = trial
        ShowBase.__init__(self)  
        self.setIntitalValues(rows,cols,instance, picturesConcentration)

    def initPictures(self):
        self.pictures = listFiles()
        self.pictures.remove('pictures/.DS_Store') #???
        for i in range(len(self.pictures)):
            self.pictures[i] = picToAscii(self.pictures[i],'foo.txt')

    def splashScreenCreate(self, number):
        text1a = " Urgent message from ur PC:"
        text1b =  "XyzBugz234VirusThingamajig, a very competent virus has taken over your computer..." 
        text1c = " It has also managed to put you in a virtual ASCII maze in your computer! " 
        text1d = " (because thats a thing that can happen) "
        text2a = "But dont worry, the antivirus software installed on your computer 'BFREE4EVR' will help you escape..." 
        text2b = "Drag your favorite pictures (preferably jpeg) to the 'pictures' folder in the directory of the game. "
        text2c = "You'll see these pictures in ASCII format in the maze. BFREE4EVR will add messages in these pictures to help guide you." 
        text2d = "Look for the hidden message in each picture you see; it will tell you whether you're om the right track or not."
        text2e = "if you're not on the right track, you should 'backtrack' to the last turn (hint ;) )"
        text3a = "Find the flag to complete the maze! (the flag is the only object thats not in black and white)"
        text3b = "Press 'h' at any time to toggle the help mini-sreen once the game starts."
        text3c = "There is also a helpful mini-map in the bottom right corner of ur screen, that shows the cells of the maze you've visited"
        text3d = "Be sure to solve the maze within the time limit indicated in the top left corner, or ur pc will b compromised."
        text3e = "However, the first level does not have a timer, so you can get comfortable with the controls"
        text3f = "The pictures may look glitchy because of the virus. You have to search them from a close distance. Good luck!"
        subtext = "[press q to continue]"
        text4a = "This is a buffer screen. Please dont panic. 'BFREE4EVR' is doing its thing. "
        text4b = "This may take anywhere from 30 seconds (regular case) to an eternity depending on how shitty ur pc is."
        text4d = "Oh! Almost forgot, policy requires that u provide BFREE4EVR consent to run on ur pc "
        text4c = "...\n...\n...\n...\n...\n...\n..."
        text4e = "[press q to provide consent and agree to terms and conditions etc and continue with loading game]"
        text4f = "...................This is another buffer screen................."
        text4g = "press q to start loading model, and then wait  a while"

        if number ==1:splashText = "\n".join([text1a,text1b,text1c, text1d, subtext])
        if number ==2:splashText = "\n".join([text2a,text2b,text2c, text2d, text2e, subtext])
        if number ==3:splashText = "\n".join([text3a,text3b,text3c,text3d, text3e, text3f, subtext])
        #if number ==4:splashText = "\n".join([text4a,text4b])
        if number ==4:
            if self.instance==0:
                splashText = "\n".join([text4a,text4b,text4c,text4d,text4e])
            else: 
                splashText = "\n".join([text4f,text4g])        
        text = TextNode('meh')
        text.setCardColor(1, 1, 1, 1) # white
        text.setCardAsMargin(0.2, 0.2, 20, 0.2)
        text.setCardDecal(True)
        text.setText(splashText)
        text.setAlign(TextNode.ALeft)
        text.setFrameColor(0, 0, 0, 1) # black, and not transparent
        text.setTextColor(0, 0, 0, 1) # black, and not transparent
        text.setFrameAsMargin(0.2, 0.2, 20, 0.2) #specifying margins for frame
        text.setShadow(0.05, 0.05)
        text.setShadowColor(0, 0, 0, 1)
        textNodePath = self.aspect2d.attachNewNode(text)
        self.splashTextObject = textNodePath 
        textNodePath.setPos(-1.1,0,0.8)
        textNodePath.setScale(0.1)
        text.setWordwrap(22)

    def setIntitalValues(self, rows, cols, instance, picturesConcentration):
        self.picturesConcentration = picturesConcentration
        self.rows, self.cols = rows, cols
        self.instance = instance
        if instance == 0: 
            self.splashScreen = 1
            self.splashScreenCreate(1)
        else:  
            self.splashScreenCreate(4)
            self.splashScreen = 4
        self.mode = "splashScreen" 
                #some key mapping 
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0, "stop":False,  "camLeft":0, "camRight":0, "camForward":0, "camBackward":0 } 
        self.keyMap["up"], self.keyMap["down"]  = [0,0]  # only for debugging purposes, will be removed from actual game
        self.keyMap["createNewGame"]= 0
        self.keyMap["nextScreen"]= 0
        self.createKeyControls()
        timer = 0.2
        taskMgr.doMethodLater(timer, self.move, "move")
 
        #self.setMazeValues(self.rows, self.cols)

    def setMazeValues(self, rows, cols):
        self.gameWon = False
        if self.instance>0: #timer stuff
            secondsTimer = 1 #(measures seconds)
            self.time = 46
            if self.instance==2: 
                self.time = 61 # bigger maze, more time.. :/
            taskMgr.doMethodLater(secondsTimer, self.timer, "timer")
            self.timerText = TextNode('time?')
            self.timerText.setAlign(TextNode.ALeft)
            self.timerText.setFrameColor(0, 1, 0, 1) # black, and not transparent
            self.timerText.setTextColor(0, 1, 0, 1) # black, and not transparent
            self.timerText.setFrameAsMargin(0.2, 0.2, 0.2, 0.2) #specifying margins for frame
            self.timerText.setShadow(0.05, 0.05)
            self.timerText.setShadowColor(0, 0, 0, 1)
            timeTextNodePath = self.aspect2d.attachNewNode(self.timerText)
            timeTextNodePath.setPos(-1.3,0,0.75)
            timeTextNodePath.setScale(0.06)
        self.initPictures()
        self.gameOver = False
        # Load the environment model.
        self.scene = self.loader.loadModel("box.egg")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        #self.buffer = OnscreenImage(image = 'out2.jpg', pos = (0, 0, 0)) # adding buffer image
        #building the maze:
        self.randMaze, self.solution = maze.generateDifficultMaze(rows, cols)
        # The mickey picture I'm using was taken from: https://s-media-cache-ak0.pinimg.com/236x/9b/a2/57/9ba25796112cad616be27e473ae1e149.jpg
        #self.buffer.destroy()
        self.boxWidth = 200.0#550
        self.boxHeight = 200.0#550 
        self.wallHeight = 30.0  
        # above values found by trial and error. I think this gives the best user experience
        min, max = self.scene.getTightBounds()
        size = max-min
        (self.width, self.height) = (self.boxWidth*cols,self.boxHeight*rows)  # calculating dimesions of scene
        # Apply scale and position transforms on the model.
        self.scene.setPos(self.width/2,self.height/2, 0) # so that left bottom corner is (0,0)
        self.scene.setScale(self.width/size[0],self.height/size[1], 1)
        self.xWallBounds = []
        self.yWallBounds = []
        
        self.buildMaze(rows,cols)
        self.taskMgr.add(self.CameraView, "CameraView")

        #initalizing some more values
        self.CamOreintX, self.CamOreintY = 0,0
        self.angleRadians = 0
        self.camZpos  = self.wallHeight*2
        self.moveUnit = 5.0
        self.deltaAngle = 1
        self.text1a = "use (W,A,S,D) to change camera orientation (up, left, down, right)"
        self.text1b = "use arrow keys to move camera forward, backward, left or right"
        self.text1c = "press z to move camera up, x to move camera down."
        self.text1d = "press h to toggle these annoying instructions"
        self.text1 = "\n".join([self.text1a,self.text1b,self.text1c,self.text1d])

        #show instructions on screen
        self.showInstructions = False
        if self.instance ==0: self.Instructions()
        y = self.height
        #creating image shown at bootom left corner
        self.cellsVisited = set()
        self.imageWidth = 200
        self.imageHeight = 200
        self.imageMap = Image.new('RGB', (self.imageWidth, self.imageHeight) , "lightGrey") 
        self.imageMap.save("out0.jpg")
        self.imageObject = OnscreenImage(image = 'out0.jpg', pos = (0, 0, 0))
        maze.colourCell(self.imageMap, "darkGrey", 0, 0, self.imageWidth/cols,self.imageHeight/rows,self.imageHeight)
        self.count = 0
        self.oldRow, self.oldCol = 0,0
        self.updateImage()
        self.hasImageObject = True
        # Add the CameraView procedure to the task manager.
        self.taskMgr.add(self.CameraView, "CameraView")

    def updateImage(self):
        currRow = int(self.camYpos//self.boxHeight)
        currCol = int(self.camXpos//self.boxWidth)
        (rows, cols) = ( len(self.randMaze), len(self.randMaze[0]) )
        boxWidth = self.imageWidth/cols
        boxHeight = self.imageHeight/rows
        imageName = "out"+str(self.count)+"trial"+str(self.trial)+".jpg"
        r = self.angleRadians*(180.0/pi)
        if self.oldRow!= currRow or self.oldCol != currCol:
            maze.colourCell(self.imageMap, "white", self.oldRow, self.oldCol, boxWidth,boxHeight,self.imageHeight)
            maze.colourCell(self.imageMap, "darkGrey", currRow, currCol, boxWidth,boxHeight,self.imageHeight)
            self.imageMap.save(imageName)
            self.imageObject.destroy()
            self.oldRow , self.oldCol = currRow, currCol
            self.imageObject = OnscreenImage(image = imageName, pos = (0.85, 0, -0.65), scale= (0.25,1,0.25), hpr = (0,0,r))
            self.count+=1
            imageName = "out"+str(self.count)+"trial"+str(self.trial)+".jpg"

        if (currRow,currCol) not in self.cellsVisited:
            self.cellsVisited.add((currRow,currCol))
            maze.drawCell(self.imageMap,self.randMaze, currRow, currCol, boxWidth, boxHeight,self.imageHeight)
            self.imageMap.save(imageName)
            self.imageObject.destroy()
            self.imageObject = OnscreenImage(image = imageName, pos = (0.85, 0, -0.65), scale= (0.25,1,0.25), hpr = (0,0,r))
            self.count+=1

    def gameWonOrLost(self):
        if self.gameWon:
            if self.instance ==0: text = "U WON THE GAME !!1!1!!1\n lol just kidding. You won level one!\n press P to go to the next level\n(Fewer pictures, bigger maze) "
            if self.instance ==1: text = "GoOd JoB 1!!!1!1!! YOu KnoW tHE drILl! neXT leVEl comiNg up.\n press P to go to the next level"
            if self.instance ==2: text = "U WON THE GAME !!1!1!!1 YOu escaped the virus.\n(for realz this time YAY!)\nPress P to play again! "
        else: text = "You just lost the level you noob.\nLuckily, you get infinite chances.\nPress P to try again."

        self.text = TextNode('bleh')
        self.text.setAlign(TextNode.ACenter)
        self.text.setText(text)
        textNodePath = aspect2d.attachNewNode(self.text)
        textNodePath.setScale(0.09)
        self.text.setCardColor(0, 0, 0, 1)
        self.text.setCardAsMargin(20, 20, 20, 20)
        self.text.setCardDecal(True)
        self.gameOver = True
        self.imageObject.destroy()
        self.hasImageObject = False

        #print("gameOver is "+str(self.gameOver))

    def newGame(self):
        self.text.clearText()
        self.deleteAll()
        taskMgr.remove('move')
        taskMgr.remove('CameraView')
        taskMgr.remove('timer')
        self.destroy()
        self.deleteImages()
        if self.gameWon: # next level or restart
            if self.instance ==2: self.__init__(5, 5, 0, 5, self.trial+1) #reset
            else: self.__init__(self.rows +2, self.cols +2, self.instance +1,self.picturesConcentration +2, self.trial+1)
        else:
            self.__init__(self.rows , self.cols , self.instance ,self.picturesConcentration, self.trial+1) # same level 


    def deleteAll(self):
            for m in render.getChildren():
                m.removeNode()
    def deleteImages(self):
        for i in range(self.count):
            filename = "out"+str(i)+"trial"+str(self.trial)+".jpg"
            os.remove(filename)

    def addPicture(self,x,y,h,row, col):
        if not probability(self.picturesConcentration): return
        i = random.randint(0,len(self.pictures)-1)
        pictureText = self.pictures[i]
        if(row,col) in self.solution:
            pictureText = addMessage(pictureText,"you're on the right track!")
        else: pictureText = addMessage(pictureText,"looks like you took a wrong turn!")
        z = 66
        text = TextNode('node name')
        text.setCardColor(1, 1, 1, 1) # white
        text.setCardAsMargin(0, 0, 0, 0)
        text.setCardDecal(True)
        #contentsRead = readFile("mickeyText.txt")
        text.setText(pictureText)
        text.setAlign(TextNode.ALeft)
        font = loader.loadFont('Menlo.ttf') # font dowloaded from : "http://www.onlinewebfonts.com"
        text.setFont(font)
        text.setFrameColor(0, 0, 0, 1) # black, and not transparent
        text.setTextColor(0, 0, 0, 1) # black, and not transparent
        text.setFrameAsMargin(0.2, 0.2, 0.1, 0.1) #specifying margins for frame
        text.setShadow(0.05, 0.05)
        text.setShadowColor(0, 0, 0, 1)
        textNodePath = self.render.attachNewNode(text)
        textNodePath.setPos(x,y,z)
        textNodePath.setHpr(h,0,0)
        textNodePath.setScale(0.6)


    def buildMaze(self, rows, cols):
        randMaze, solution = self.randMaze, self.solution
        maze.createImage(randMaze, 400, 400)
        self.endPoints = solution[-1]
        self.winXbounds = []
        boxWidth = self.boxWidth 
        boxHeight =self.boxHeight 
        wallWidth = self.wallWidth = 5.0
        print(boxWidth, boxHeight, wallWidth)
        wallHeight = self.wallHeight 
        wall= loader.loadModel("box.egg")
        min, max = wall.getTightBounds()
        size = max-min
        (initialWidth, intialHeight) = (size[0],size[1]) # of box.egg
        k = wallWidth # added to wall length to guarantee smooth corners

        for row in range(rows):
            for col in range(cols):
                walls = randMaze[row][col]
                #creating walls:
                if (walls[0]==1): #Nwall
                    (startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, (col+1)*boxWidth, row*boxHeight) 
                    self.addWall(startX, startY, endX, endY, True, boxWidth, boxHeight, wallWidth, wallHeight, initialWidth, intialHeight, k)
                    self.addPicture(startX + wallWidth + boxWidth/2 , endY + 0.8*wallWidth,180,row, col )

                if (walls[1]==1):  
                    (startX, startY, endX, endY) =((col+1)*boxWidth, row*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight) 
                    if col== cols -1: #Ewall
                        self.addWall(startX, startY, endX, endY, False, boxWidth, boxHeight, wallWidth, wallHeight, initialWidth, intialHeight, k)
                    self.addPicture(endX - 0.8*wallWidth , startY + wallWidth + boxHeight/2 , 270, row, col )

                if (walls[2]==1):
                    (startX, startY, endX, endY) =(col*boxWidth, (row+1)*boxHeight, (col+1)*boxWidth, (row+1)*boxHeight) 
                    if row == rows-1: #Swall
                        self.addWall(startX, startY, endX, endY, True, boxWidth, boxHeight, wallWidth, wallHeight, initialWidth, intialHeight, k)
                    self.addPicture(startX + wallWidth + boxWidth/2 , endY - 0.8*wallWidth, 0, row, col )

                if (walls[3]==1): #Wwall
                    (startX, startY, endX, endY) =(col*boxWidth, row*boxHeight, col*boxWidth, (row+1)*boxHeight) # vertical
                    self.addWall(startX, startY, endX, endY, False, boxWidth, boxHeight, wallWidth, wallHeight, initialWidth, intialHeight, k)
                    self.addPicture(endX + 0.8*wallWidth , startY + wallWidth + boxHeight/2 , 90, row, col )

        for row in range(rows+1):
            for col in range(cols+1):
                (x, y, z) =(col*boxWidth, row*boxHeight, 0)
                model =  loader.loadModel("box.egg")
                model.setScale(wallWidth, wallWidth, wallHeight)
                model.reparentTo(render)
                model.setPos(x,y,z)
                MyApp.applyRandomTexture(model,0)
                (min,max) = model.getTightBounds()
                (minX, minY, maxX, maxY) = (min[0], min[1], max[0], max[1])
                k = 2  # panda renders weirdly at certain viewpoints if one gets too close to model :?
                self.xWallBounds+=[(minX-k, maxX+k)]
                self.yWallBounds+=[(minY-k, maxY+k)]

        self.initializeStartAndEnd(boxWidth, boxHeight,wallHeight, self.endPoints)
        self.splashTextObject.removeNode()
        #self.addFlag() #adds flag to end position

    def initializeStartAndEnd(self,boxWidth, boxHeight, wallHeight, endPoints):
        #initializing start position of camera:
        self.camXpos = boxWidth/2
        self.camYpos = boxHeight/2
        # adding flag to end of maze as recored by the solution
        model =  loader.loadModel("banner/banner.egg") # model from http://alice.org/pandagallery/Medieval/index.html
        model.reparentTo(render)
        lo, hi = model.getTightBounds()
        size = hi-lo
        intialHeight = size[0]
        (endRow, endCol) = endPoints
        model.setPos(endCol*boxWidth + boxWidth/2, endRow*boxHeight + boxHeight/2,0)
        scaleFactor = wallHeight*0.7/intialHeight
        model.setScale(scaleFactor,scaleFactor,scaleFactor)
        tex = loader.loadTexture('banner/bannero_3_-_Default_CL.tif')
        model.setTexture(tex)

    def addWall(self, startX, startY, endX, endY, isHorizontal, boxWidth, boxHeight, wallWidth, wallHeight, initialWidth, intialHeight, k):
        model =  loader.loadModel("box.egg")
        if isHorizontal:
            model.setScale(boxWidth/initialWidth-k, wallWidth, wallHeight) #horizontalWall
        else: 
            model.setScale(wallWidth, boxHeight/intialHeight-k, wallHeight) #verticallWall
        self.addModel(startX, startY, endX, endY, model, wallWidth, True)
        MyApp.applyRandomTexture(model,1)

    @staticmethod
    def applyRandomTexture(model, i):
        textures = ['blackWhite1.jpeg','blackWhite2.jpg']
        # blacWhite2 from http://cdn.pcwallart.com/images/gradient-black-to-white-square-wallpaper-4.jpg
        # blackWhite1 from http://cdn.pcwallart.com/images/gradient-black-to-white-wallpaper-2.jpg
        tex = loader.loadTexture(textures[i])
        model.setTexture(tex)

    def addModel(self,startX, startY, endX, endY, model, wallWidth, isHorizontal):
        x = (startX+endX)/2
        y = (startY+endY)/2
        z = 0
        #print(self.xWallBounds, self.yWallBounds)
        #print(self.width, self.height, self.boxWidth, self.boxHeight, wallWidth)
        model.reparentTo(render)
        model.setPos(x,y,z)
        (min,max) = model.getTightBounds()
        (minX, minY, maxX, maxY) = (min[0], min[1], max[0], max[1])
        k = 2  # panda renders weirdly at certain viewpoints if one gets too close to model :?
        self.xWallBounds+=[(minX-k, maxX+k)]
        self.yWallBounds+=[(minY-k, maxY+k)]

    def setKey(self, key, value):
        self.keyMap[key] = value

    def createKeyControls(self):
        self.accept("r", self.setKey, ["stop", not self.keyMap["stop"]])
        self.accept("h", self.Instructions )
        self.accept("z", self.setKey, ["up",1])
        self.accept("x", self.setKey, ["down",1])
        self.accept("q", self.nextSplashScreen)
        self.accept("p", self.setKey, ["createNewGame",1])

        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_down", self.setKey, ["backward", 1])
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])

        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("arrow_down-up", self.setKey, ["backward", 0])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])

        self.accept("w", self.setKey, ["camForward", 1])
        self.accept("s", self.setKey, ["camBackward", 1])
        self.accept("a", self.setKey, ["camLeft", 1])
        self.accept("d", self.setKey, ["camRight", 1])

        self.accept("w-up", self.setKey, ["camForward", 0])
        self.accept("s-up", self.setKey, ["camBackward", 0])
        self.accept("a-up", self.setKey, ["camLeft", 0])
        self.accept("d-up", self.setKey, ["camRight", 0])

        self.accept("z-up", self.setKey, ["up", 0])
        self.accept("x-up", self.setKey, ["down", 0])

    def nextSplashScreen(self):
        self.splashTextObject.removeNode()
        self.splashScreen+=1
        if self.splashScreen>5: self.splashScreen =5
        print(self.splashScreen)
        if self.splashScreen ==5 and self.mode == "splashScreen":
            self.mode = "game"
            self.setMazeValues(self.rows, self.cols)
        elif self.mode == "splashScreen": 
            self.splashScreenCreate(self.splashScreen)

    def cameraMove(self, dy, dx):
        self.camYpos +=dy
        self.camXpos +=dx
        for i in range(len(self.xWallBounds)):
            xInterval = self.xWallBounds[i]
            (xLow, xHigh) = (xInterval[0],xInterval[1])
            yInterval = self.yWallBounds[i]
            (yLow,yHigh) = (yInterval[0],yInterval[1])
            if (xLow<=self.camXpos<=xHigh and yLow<=self.camYpos<=yHigh) or self.camZpos<=1:
                    self.camXpos -=dx
                    self.camYpos -=dy
                    #print(self.camXpos,self.camYpos, xLow, xHigh, yLow, yHigh)
                    return
        (winRow, winCol) = self.endPoints
        k = 30 # you must go into winning cell
        (winXlow, winXhigh) = (winCol*self.boxWidth +k, (winCol+1)*self.boxWidth -k) 
        (winYlow, winYhigh) = (winRow*self.boxHeight +k, (winRow+1)*self.boxHeight-k) 
        if winXlow<self.camXpos<winXhigh and winYlow<self.camYpos<winYhigh:
            self.gameWon = True
            self.gameWonOrLost()
        self.updateImage()

    def Instructions(self):
        if self.showInstructions:
            self.textObject1.removeNode()
            self.showInstructions = False
        else:
            text = TextNode('eh')
            text.setCardColor(1, 1, 1, 1) # white
            text.setCardAsMargin(0, 0, 0, 0)
            text.setCardDecal(True)
            text.setText(self.text1)
            text.setAlign(TextNode.ALeft)
            text.setFrameColor(0, 0, 0, 1) # black, and not transparent
            text.setTextColor(0, 0, 0, 1) # black, and not transparent
            text.setFrameAsMargin(0, 0, 0, 0) #specifying margins for frame
            text.setShadow(0.05, 0.05)
            text.setShadowColor(0, 0, 0, 1)
            textNodePath = self.aspect2d.attachNewNode(text)
            self.textObject1 = textNodePath 
            textNodePath.setPos(-1.3,0,-0.5)
            textNodePath.setScale(0.06)
            self.showInstructions = True

    def timer(self, task):
        self.time -=1
        self.timerText.setText("time left: "+str(self.time)+ " seconds")
        if self.time==5:
            self.timerText.setFrameColor(1, 0, 0, 1) # red
            self.timerText.setTextColor(1, 0, 0, 1) # red
        if self.time ==0: 
            self.gameWonOrLost()
            return None # end task
        return task.again

    def move(self, task): #direction = (dx, dy, dz)

        if self.mode=="game" and not self.gameOver:
        
        # since I want to be able move left/right/forward/backwards relative to the current direction, 
        # I had to use cos and sin to change the x and y positions
            if self.keyMap["left"] > 0:
                self.cameraMove(-sin(self.angleRadians)*self.moveUnit,-cos(self.angleRadians)*self.moveUnit)
                # bc math lol
            if self.keyMap["right"] > 0:
                self.cameraMove(+sin(self.angleRadians)*self.moveUnit,+cos(self.angleRadians)*self.moveUnit)

            if self.keyMap["forward"] > 0:
                self.cameraMove(cos(self.angleRadians)*self.moveUnit,-sin(self.angleRadians)*self.moveUnit)

            if self.keyMap["backward"] > 0:
                self.cameraMove(-cos(self.angleRadians)*self.moveUnit,+sin(self.angleRadians)*self.moveUnit)

            if self.keyMap["camLeft"] > 0:
                self.CamOreintX += self.deltaAngle

            if self.keyMap["camRight"] > 0:
                self.CamOreintX -= self.deltaAngle

            if self.keyMap["camForward"] > 0:
                self.CamOreintY += self.deltaAngle

            if self.keyMap["camBackward"] > 0:
                self.CamOreintY -= self.deltaAngle

            #for debugging purposes!!!
            if self.keyMap["up"] > 0:
                self.camZpos += self.moveUnit
                if self.camZpos>= self.wallHeight*2: self.camZpos -= self.moveUnit

            if self.keyMap["down"] > 0:
                self.camZpos -= self.moveUnit
                if self.camZpos<= 1: self.camZpos += self.moveUnit
        if self.mode=="game" and self.gameOver:
            print("here")
            if self.keyMap["createNewGame"] >0:
                self.newGame()

        if self.keyMap["nextScreen"]>0 and self.mode == "splash":
            print(self.splashScreen)

        return task.cont

    def CameraView(self, task):
        spinConstant = 0 # makes camera  spin
        angleDegrees = task.time * spinConstant +  self.CamOreintX # spin about the x axis
        self.angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(0 * sin(self.angleRadians)+ self.camXpos, -0 * cos(self.angleRadians) + self.camYpos, self.camZpos)
        self.camera.setHpr( angleDegrees, self.CamOreintY, 0)
        if self.hasImageObject: self.imageObject.setHpr(0,0, angleDegrees)
        return Task.cont

app = MyApp(5,5)
app.run()
