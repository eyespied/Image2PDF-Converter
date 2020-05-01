__author__ = "James Clark"
__version__ = "1.0.2"

# Import libraries
import datetime

import tkinter as tk
from tkinter import filedialog

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Initialize variables
filename = ''
export = ''
selected = None
files = []


# Displays GUI and runs everything else.
class GUI():
    root = None

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IMAGE 2 PDF")
        self.root.iconbitmap("C:/Users/James/Documents/GitHub/Image2PDFConverter/icon.ico")
        self.root.minsize(640, 400)
        self.root.maxsize(640, 400)
        self.root.configure(bg='#53687E')

        self.labelFrame = tk.Label(self.root, text="IMAGE 2 PDF", font=("Helvetica", 36), fg='#FFFFFF', bg='#53687E')
        self.labelFrame.grid(column=0, row=1, padx=165, pady=20)
        self.button()

        self.labelFrame2 = tk.Label(self.root, text="Images selected: {}".format(selected), font=("Helvetica", 16),
                                    fg='#FFFFFF', bg='#53687E')
        self.labelFrame2.grid(column=0, row=4, padx=165, pady=0)

    def button(self):
        self.labelButton = tk.Button(self.root, text="Browse Files", command=self.fileDialog, font=("Helvetica", 12))
        self.labelButton.grid(column=0, row=3, padx=165, pady=15)
        self.labelButton2 = tk.Button(self.root, text="Convert", command=self.convert, font=("Helvetica", 20), width=15)
        self.labelButton2.grid(column=0, row=5, padx=165, pady=100)

    # Filedialog to select images
    def fileDialog(self):
        global filename, export
        self.filename = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                                    filetypes=[("All Files", "*.*"), (".PNG", "*.png"),
                                                               (".JPEG", "*.jpeg"), (".BMP", "*.bmp"),
                                                               (".SVG", "*.svg")])
        filename = str(self.filename)
        export = filename[1:-2].replace("'", '')
        export = [x.strip() for x in export.split(',')]
        for i in export:
            files.append(i)
        self.calculateItems()

    # Updates text
    def calculateItems(self):
        selected = len(files)
        self.labelFrame2.config(text="Images selected: {}".format(selected))

    def convertLabel(self):
        self.labelFrame2.config(text="Converting...")

    # Executes exportToPDF function and resets variables back to start state.
    def convert(self):
        global filename, export, files, selected
        self.convertLabel()
        self.exportToPDF()
        filename = ''
        export = ''
        selected = None
        files = []

    # Deals with opening the images in the files list, and drawing them to a page-per-image.
    # Saves the PDF name as the current date-time
    def exportToPDF(self):
        now = datetime.datetime.now()
        title = now.strftime("%Y-%m-%d %H-%M-%S.pdf")

        canvas = Canvas('{}.pdf'.format(title))
        canvas.setPageSize(A4)
        document_width, document_height = A4

        for i in files:
            im = ImageReader(i)
            image_width, image_height = im.getSize()
            image_aspect = image_height / float(image_width)
            print_width = document_width
            print_height = document_width * image_aspect
            canvas.drawImage(im, document_width - print_width, document_height - print_height, width=print_width,
                             height=print_height, preserveAspectRatio=True, mask='auto', anchor='c', )
            canvas.showPage()

        canvas.save()

        self.labelFrame2.config(text="Images selected: {}".format(selected))


if __name__ == '__main__':
    app = GUI()
    app.root.mainloop()
