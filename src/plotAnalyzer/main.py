from tkinter import Tk, ttk, END, Text
import plotAnalyzer.analyzer as analyzer


def main():
    root = Tk()
    root.title("Folder Location")
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    urltxt = Text(frm,
                      height=1,
                      width=30)
    urltxt.grid(row=0)

    ttk.Button(frm, text="Open", command=lambda: analyzer.analyzerLoop(urltxt.get("1.0", END))).grid(column=0, row=1)

    root.mainloop()


if __name__ == '__main__':
    main()
