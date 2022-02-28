from tkinter import Tk, ttk, filedialog, Label, Canvas, PhotoImage, Button
import tempfile
from os import listdir
from os.path import isfile, join, splitext, exists

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


def analyzerLoop():
    folder = selectFolder()
    files = getFiles(folder)

    analyzerRoot = Tk()
    frm = ttk.Frame(analyzerRoot, padding=10)
    frm.grid()

    i = 0

    fnameLabel = Label(frm, text=join(folder, files[i]))
    fnameLabel.grid(row=0, column=0, columnspan=2)

    img = PhotoImage(master=frm, file=join(folder, files[i]))
    panel = Label(frm, image=img)
    panel.grid(row=1, columnspan=2)

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

    ttk.Button(frm, text="Good Figure", command=goodImage).grid(row=2, column=0)
    ttk.Button(frm, text="Bad Figure", command=badImage).grid(row=2, column=1)

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

    ttk.Button(frm, text="Print all good figures", command=printGoodFigures).grid(row=3, column=0)
    ttk.Button(frm, text="Print all bad figures", command=printBadFigures).grid(row=3, column=1)

    analyzerRoot.mainloop()


def main():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    ttk.Button(frm, text="Open Folder", command=analyzerLoop).grid(column=0, row=0)

    root.mainloop()


if __name__ == '__main__':
    main()
