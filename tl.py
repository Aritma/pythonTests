#python v.3+
#Tiny locomotive - made just for fun
#Inspired by linux steam locomotive program
#
#USE: python3 tl.py <num of random wagons>

#---IMPORTS---

import curses
import time
import random
import sys
from curses import wrapper

#---VARIABLES---
#initial variables
#arguments read

framerate=20
if len(sys.argv) == 1:
    wagonNum=3
    treeNum=3
else:
    wagonNum=int(sys.argv[1])

#---GRAPHICS---
#each wagon have 4 lines
#locomotive is everytime the first

locomotives={
'locomotive1':["    __~ ~   _---_  ","   _||_^_^__|_..|  "," {|__..__..---||#  ","/##()-()_()-()()#>|"],
'locomotive2':["    __ ~ ~  _---_  ","   _||_^_^__|_..|  "," {|__..__..---||#  ","/##()_()-()_()()#>|"]
}

wagons={
'coal':["                ","  \``````````/  ","  |__________|  ","|<#()()##()()#>|"],
'passagers':["   __________   ","  |[] [] []| |  ","  |________|_|  ","|<#()()##()()#>|"],
'cistern':["   __-____-__   ","  /..........\  ","  \__________/  ","|<#()()##()()#>|"],
'wood':["                "," =|===|==|===|= "," =|===|==|===|= ","|<#()()##()()#>|"],
'empty':["                ","                ","  ____________  ","|<#()()##()()#>|"],
'goods':["  ____________  ","  |===|==|===|  ","  |___|__|___|  ","|<#()()##()()#>|"],
'tank':["                ","  ===/###\_     ","  _(O_O_O_O)__  ","|<#()()##()()#>|"]
}

trees={
    'pine':["   /\   ","  /  \  ","  /  \  "," / /\ \ "," /    \ ","/ /  \ \\","```||```","   ||   "],
    'oak':["  _--_  "," /    \ ","| |  ` |","\   |  /"," \_.._/ ","   \/   ","   ||   ","   ||   "],
    'top':["   /\   ","  |  |  "," | \  | "," |  / | ","  |  |  ","   \/   ","   ||   ","   ||   "],
    'bush':["        ","        ","        ","        ","   __   "," / ,  \ ","|    \ |"," \ /  / "]
}

#---NAME LISTS---
#lists with names from dictionaries for random choices

wagonNames=[]
for key in wagons.keys():
    wagonNames.append(key)

treeNames=[]
for key in trees.keys():
    treeNames.append(key)

#---GENERATE LIST OF POSITIONS---
#generate spectrum of numbers for tree positions

def getSpectrum(fieldSize,treeWidth,minDist,spawnChance):
    nums=[]
    actualPos=0
    size=fieldSize
    tWid=treeWidth
    minD=minDist
    if spawnChance>1:
        initChance=spawnChance
        chance=spawnChance
    else:
        initChance=2
        chance=2
    while True:
        if random.choice(range(1,chance)) == 1:
            nums.append(actualPos)
            actualPos+=(tWid+minD)
            chance=initChance
        else:
            actualPos+=1
            if chance>1:
                chance-=1
        if (actualPos+tWid)>=size:
            break
    return nums

#---TREE DICTIONARY---
#key: tree position
#value: tree name

treeDict={}
#generate trees
def generateTrees(positionList):
    for i in positionList:
        randomTree=random.choice(treeNames)
        treeDict[i]=trees[randomTree]

#---GENERATE TRAIN---
#generate train as lists of strings to draw line by line
#returns two variants of train for each state of locomotive and named list of wagons

def generateTrain(numOfwagons):
    train1=["","","",""]
    train2=["","","",""]
    wagonList=[]
    for num in range(0,numOfwagons+1):
        randomwagon=random.choice(wagonNames)
        for i in range(0,4):
            if num==0:
                train1[i]=train1[i]+locomotives['locomotive1'][i]
                train2[i]=train2[i]+locomotives['locomotive2'][i]
            else:
                train1[i]=train1[i]+wagons[randomwagon][i]
                train2[i]=train2[i]+wagons[randomwagon][i]
        if num>1:
            wagonList.append(randomwagon)
    return train1,train2,wagonList

#---TREE INSERT---
#insert trees in train strings
#take original train string and change characters where tree should be visible in the moment
#wraper for original train string

def insertTrees(string,line):
    newString=list(string)
    for key in treeDict:
        count=0
        for letter in treeDict[key][line-4]:
            if newString[key+count]==" ":
                newString[key+count]=letter
            count+=1
    return "".join(newString)

#---DRAW ON SCREEN---
#inicialization of screen
#printing of all values on screen

def drawIt(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    rail="="*width
    wagonStats=[]
    dist=0
    generateTrees(getSpectrum(width,len(trees['pine'][1]),5,random.randint(5,30)))
    trainList1,trainList2,wagonList=generateTrain(wagonNum)
    lines=[[
    (width*" ")+trainList1[0]+(width*" "),
    (width*" ")+trainList1[1]+(width*" "),
    (width*" ")+trainList1[2]+(width*" "),
    (width*" ")+trainList1[3]+(width*" ")],
    [
    (width*" ")+trainList2[0]+(width*" "),
    (width*" ")+trainList2[1]+(width*" "),
    (width*" ")+trainList2[2]+(width*" "),
    (width*" ")+trainList2[3]+(width*" ")]]
    framecount=0    
    variant=0
    #startY=int(height/2-4)
    startY=2
    while True:
        stdscr.refresh()
        for key in treeDict.keys():
            stdscr.addstr(startY,key,treeDict[key][0])
            stdscr.addstr(startY+1,key,treeDict[key][1])
            stdscr.addstr(startY+2,key,treeDict[key][2])
            stdscr.addstr(startY+3,key,treeDict[key][3])
        for i in range(0,4):
            stdscr.addstr(startY+4+i,0,insertTrees(lines[variant][i][0+dist:width+1+dist],i))
        stdscr.addstr(startY+8,0,rail)
        #---debug---
        #stdscr.addstr(startY+9,0,str(treeDict.keys()))
        
        stdscr.refresh()
        time.sleep(1/framerate)
        if dist>width+len(trainList1[0]):
            break
        else:
            dist+=1
            framecount+=1
            if framecount>=framerate/2:
                variant=0
                framecount=0
            elif framecount>framerate/4:
                variant=1
            else:
                variant=0

#---MAIN FUNCTION---

def main():
    wrapper(drawIt)

if __name__=="__main__":
    main()
