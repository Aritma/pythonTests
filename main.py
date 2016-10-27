from graphics import *
import time

"""
register_cell function register cells in cellDict
*args takes cell position (x,y)
No return value
"""
def register_cell(cellDict,*args):
    for cell in args:
        cellDict[cell]=True

"""
new_window function create game window and set its background
Return created window object
"""
def new_window(title,width,height):
    _window=GraphWin(title,width,height,False)
    _window.setBackground("grey")

    return _window

"""
check_life function control cell life conditions and remove or create cells
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
def check_life(cellDict):
    aliveTab={}
    for cell in cellDict:
        neib=get_count(cellDict,cell[0],cell[1])
        if neib in (2,3):
            register_cell(aliveTab,(cell[0],cell[1]))
            
    emptyCells=get_empty(cellDict)
    for cell in emptyCells:
        neib=get_count(cellDict,cell[0],cell[1])
        if neib==3:
            register_cell(aliveTab,(cell[0],cell[1]))

    cellDict.clear()
    cellDict.update(aliveTab)


"""
get_empty function check all existing cells and make list of adjescent empty positions
Return dictionary of empty positions
"""
def get_empty(cellDict):
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
get_count count amount of living adjescent cells around target position
do not count itselfs
Return count of cells
"""
def get_count(cellDict,x,y):
    _count=0
    for a in [-1,0,1]:
        for b in [-1,0,1]:
            #if not (a==0 and b==0):
            if not (a,b)==(0,0):
                key=x+a,y+b
                if key in cellDict:
                    _count+=1

    return _count


"""
draw_cells function draw existing cells in generation in window
before drawing new cell, function check last drawn cell and undraw those that do no exist in next generation
after removing invalid cells, clears draw tab
create Rectangle object for every existing cell and save it in drawn dictionary
draw all Rectangles in drawn dict
No return value
"""
def draw_cells(cellDict,scale,size,ofsX,ofsY,window,drawn):
    for i in drawn:
        drawn[i].undraw()
    drawn.clear()
    
    offsetX=window.width/2+ofsX
    offsetY=window.height/2+ofsY
    
    for cell in cellDict:
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
listen_key function check if any key of predefined list was pressed
called twice in code to increase chance of catching key event
Return pressed key value
"""
def listen_key(win):
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
    cellDict={}

    win=new_window("Game of life - test",800,600)

    """Infinite creation pattern ◘◘◘◘◘◘◘◘.◘◘◘◘◘...◘◘◘......◘◘◘◘◘◘◘.◘◘◘◘◘ """
    register_cell(cellDict,(-14,0),(-13,0),(-12,0),(-11,0))
    register_cell(cellDict,(-10,0),(-9,0),(-8,0),(-7,0))
    register_cell(cellDict,(-5,0),(-4,0),(-3,0),(-2,0),(-1,0))
    register_cell(cellDict,(3,0),(4,0),(5,0))
    register_cell(cellDict,(12,0),(13,0),(14,0),(15,0))
    register_cell(cellDict,(16,0),(17,0),(18,0))
    register_cell(cellDict,(20,0),(21,0),(22,0),(23,0),(24,0))

    while True:

        #draw only every 10th (or other number) generation, uncoment to use
        #if repeat%10==0:
        draw_cells(cellDict,scale,10,ofsX*(scale*10),ofsY*(scale*10),win,drawn)
        win.redraw()

        keyUsed=listen_key(win)

        check_life(cellDict)

        keyUsed=listen_key(win)

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
