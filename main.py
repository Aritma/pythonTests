from graphics import *
import time

"""
Dict class to encapsulate main working dictionary
"""
class Dict:

    def __init__(self):
        self.dict={}

    def getDict(self):
        return self.dict

    def setDict(self,newDict):
        self.dict.clear()
        self.dict=newDict
        return self.dict

    def clear(self):
        self.dict.clear()


"""
Cell class keep information of single cell values
"""
class Cell:

    def __init__(self,x=0,y=0,size=10):
        self.x=x
        self.y=y
        self.size=size
        
    def getPosition(self):
        return self.x,self.y


"""
newCell function register cells in cellDict
*args takes Cell object constructors
No return value
"""
def newCell(cellDict,*args):
    for cell in args:
        cellDict[cell.getPosition()]=cell

"""
newWindow function create game window and set its background
Return created window object
"""
def newWindow(title,width,height):
    _window=GraphWin(title,width,height,False)
    _window.setBackground("grey")

    return _window

"""
checkLife function control cell life conditions and remove or create cells
Conditions(source: https://en.wikipedia.org/wiki/Conway's_Game_of_Life):
 - Any live cell with fewer than two live neighbours dies, as if caused by under-population.
 - Any live cell with two or three live neighbours lives on to the next generation.
 - Any live cell with more than three live neighbours dies, as if by over-population.
 - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
---------------------------
read all exisiting cells and set all valid cells in aliveTab
read all empty cells around existing structure and for valid positions create new cells in aliveTab
pass aliveTab into next generation
No return value
"""
def checkLife(cellDict,dictParrent):
    aliveTab={}
    for cell in cellDict:
        neib=getCount(cellDict,cell[0],cell[1])
        if neib==2 or neib==3:
            newCell(aliveTab,Cell(cell[0],cell[1]))
            
    emptyCells=getEmpty(cellDict)
    for cell in emptyCells:
        neib=getCount(cellDict,cell[0],cell[1])
        if neib==3:
            newCell(aliveTab,Cell(cell[0],cell[1]))

    dictParrent.setDict(aliveTab)


"""
getEmpty function check all existing cells and make list of adjescent empty positions
Return dictionary of empty positions
"""
def getEmpty(cellDict):
    _emptyCells={}
    for cell in cellDict:
        x=cell[0]
        y=cell[1]
        
        for a in [-1,0,1]:
            for b in [-1,0,1]:
                key=x+a,y+b
                if not key in cellDict:
                    _emptyCells[key]="empty"

    return _emptyCells

"""
getCount count amount of living adjescent cells around target position
do not count itselfs
Return count of cells
"""
def getCount(cellDict,x,y):
    _count=0
    for a in [-1,0,1]:
        for b in [-1,0,1]:
            if not (a==0 and b==0):
                key=x+a,y+b
                if key in cellDict:
                    _count+=1

    return _count


"""
drawCells function draw existing cells in generation in window
before drawing new cell, function check last drawn cell and undraw those that do no exist in next generation
after removing invalid cells, clears draw tab
create Rectangle object for every existing cell and save it in drawn dictionary
draw all Rectangles in drawn dict
No return value
"""
def drawCells(cellDict,scale,ofsX,ofsY,window,drawn):
    for i in drawn:
        drawn[i].undraw()
    drawn.clear()
    
    offsetX=window.width/2+ofsX
    offsetY=window.height/2+ofsY
    
    for cell in cellDict:
        size=cellDict[cell].size
        cx1=cell[0]*size
        cy1=cell[1]*size
        cx2=cx1+size
        cy2=cy1+size
        
        c=Rectangle(Point(cx1*scale+offsetX,cy1*scale+offsetY),Point(cx2*scale+offsetX,cy2*scale+offsetY))
        c.setFill("white")
        drawn[cell]=c
    
    #remove items from window to draw new one (test)
    window.items=[]
    
    for i in drawn:
        drawn[i].draw(window)


"""
listenKey function check if any key of predefined list was pressed
called twice in code to increase chance of catching key event
Return pressed key value
"""
def listenKey(win):
    for _i in ("q","w","Right","Left","Up","Down"):
        if win.lastKey==_i:
            return _i


"""
Main function
"""
def main():
    #initial vars
    scale=1
    ofsX=0
    ofsY=0
    repeat=0
    keyUsed=""
    drawn={}
    d=Dict()
    cellDict=d.getDict()

    win=newWindow("Game of life - test",800,600)

    """Infinite creation pattern ◘◘◘◘◘◘◘◘.◘◘◘◘◘...◘◘◘......◘◘◘◘◘◘◘.◘◘◘◘◘ """
    newCell(cellDict,Cell(-14,0),Cell(-13,0),Cell(-12,0),Cell(-11,0))
    newCell(cellDict,Cell(-10,0),Cell(-9,0),Cell(-8,0),Cell(-7,0))
    newCell(cellDict,Cell(-5,0),Cell(-4,0),Cell(-3,0),Cell(-2,0),Cell(-1,0))
    newCell(cellDict,Cell(3,0),Cell(4,0),Cell(5,0))
    newCell(cellDict,Cell(12,0),Cell(13,0),Cell(14,0),Cell(15,0))
    newCell(cellDict,Cell(16,0),Cell(17,0),Cell(18,0))
    newCell(cellDict,Cell(20,0),Cell(21,0),Cell(22,0),Cell(23,0),Cell(24,0))

    while True:
        cellDict=d.getDict()

        #draw only every 10th (or other number) generation, uncoment to use
        #if repeat%10==0:
        drawCells(cellDict,scale,ofsX*(scale*10),ofsY*(scale*10),win,drawn)
        win.redraw()

        keyUsed=listenKey(win)

        checkLife(cellDict,d)

        keyUsed=listenKey(win)

        #time pause between next generation
        #problems with key event handling while using sleep
        #time.sleep(1)


        #key listener effects (predefined)
        # q = -zoom; w = +zoom; Arrows to move screen using offset
        if keyUsed=="q":
            scale=scale/2
            ofsX=0
            ofsY=0
            keyUsed=""
        elif keyUsed=="w":
            scale=scale*2
            ofsX=0
            ofsY=0
            keyUsed=""
        elif keyUsed=="Right":
            ofsX-=10
            keyUsed=""
        elif keyUsed=="Left":
            ofsX+=10
            keyUsed=""
        elif keyUsed=="Up":
            ofsY+=10
            keyUsed=""
        elif keyUsed=="Down":
            ofsY-=10
            keyUsed=""

        #terminate key
        if win.checkKey()=="Escape":
            print("Terminated")
            print("Generation: "+str(repeat))
            print("<Press Escape to exit>")
            
            break
        
        repeat+=1
    
    #exit key
    if win.checkKey()=="Escape":
        print("EXIT")
        win.close()


main()
