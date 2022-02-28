from tkinter import Tk, ttk, filedialog, Label, Canvas, PhotoImage, Button
from os import listdir
from os.path import isfile, join, splitext, exists, isdir
import plotAnalyzer.webpage as webpage

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


def printType(filePath: str, prefix: str, type: str):
    if exists(filePath):
        print(f"{type} Figures")
        print("===========================================")
        with open(filePath, 'r') as f:
            for line in f.readlines():
                if line.split(':')[0] == prefix:
                    print(line.split(':')[1].replace('\n', ""))
        print("===========================================")
    else:
        print(f"No \"{type}\" figures exist")


def writeImageResult(filePath: str, prefix: str, toWrite: str):
    with open(filePath, 'a+') as f:
        f.write(f"{prefix}:{toWrite}\n")


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

    def nextHelper():
        nonlocal i

        nextImg = PhotoImage(master=frm, file=join(folder, files[i]))
        panel.configure(image=nextImg, width=nextImg.width(), height=nextImg.height())
        panel.image = nextImg

        fnameLabel.configure(text=join(folder, files[i]))
        fnameLabel.text = join(folder, files[i])
        i += 1

    def nextImage(prefix: str):
        writeImageResult(join(folder, RESULTS_FILENAME), prefix, files[i])
        nextHelper()

    ttk.Button(frm, text="Good Figure", command=lambda: nextImage('g')).grid(row=2, column=0)
    ttk.Button(frm, text="Interesting Figure", command=lambda: nextImage('i')).grid(row=2, column=1)
    ttk.Button(frm, text="Bad Figure", command=lambda: nextImage('b')).grid(row=2, column=2)

    ttk.Button(frm, text="Print all good figures",
               command=lambda: printType(join(folder, RESULTS_FILENAME), 'g', 'Good')).grid(row=3, column=0)
    ttk.Button(frm, text="Print all interesting figures",
               command=lambda: printType(join(folder, RESULTS_FILENAME), 'i', 'Interesting')).grid(row=3, column=1)
    ttk.Button(frm, text="Print all bad figures",
               command=lambda: printType(join(folder, RESULTS_FILENAME), 'b', 'Bad')).grid(row=3, column=2)

    analyzerRoot.mainloop()


def analyzerWeb(url):
    url = url.replace("\n", "")
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

    def nextHelper():
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

    def nextImage(prefix: str):
        writeImageResult(thisResultsFileName, prefix, name)
        nextHelper()

    ttk.Button(frm, text="Good Figure", command=lambda: nextImage('g')).grid(row=2, column=0)
    ttk.Button(frm, text="Interesting Figure", command=lambda: nextImage('i')).grid(row=2, column=1)
    ttk.Button(frm, text="Bad Figure", command=lambda: nextImage('r')).grid(row=2, column=2)

    ttk.Button(frm, text="Print all good figures", command=lambda: printType(thisResultsFileName, 'g', 'Good')).grid(
        row=3, column=0)
    ttk.Button(frm, text="Print all interesting figures",
               command=lambda: printType(thisResultsFileName, 'i', 'Interesting')).grid(row=3, column=1)
    ttk.Button(frm, text="Print all bad figures", command=lambda: printType(thisResultsFileName, 'b', 'Bad')).grid(
        row=3, column=2)

    analyzerRoot.mainloop()


def analyzerLoop(dest=None):
    if dest is None or isdir(dest):
        analyzerFiles(dest)
    else:
        analyzerWeb(dest)
