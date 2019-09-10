from tkinter import *
from tkinter import ttk
import json

inputFile = sys.argv[1]

#SIZE
wWidth=800
wHeight=340
wXoffset=300
wYoffset=300
geometryString=str(wWidth)+'x'+str(wHeight)+'+'+str(wXoffset)+'+'+str(wYoffset)

#LOAD JSON DATA
with open(inputFile) as f:
    dataDict = json.loads(f.read())


#COLORS
bgcolor="#C0C0C0"
textcolor='black'


#WINDOW
window = Tk()
window.title("ECS QestionMaker 5000")
window.geometry(geometryString)
window.configure(background=bgcolor)
window.resizable(False, False)


#FRAME
fr = Frame(window,width=wWidth,height=50, background=bgcolor)
separator = Frame(window,width=wWidth,height=1, background='white')


#VARIABLES
infoLabelText="test text"
#IntVar need to be defined after instance creation to keep reference of parrent object
maxindex=IntVar()
maxindex.set(len(dataDict)-1)
index=IntVar()
aValid=IntVar()
bValid=IntVar()
cValid=IntVar()
dValid=IntVar()
questionTXTtext = StringVar()
aTXTtext = StringVar()
bTXTtext = StringVar()
cTXTtext = StringVar()
dTXTtext = StringVar()
explTXTtext = StringVar()
gotoTXTtext = StringVar()

#LABELS
infoLabel = Label(window, text="text text here blablabla", background=bgcolor, anchor='w', relief='sunken', padx=5)
def printInfo(textstring):
    infoLabel.config(text=textstring)

indexLBL = Label(fr, text=str(index.get())+"/"+str(maxindex.get()), background=bgcolor)
questionLBL = Label(window, text="Question", background=bgcolor)
aLBL = Label(window, text="A", background=bgcolor, anchor='e')
bLBL = Label(window, text="B", background=bgcolor, anchor='e')
cLBL = Label(window, text="C", background=bgcolor, anchor='e')
dLBL = Label(window, text="D", background=bgcolor, anchor='e')
explLBL = Label(window, text="Explanation", background=bgcolor, anchor='e')
tagsLBL = Label(window, text="Tags", background=bgcolor, anchor='e')
ansLBL = Label(window, text="ANS", background=bgcolor, anchor='e')


#TEXTFIELDS
questionTXT = Entry(window,background='white', width=70, textvariable=questionTXTtext)
aTXT = Entry(window,background='white', width=70, textvariable=aTXTtext)
bTXT = Entry(window,background='white', width=70, textvariable=bTXTtext)
cTXT = Entry(window,background='white', width=70, textvariable=cTXTtext)
dTXT = Entry(window,background='white', width=70, textvariable=dTXTtext)
explTXT = Entry(window,background='white', width=70, textvariable=explTXTtext)
gotoTXT = Entry(fr,background='white', width=5, textvariable=gotoTXTtext)


#CHECKBUTTONS
aCHCK = Checkbutton(window, variable=aValid, background=bgcolor)
bCHCK = Checkbutton(window, variable=bValid, background=bgcolor)
cCHCK = Checkbutton(window, variable=cValid, background=bgcolor)
dCHCK = Checkbutton(window, variable=dValid, background=bgcolor)


#COMBOBOX - DROPDOWN MENU
tags = [ "0: Empty",
         "1: Linux basics",
         "2: Data manipulation",
         "3: User Management and Permissions",
         "4: Proceses and Services",
         "5: Networks",
         "6: Advanced Linux",
         "7: Scripting and shell",
         "8: Databases",
         "9: Other"
         ]
tagList = ttk.Combobox(window, values=tags, width=50, background=bgcolor)


#BUTTONS
def clickSubmit():
    dataDict[index.get()]['text'] = questionTXTtext.get()
    dataDict[index.get()]['explanation'] = explTXTtext.get()

    dataDict[index.get()]['answers'][0]['text'] = aTXTtext.get()
    dataDict[index.get()]['answers'][1]['text'] = bTXTtext.get()
    dataDict[index.get()]['answers'][2]['text'] = cTXTtext.get()
    dataDict[index.get()]['answers'][3]['text'] = dTXTtext.get()

    dataDict[index.get()]['answers'][0]['correct'] = aValid.get()==1
    dataDict[index.get()]['answers'][1]['correct'] = bValid.get()==1
    dataDict[index.get()]['answers'][2]['correct'] = cValid.get()==1
    dataDict[index.get()]['answers'][3]['correct'] = dValid.get()==1

    dataDict[index.get()]['tag'] = tags.index(tagList.get())

    printInfo("Submited")

def clickNext():
    if index.get() < maxindex.get():
        index.set(index.get()+1)
        indexLBL.config(text=str(index.get())+"/"+str(maxindex.get()))
        loadDataToView()
        printInfo("Moved to question "+str(index.get()))

def clickPrev():
    if index.get() > 0:
        index.set(index.get()-1)
        indexLBL.config(text=str(index.get())+"/"+str(maxindex.get()))
        loadDataToView()
        printInfo("Moved to question "+str(index.get()))

def clickLast():
    index.set(maxindex.get())
    indexLBL.config(text=str(index.get())+"/"+str(maxindex.get()))
    loadDataToView()
    printInfo("Moved to question "+str(index.get()))

def clickNew():
    maxindex.set(maxindex.get()+1)
    index.set(maxindex.get())
    indexLBL.config(text=str(index.get())+"/"+str(maxindex.get()))
    clearView()
    emptyDict={
        'answers': [
            {'correct': False,'text': ''},
            {'correct': False, 'text': ''},
            {'correct': False, 'text': ''},
            {'correct': False, 'text': ''}],
        'text': '',
        'explain': '',
        'tag':0,
        }
    dataDict.append(emptyDict)
    loadDataToView()
    printInfo("New question created with index "+str(maxindex.get()))

def clickClear():
    clearView()
    printInfo("View cleared")

def clickReload():
    loadDataToView()
    printInfo("Data reloaded into view")

def clickSave():
    with open(inputFile,'w') as f:
        json.dump(dataDict, f, ensure_ascii=False)
    printInfo("Saved: " + inputFile)

def clickGoTo():
    if RepresentsInt(gotoTXTtext.get()):
        if int(gotoTXTtext.get()) >= 0 and int(gotoTXTtext.get()) <= maxindex.get():
            index.set(int(gotoTXTtext.get()))
            loadDataToView()
            indexLBL.config(text=str(index.get())+"/"+str(maxindex.get()))
            printInfo("Moved to question "+str(index.get()))
        else:
            gotoTXTtext.set("")
            printInfo("Value out of maximal range (" + str(maxindex.get()) + ")")
    else:
        gotoTXTtext.set("")
        printInfo("Invalid value, use number")


submitBTN = Button(window, text="Submit", command=clickSubmit, highlightbackground=bgcolor, foreground=textcolor)
prevBTN = Button(fr, text='<', command=clickPrev, highlightbackground=bgcolor, foreground=textcolor)
nextBTN = Button(fr, text='>', command=clickNext, highlightbackground=bgcolor, foreground=textcolor)
lastBTN = Button(fr, text='Last', command=clickLast, highlightbackground=bgcolor, foreground=textcolor)
newBTN = Button(fr, text='New', command=clickNew, highlightbackground=bgcolor, foreground=textcolor)
reloadBTN = Button(window, text="Reload", command=clickReload, highlightbackground=bgcolor, foreground=textcolor)
clearBTN = Button(window, text="Clear", command=clickClear, highlightbackground=bgcolor, foreground=textcolor)
saveBTN = Button(window, text="SAVE", command=clickSave, highlightbackground=bgcolor, foreground=textcolor)
gotoBTN = Button(fr, text="GoTo", command=clickGoTo, highlightbackground=bgcolor, foreground=textcolor)


#COMMON FUNCTIONS
def RepresentsInt(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False

def loadDataToView():
    if "text" in dataDict[index.get()]:
        questionTXTtext.set(dataDict[index.get()]['text'])
    else:
        questionTXTtext.set("")

    if "explanation" in dataDict[index.get()]:
        explTXTtext.set(dataDict[index.get()]['explanation'])
    else:
        explTXTtext.set("")

    aValid.set(0)
    bValid.set(0)
    cValid.set(0)
    dValid.set(0)

    if "answers" in dataDict[index.get()]:
        aTXTtext.set(dataDict[index.get()]['answers'][0]['text'])
        bTXTtext.set(dataDict[index.get()]['answers'][1]['text'])
        cTXTtext.set(dataDict[index.get()]['answers'][2]['text'])
        dTXTtext.set(dataDict[index.get()]['answers'][3]['text'])
        #TEST=BOOL and 1 or 0

        if 'correct' in dataDict[index.get()]['answers'][0]:
            aValid.set(dataDict[index.get()]['answers'][0]['correct'] and 1 or 0)
        if 'correct' in dataDict[index.get()]['answers'][1]:
            bValid.set(dataDict[index.get()]['answers'][1]['correct'] and 1 or 0)
        if 'correct' in dataDict[index.get()]['answers'][2]:
            cValid.set(dataDict[index.get()]['answers'][2]['correct'] and 1 or 0)
        if 'correct' in dataDict[index.get()]['answers'][3]:
            dValid.set(dataDict[index.get()]['answers'][3]['correct'] and 1 or 0)
    else:
        aTXTtext.set("")
        bTXTtext.set("")
        cTXTtext.set("")
        dTXTtext.set("")
    
    if 'tag' in dataDict[index.get()]:
        tagList.current(dataDict[index.get()]['tag'])
    else:
        tagList.current(0)

def clearView():
    questionTXTtext.set("")
    explTXTtext.set("")
    aValid.set(0)
    aTXTtext.set("")
    bValid.set(0)
    bTXTtext.set("")
    cValid.set(0)
    cTXTtext.set("")
    dValid.set(0)
    dTXTtext.set("")
    tagList.current(0)

#KEYBOARD SHOTRCUTS
def subAndSaveSHRT(event):
    clickSubmit()
    clickSave()

window.bind("<Control-s>", subAndSaveSHRT)

def clearSHRT(event):
    clickClear()

window.bind("<Control-l>",clearSHRT)

def newSHRT(event):
    clickNew()

window.bind("<Control-n>",newSHRT)

def nextSHRT(event):
    clickNext()

#window.bind("<Control-right>",nextSHRT)

def prevSHRT(event):
    clickPrev()

#window.bind("<Control-left>",prevSHRT)

def testKey(event):
    print(str(event.char))

#window.bind("<KeyRelease>", testKey)

#ABSOLUTE POSITIONING
infoLabel.place(x=0, y=wHeight-31, width=wWidth-1, height=30)

#fr.grid(row=0, sticky='ew')
fr.place(x=10,y=5)
prevBTN.grid(column=0,row=0)
indexLBL.grid(column=1,row=0)
nextBTN.grid(column=2,row=0)
Label(fr, text='     ', background=bgcolor).grid(row=0, column=3, sticky="w")
gotoTXT.grid(column=4,row=0)
gotoBTN.grid(column=5,row=0)
lastBTN.grid(column=6,row=0)
newBTN.grid(column=7,row=0)

yScale=30
yPosition=yScale+10

questionLBL.place(x=10,y=yPosition)
questionTXT.place(x=100,y=yPosition)
ansLBL.place(x=750,y=yPosition)
yPosition += yScale+10

aLBL.place(x=10,y=yPosition)
aTXT.place(x=100,y=yPosition)
aCHCK.place(x=750,y=yPosition)
yPosition += yScale

bLBL.place(x=10,y=yPosition)
bTXT.place(x=100,y=yPosition)
bCHCK.place(x=750,y=yPosition)
yPosition += yScale

cLBL.place(x=10,y=yPosition)
cTXT.place(x=100,y=yPosition)
cCHCK.place(x=750,y=yPosition)
yPosition += yScale

dLBL.place(x=10,y=yPosition)
dTXT.place(x=100,y=yPosition)
dCHCK.place(x=750,y=yPosition)
yPosition += yScale+10

explLBL.place(x=10,y=yPosition)
explTXT.place(x=100,y=yPosition)
yPosition += yScale

tagsLBL.place(x=10,y=yPosition)
tagList.place(x=100,y=yPosition)
yPosition += yScale+10

submitBTN.place(x=100,y=yPosition)
reloadBTN.place(x=200,y=yPosition)
clearBTN.place(x=300,y=yPosition)
saveBTN.place(x=700,y=yPosition)
yPosition += yScale

loadDataToView()
window.mainloop()