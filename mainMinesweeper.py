from cmu_graphics import *

from cmu_graphics import *
import random
import math

def onAppStart(app):
    
    #url for bomb image
    app.url = "https://play-lh.googleusercontent.com/pHMh7lpyML_1ItqaUnxc3pBzFymwyuv3f_C6Uqq8R5EhBA6qe7dvHhJF_SNAKkvIo2I"
    
    #url for tiles
    app.url2 = 'https://lh3.googleusercontent.com/61Nza9pnCkEGDH42MiFB4khcy796SpdmcMASHFZviSkGpWm7AczBVfs7lAp5pSA5WMCJSPwuWOR_pQPjeeJP'
    
    #sets number of rows and columns --> fully customizable, though tile counts higher than 100 will start to lag
    app.rows = 10
    app.cols = 10
    
    #properly sizes cells depending on rows and columns so that all tiles are squares
    if app.cols > app.rows:
        app.boardWidth = 400
        app.boardHeight = 400 * (app.rows / app.cols)
    else:
        app.boardWidth = 400 * (app.cols / app.rows)
        app.boardHeight = 400
        
    app.boardLeft = 0
    app.boardTop = 0
    app.cellBorderWidth = 1
    app.selection = None
    app.game = None
    
    #creats two identical 2d lists, one for the position of the bombs and values of each square, and the other to determine if a cell has been clicked
    app.minesweeper = [[None for i in range(app.cols)] for i in range(app.rows)]
    app.clicked = [[None for i in range(app.cols)] for i in range(app.rows)]
    
#function that ends the game, and reveals all bombs
def endgame(app):
    app.game = 'over'
    
    #sets each bomb tile to clicked so that they are revealed
    for row in range(app.rows):
        for col in range(app.cols):
            if app.minesweeper[row][col] == 'x':
                app.clicked[row][col] = 1
            
#function to place bombs and assign values of each square            
def assignSquare(app):
    count = 0
    
    #goes through empty 2d list app.minesweeper
    for row in range(app.rows):
        for col in range(app.cols):
            
            #randomly assigns a value to each square. 25% chance it is a bomb, and bombs cannot make 
            #up more than 20% of squares, nor can there be bombs on the first square clicked
            #bomb tiles have a value of 'x' in the list
            if random.randrange(0, 100) <= 25 and count < .20 * app.rows * app.cols and app.clicked[row][col]!= 1 and app.minesweeper[row][col]!=0:
                count+= 1
                            
                
                app.minesweeper[row][col] = 'x'
            else:
                app.minesweeper[row][col] = 0
    
    #adds a tuple of the row and col of every bomb to the list bombPos            
    bombPos = []
    for row in range(app.rows):
        
        for col in range(app.cols):
            
            if app.minesweeper[row][col] == 'x':
                bombPos.append((row,col))
    
    #for every bomb, it adds 1 to the value of every neighboring cell
    indexArray = [-1, 0, 1]
    for bomb in bombPos:
        row = bomb[0]
        col = bomb[1]
        
        for i in indexArray:
            
            for x in indexArray:
                
                try:
                    if app.minesweeper[row+i][col+x] != 'x' and row+i>-1 and col+x>-1:
                        app.minesweeper[row+i][col+x] += 1
                except:
                    continue
            
                

    
def redrawAll(app):
    drawBoard(app)
    
#function to clear out spaces and check neighboring cells
#used to clear out large spaces of 'zeroes' (cells that arent neighboring any bombs) with one click
def searchSurrounding(row, col, app):
    indexArray = [-1, 0, 1]
    
    new = []
    
    #used to iterate through all 8 neighboring cells
    for i in indexArray:
        for x in indexArray:
            
            #try function is used to prevent out of range errors
            try:
                #checks if any neighboring cells are 0 (purposefully does not include wraparounds)
                if app.minesweeper[row+i][col+x] == 0 and app.clicked[row+i][col+x] != 1 and col+x > -1 and row + i > -1:
                    app.clicked[row+i][col+x] = 1
                    
                    #adds any neighboring zeroes found to the list new
                    new.append((row+i,col+x))
                    
            except:
                continue
            
    #recursively calls the same function for all additional zeroes added        
    if len(new) > 0:
        for i in new:
            rox,cox = i
            if app.clicked[rox][cox] == 1:
                searchSurrounding(rox,cox, app)
    
    #iterates through each cell in the list            
    for k in range(app.rows):
        for j in range(app.cols):
            
            #checks the neighboring cells of every clicked cell
            if app.clicked[k][j] == 1:
                for i in indexArray:
                    for x in indexArray:
                        
                        
                        try:
                            #marks all the cells that are neighboring zeroes as clicked
                            if app.minesweeper[row+i][col+x] != 'x' and app.clicked[row+i][col+x] != 1 and col+x > -1 and row + i > -1:
                                app.clicked[row+i][col+x] = 1
                        except:
                            continue
            
        
            
def drawBoard(app):
    #calls drawCell for every cell
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

#function that draws each individual cell
def drawCell(app, row, col):
    
    #calls helper functions to get position and dimensions of cell
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
        
    #draws the background tiles
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, border='grey',
        borderWidth=app.cellBorderWidth, fill = 'lightgrey')
    
    #places the minesweeper tile image over any unclicked cells
    if app.clicked[row][col] != 1:   
        imageWidth, imageHeight = getImageSize(app.url2)
        drawImage(app.url2, cellLeft, cellTop, width = cellWidth, height = cellHeight)
        
    #sets the colors of the cell labels
    if app.minesweeper[row][col] == 1:
        fontColor = 'blue'
    elif app.minesweeper[row][col] == 2:
        fontColor = 'green'
    elif app.minesweeper[row][col] == 3:
        fontColor = 'red'
    elif app.minesweeper[row][col] == 4:
        fontColor = 'purple'
    else:
        fontColor = 'maroon'
        
    #draws the labels of any clicked tiles (zeroes are displayed as blank cells)
    if app.minesweeper[row][col] != 0 and app.minesweeper[0][0] != None and app.clicked[row][col] == 1:
        drawLabel(app.minesweeper[row][col], cellLeft+cellWidth/2, cellTop+cellHeight/2, font='monospace', fill = fontColor, bold = True, size = cellHeight * .7)
    
    
    #Below code creates a red 'selection' square beneath your mouse, but is commented out due to lag
    # if (row,col) == app.selection and app.minesweeper[row][col] != None:
    #     drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = 'red', opacity = 75)
        
    #places the bomb image on any bomb tiles if the game is ended
    if app.game == 'over' and app.minesweeper[row][col] == 'x':
        imageWidth, imageHeight = getImageSize(app.url)

        drawImage(app.url, cellLeft, cellTop, width = cellWidth, height = cellHeight)
    
#helper function that uses x and y position to return the row and col of a cell             
def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
      
#function that returns the top-left x and y value based on row and col
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

#function that determines the cell size based on the width and height of the board, as well as the number of rows and cols
def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    
#sets the selected cell using the mouses x and y position
def onMouseMove(app, mouseX, mouseY):
    if app.game != 'over':
        selectedCell = getCell(app, mouseX, mouseY)
        app.selection = selectedCell
        
def onMousePress(app, mouseX, mouseY):
    
    #sets the current square to clicked
    row,col = app.selection
    app.clicked[row][col] = 1
    
    #ends the game if a bomb is clicked
    if app.minesweeper[row][col] == 'x':
        endgame(app)
        
    #this assigns the tiles if it is the first click, that way the player always starts with a 0
    if app.minesweeper[0][0] == None:
        indexArray = [-1,0,1]
        for i in indexArray:
                    
                    for x in indexArray:
                        app.minesweeper[row+i][col+x] = 0
        assignSquare(app)
        
    #if the player clicks a zero, searchSurrounding is called to clear out all adjacent zeroes
    if app.minesweeper[row][col] == 0:
        searchSurrounding(row, col, app)

def main():
    runApp()

main()