import os, tkinter, re

# Constants
illegalFileNameCharacters = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/', '$', ':', ';', '@', '+', '`', '|', '=']

# Functions
def rename_files_in_dir(dir, top):
    global selectedFiles, newFileNames
    for i in range(len(selectedFiles)):
        try:
            os.rename(F"{dir}\\{selectedFiles[i]}", F"{dir}\\{newFileNames[i]}")
        except FileExistsError:
            pass

    top.destroy()
    renameInput.delete(0, tkinter.END)
    inputFiles.delete(0, tkinter.END)
    outputFiles.delete(0, tkinter.END)
    selectedFiles = []
    newFileNames = []
    update_rename_preview()

def next_dir():
    global currentDir, directories, nonDirectories, selectedFiles, newFileNames
    if len(dirSelectBox.curselection()) > 0:
        currentDir = currentDir+directories[dirSelectBox.curselection()[0]]+"\\"
    else:
        print("NOTHING SELECTED")
        return

    dirSelectBox.delete(0, tkinter.END)
    inputFiles.delete(0, tkinter.END)
    outputFiles.delete(0, tkinter.END)
    selectedFiles = []
    newFileNames = []
    directories = []
    nonDirectories = []
    
    update_rename_preview()
    for i in os.listdir(currentDir):
        if os.path.isdir(currentDir+"\\"+i):
            directories.append(i)
            dirSelectBox.insert(tkinter.END, i)
        else:
            nonDirectories.append(i)
            inputFiles.insert(tkinter.END, i)

    if len(currentDir) > 25:
        dirIndicator.configure(text=F"{currentDir[:9]}...{currentDir[-13:]}")
    else:
        dirIndicator.configure(text=currentDir)

def previous_dir():
    global currentDir, directories, nonDirectories, selectedFiles, newFileNames
    newDirName = currentDir.split("\\")
    update_rename_preview()
    if len(newDirName) != 2:
        newDirName.pop()
        newDirName.pop()
        currentDir = "\\".join(newDirName)+"\\"
    else:
        currentDir = "\\".join(newDirName)
    
    dirSelectBox.delete(0, tkinter.END)
    inputFiles.delete(0, tkinter.END)
    outputFiles.delete(0, tkinter.END)
    selectedFiles = []
    newFileNames = []
    directories = []
    nonDirectories = []
    for i in os.listdir(currentDir):
        if os.path.isdir(currentDir+"\\"+i):
            directories.append(i)
            dirSelectBox.insert(tkinter.END, i)
        else:
            nonDirectories.append(i)
            inputFiles.insert(tkinter.END, i)

    if len(currentDir) > 25:
        dirIndicator.configure(text=F"{currentDir[:9]}...{currentDir[-13:]}")
    else:
        dirIndicator.configure(text=currentDir)

def scroll_files(*args):
    inputFiles.yview(*args)
    outputFiles.yview(*args)

def renameInputFunc(P):
    validInput = False
    if (len(P) == 0 or len(P) <= 128) and not (any(item in list(char for char in P+" ") for item in illegalFileNameCharacters)):
        validInput = True

    return validInput

def open_popup():
    top = tkinter.Toplevel(root)
    top.geometry("500x125")
    top.title("CONFIRM RENAME")
    top.resizable(False, False)

    buttonFrame = tkinter.Frame(top)
    tkinter.Button(buttonFrame, text="Confirm", font="Helvetica 10 bold", width=20, command=lambda x=None: rename_files_in_dir(currentDir, top)).pack(side="left", padx=5)
    tkinter.Button(buttonFrame, text="Cancel", font="Helvetica 10", width=20, command=top.destroy).pack(side="left", padx=5)
    tkinter.Label(top, text= "Confirm Rename? This action cannot be undone!", font=('Helvetica 12 bold')).pack(side="top", pady=10)
    buttonFrame.pack(side="top", pady=10)

def update_rename_preview(*args):
    global selectedFiles, newFileNames
    if len(inputFiles.curselection()) > 0:
        selectedFiles = []
        for index in inputFiles.curselection():
            selectedFiles.append(nonDirectories[index])

    newFileNames = []

    for file in enumerate(selectedFiles):
        newFileNames.append(F'{renameInput.get()}_{str(file[0]+1)}.{file[1].split(".")[-1]}')
    
    outputFiles.configure(state='normal')
    outputFiles.delete('1.0', tkinter.END)
    if len(renameInput.get()) > 0 and len(selectedFiles) > 0:
        renameButton['state'] = 'normal'
        outputFiles.insert('1.0', '\n'.join(newFileNames))
    else:
        renameButton['state'] = 'disabled'
    outputFiles.configure(state='disabled')

# Initialize Display
root = tkinter.Tk()
root.title("Bulknamer")
root.geometry('900x600')
root.resizable(False, False)

# Variables
currentDir = os.path.abspath(os.sep)
print(currentDir)
navigating = False
nonDirectories = []
directories = []
vcmd = (root.register(renameInputFunc), '%P')
selectedFiles = []
newFileNames = []

# Create GUI Elements
title = tkinter.Label(root, text="Bulknamer").pack(padx=10, pady=10)
fileList = tkinter.LabelFrame(root)

fileScroll = tkinter.Scrollbar(fileList)
fileScroll.config(command=scroll_files)

inputFileContainer = tkinter.LabelFrame(fileList, text="Input Files", padx=10, pady=10, height=300)
inputFiles = tkinter.Listbox(inputFileContainer, selectmode=tkinter.MULTIPLE, width=50, height=15, yscrollcommand=fileScroll.set)
inputFiles.configure(exportselection=False)

outputFileContainer = tkinter.LabelFrame(fileList, text="Renamed Files", padx=10, pady=10, height=300)
outputFiles = tkinter.Text(outputFileContainer, state="disabled", width=40, height=15, yscrollcommand=fileScroll.set)
renameAndDirContainer = tkinter.LabelFrame(root)

dirSection = tkinter.LabelFrame(renameAndDirContainer, text="Directory Selection", pady=10, padx=10, height=300)

dirList = tkinter.Frame(dirSection)
dirIndicator = tkinter.Label(dirList, text=F"{currentDir}")
dirBoxScroll = tkinter.Scrollbar(dirList)
dirSelectBox = tkinter.Listbox(dirList, selectmode=tkinter.SINGLE, yscrollcommand=dirBoxScroll.set)
dirBoxScroll.config(command=dirSelectBox.yview)

navBtns = tkinter.Frame(dirSection)
fwBtn = tkinter.Button(navBtns, text="CONFIRM", command=next_dir)
BkBtn = tkinter.Button(navBtns, text="BACK", command=previous_dir)

renameSection = tkinter.LabelFrame(renameAndDirContainer, text="Rename")
renameTitle = tkinter.Label(renameSection, text="Enter new file names")

renameInput = tkinter.Entry(renameSection, validate="key", validatecommand=vcmd)
renameOptions = tkinter.LabelFrame(renameSection, text="Confirmation")
renameButton = tkinter.Button(renameOptions, text="CONFIRM RENAME", command=open_popup)
renameButton['state'] = 'disabled'

# Place GUI Elements
fileList.pack()
inputFileContainer.pack(side="left", fill="x")
inputFiles.pack(side="left", fill="x")
fileScroll.pack(side="left", fill="y")

outputFileContainer.pack(side="left", fill="x")
outputFiles.pack(side="left", fill="x")
renameAndDirContainer.pack()

dirSection.pack(side="left", padx=10)
dirIndicator.pack()
dirSelectBox.pack(side="left")
dirBoxScroll.pack(side="left", fill="y")
dirList.pack()

BkBtn.pack(side="left")
fwBtn.pack(side="left")
navBtns.pack(side="top")

renameSection.pack(side="left", padx=10)

renameTitle.pack()
renameButton.pack()

renameInput.bind("<KeyRelease>", update_rename_preview)

renameInput.pack()
renameOptions.pack()

# Start program
for i in os.listdir(currentDir):
    directories.append(i)
    dirSelectBox.insert(tkinter.END, i)

for i in os.listdir(currentDir):
    if os.path.isdir(currentDir+"\\"+i):
        directories.append(i)
        dirSelectBox.insert(tkinter.END, i)
    else:
        nonDirectories.append(i)
        inputFiles.insert(tkinter.END, i)

root.mainloop()