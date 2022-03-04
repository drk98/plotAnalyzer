from tkinter import Tk, ttk, filedialog, Label, Canvas, PhotoImage, Button, RIGHT, Y
from plotAnalyzer.webpage import RESULTS_FILENAME
from os.path import exists, splitext, join
import tempfile
from requests import get
from pdf2image import convert_from_path
import webbrowser
from PIL import Image, ImageTk
from plotAnalyzer.tooltip import CreateToolTip


class ScrollableFrame(ttk.Frame):
    """
    Adapted from https://blog.teclado.com/tkinter-scrollable-frames/
    """

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        # canvas.grid()
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        # canvas.grid(row=0,column=0)
        # scrollbar.grid(row=0, column=1, rowspan=1)


def display(fname: str, type: str, url: str = None, folder: str = None):
    assert url is not None or folder is not None

    displayRoot = Tk()
    displayRoot.title("Wall")
    # displayRoot.geometry(f"1000x1000")

    frm = ScrollableFrame(displayRoot, padding=10)
    # frm = ttk.Frame(displayRoot, padding=10)
    frm.grid()
    # frm.pack()

    typeFiles = []
    thisResultsFileName = url.split('/')[-2] + "_" + RESULTS_FILENAME
    if exists(thisResultsFileName):
        with open(thisResultsFileName, 'r') as f:
            for line in f.readlines():
                if line.split(':')[0] == type:
                    typeFiles.append(line.split(':')[1].replace("\n", ""))
    else:
        displayRoot.destroy()
        return
    width = 0
    height = 0
    tempFiles = [None for _ in range(len(typeFiles))]
    for i, file in enumerate(typeFiles):
        if url is not None:
            r = get(url + file)
            if splitext(file)[1] == '.pdf':
                pdfTmpFile = tempfile.NamedTemporaryFile()

                pdfTmpFile.write(r.content)
                images = convert_from_path(pdfTmpFile.name)

                pdfTmpFile.close()

                tempFiles[i] = tempfile.NamedTemporaryFile(suffix='.png')
                images[0].save(tempFiles[i].name, 'PNG')


            else:
                tempFiles[i] = tempfile.NamedTemporaryFile(suffix=splitext(file)[1])
                tempFiles[i].write(r.content)

            image = Image.open(tempFiles[i].name)
        else:
            image = Image.open(join(folder, file))

        resize_image = image.resize((int(image.width / 3), int(image.height / 3)))
        width, height = (int(image.width), int(image.height))

        resize_image.save(tempFiles[i].name)
        # img = ImageTk.PhotoImage(resize_image)
        img = PhotoImage(master=frm, file=tempFiles[i].name)
        panel = Label(frm.scrollable_frame, image=img, cursor="hand2")
        # panel = Label(frm, image=img, cursor="hand2")
        panel.grid(row=int(i / 3), columnspan=1, column=i % 3)
        # if i % 3 == 0 and i != 0:
        #     panel.pack(side="bottom")
        # else:
        #     panel.pack(side="right")
        # panel.configure(image=img, width=img.width(), height=img.height())
        panel.image = img
        panel.bind('<Button-1>', lambda e: webbrowser.open_new_tab(url + file))

        CreateToolTip(panel, file)

    if url is not None:
        for tf in tempFiles:
            tf.close()

    displayRoot.geometry(f"{width + 10}x{height + 10}")
    frm.canvas.width = width - 15
    frm.canvas.height = height - 15
    frm.canvas.configure(width=width - 15, height=height - 15)
    displayRoot.mainloop()
