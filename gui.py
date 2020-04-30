import datetime

import tkinter as tk
from tkinter import filedialog

from reportlab.platypus import SimpleDocTemplate, Image, Table
from reportlab.lib.pagesizes import letter

filename = ''
export = ''
selected = None
files = []


class GUI():
    root = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IMAGE2PDF")
        self.root.minsize(640, 400)
        self.root.maxsize(640, 400)

        self.labelFrame = tk.Label(self.root, text="IMAGE to PDF", font=("Arial", 36))
        self.labelFrame.grid(column=0, row=1, padx=170, pady=20)
        self.button()

        self.labelFrame2 = tk.Label(self.root, text="Images selected: {}".format(selected), font=("Arial", 16))
        self.labelFrame2.grid(column=0, row=5, padx=170, pady=100)

    def button(self):
        self.labelButton = tk.Button(self.root, text="Browse Files", command=self.fileDialog, font=("Arial", 16))
        self.labelButton.grid(column=0, row=3, padx=170, pady=3)
        self.labelButton2 = tk.Button(self.root, text="Convert", command=self.convert, font=("Arial", 20))
        self.labelButton2.grid(column=0, row=4, padx=170, pady=3)

    def fileDialog(self):
        global filename, export
        self.filename = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                                    filetype=(("png", "*.png"), ("All Files", "*.*")))
        filename = str(self.filename)
        export = filename[1:-2].replace("'", '')
        export = [x.strip() for x in export.split(',')]
        for i in export:
            files.append(i)
        print(files)
        self.calculateItems()

    def calculateItems(self):
        selected = len(files)
        self.labelFrame2.config(text="Images selected: {}".format(selected))
        print(selected)

    def convert(self):
        global filename, export, files
        exportToPDF()
        filename = ''
        export = ''
        selected = None
        files = []
        self.labelFrame2.config(text="Images selected: {}".format(selected))


def exportToPDF():
    now = datetime.datetime.now()
    title = now.strftime("%Y-%m-%d %H-%M-%S.pdf")
    pdf = SimpleDocTemplate(
        title,
        pagesize=letter
    )

    elements = []

    for i in files:
        im = Image(i, height=400, width=400)
        elements.append(im)

    pdf.build(elements)


if __name__ == '__main__':
    app = GUI()
    app.root.mainloop()
