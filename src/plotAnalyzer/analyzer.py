from tkinter import Tk, ttk, filedialog, Label, Canvas, PhotoImage, Button
from os import listdir
from os.path import isfile, join, splitext, exists, isdir
import webpage
import analyzer

validExtensions = [".png"]
RESULTS_FILENAME = "figureResults.txt"


def selectFolder() -> str:
    return "/home/daniel/Desktop/weridast"
    return filedialog.askdirectory()


def getFiles(folder: str) -> list:
    doneFiles = []
    if exists(join(folder, RESULTS_FILENAME)):
        with open(join(folder, RESULTS_FILENAME), 'r') as f:
            for line in f.readlines():
                doneFiles.append(line.split(':')[1])

    files = [f.replace('\n', "") for f in listdir(folder) if isfile(join(folder, f.replace('\n', ""))) and
             splitext(f.replace('\n', ""))[1] in validExtensions and
             f.replace('\n', "") not in doneFiles]

    return files


def analyzerFiles(folder=None):
    if folder is None:
        folder = selectFolder()
    files = getFiles(folder)
    analyzerRoot = Tk()
    analyzerRoot.title('Analyzer')
    frm = ttk.Frame(analyzerRoot, padding=10)
    frm.grid()

    i = 0

    fnameLabel = Label(frm, text=join(folder, files[i]))
    fnameLabel.grid(row=0, column=0, columnspan=3)

    img = PhotoImage(master=frm, file=join(folder, files[i]))
    panel = Label(frm, image=img)
    panel.grid(row=1, columnspan=3)

    def nextImage():
        nonlocal i

        nextImg = PhotoImage(master=frm, file=join(folder, files[i]))
        panel.configure(image=nextImg, width=nextImg.width(), height=nextImg.height())
        panel.image = nextImg

        fnameLabel.configure(text=join(folder, files[i]))
        fnameLabel.text = join(folder, files[i])
        i += 1

    def goodImage():
        with open(join(folder, RESULTS_FILENAME), 'a+') as f:
            f.write(f"g:{files[i]}\n")
        nextImage()

    def badImage():
        with open(join(folder, RESULTS_FILENAME), 'a+') as f:
            f.write(f"b:{files[i]}\n")
        nextImage()

    def interestingImage():
        with open(join(folder, RESULTS_FILENAME), 'a+') as f:
            f.write(f"i:{files[i]}\n")
        nextImage()

    ttk.Button(frm, text="Good Figure", command=goodImage).grid(row=2, column=0)
    ttk.Button(frm, text="Interesting Figure", command=interestingImage).grid(row=2, column=1)
    ttk.Button(frm, text="Bad Figure", command=badImage).grid(row=2, column=2)

    def printGoodFigures():
        if exists(join(folder, RESULTS_FILENAME)):
            with open(join(folder, RESULTS_FILENAME), 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'g':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No good figures exist")

    def printBadFigures():
        if exists(join(folder, RESULTS_FILENAME)):
            with open(join(folder, RESULTS_FILENAME), 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'b':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No bad figures exist")

    def printInterestingFigures():
        if exists(join(folder, RESULTS_FILENAME)):
            with open(join(folder, RESULTS_FILENAME), 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'i':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No bad figures exist")

    ttk.Button(frm, text="Print all good figures", command=printGoodFigures).grid(row=3, column=0)
    ttk.Button(frm, text="Print all interesting figures", command=printInterestingFigures).grid(row=3, column=1)
    ttk.Button(frm, text="Print all bad figures", command=printBadFigures).grid(row=3, column=2)

    analyzerRoot.mainloop()


def analyzerWeb(url):
    url = url.replace("\n","")
    filesGen = webpage.getWebPageImages(url)

    analyzerRoot = Tk()
    analyzerRoot.title('Analyzer')
    frm = ttk.Frame(analyzerRoot, padding=10)
    frm.grid()

    try:
        file, name = next(filesGen)
    except StopIteration:
        print(f"No images found at URL: {url}")
        analyzerRoot.destroy()
        return
    fnameLabel = Label(frm, text=url + name)
    fnameLabel.grid(row=0, column=0, columnspan=3)

    img = PhotoImage(master=frm, file=file)
    panel = Label(frm, image=img)
    panel.grid(row=1, columnspan=3)

    def nextImage():
        nonlocal name
        nonlocal file
        try:
            file, name = next(filesGen)
        except StopIteration:
            print(f"All files in {url} have been categorized")
            return
        nextImg = PhotoImage(master=frm, file=file)
        panel.configure(image=nextImg, width=nextImg.width(), height=nextImg.height())
        panel.image = nextImg

        fnameLabel.configure(text=url + name)
        fnameLabel.text = url + name

    thisResultsFileName = url.split('/')[-2] + "_" + RESULTS_FILENAME

    def goodImage():
        with open(thisResultsFileName, 'a+') as f:
            f.write(f"g:{name}\n")
        nextImage()

    def badImage():
        with open(thisResultsFileName, 'a+') as f:
            f.write(f"b:{name}\n")
        nextImage()

    def interestingImage():
        with open(thisResultsFileName, 'a+') as f:
            f.write(f"i:{name}\n")
        nextImage()

    ttk.Button(frm, text="Good Figure", command=goodImage).grid(row=2, column=0)
    ttk.Button(frm, text="Interesting Figure", command=interestingImage).grid(row=2, column=1)
    ttk.Button(frm, text="Bad Figure", command=badImage).grid(row=2, column=2)

    def printGoodFigures():
        if exists(thisResultsFileName):
            with open(thisResultsFileName, 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'g':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No good figures exist")

    def printBadFigures():
        if exists(thisResultsFileName):
            with open(thisResultsFileName, 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'b':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No bad figures exist")

    def printInterestingFigures():
        if exists(thisResultsFileName):
            with open(thisResultsFileName, 'r') as f:
                for line in f.readlines():
                    if line.split(':')[0] == 'i':
                        print(line.split(':')[1].replace('\n', ""))
        else:
            print("No interesting figures exist")

    ttk.Button(frm, text="Print all good figures", command=printGoodFigures).grid(row=3, column=0)
    ttk.Button(frm, text="Print all interesting figures", command=printInterestingFigures).grid(row=3, column=1)
    ttk.Button(frm, text="Print all bad figures", command=printBadFigures).grid(row=3, column=2)

    analyzerRoot.mainloop()


def analyzerLoop(dest=None):
    if dest is None or isdir(dest):
        analyzerFiles(dest)
    else:
        analyzerWeb(dest)
