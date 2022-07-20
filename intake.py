from tkinter import *
import sqlite3 as sq
import datetime
import tkinter as tk
from tkinter import filedialog
import PyPDF2

import re

from anyio import open_file
from matplotlib.cbook import open_file_cm

from urllib.parse import urlparse
import pdfplumber
import pandas as pd
from collections import namedtuple



# Create a new window with the title "Freight Entry Form"
window = tk.Tk()
window.title("Freight Shipment Entry Form")
window.iconbitmap()
window.geometry("750x750")


window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)


my_text = Text(window, height=30, width=60)
my_text.pack(pady=10)


# Create a new frame `frm_form` to contain the Label
# and Entry widgets for entering address information
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3, pady=10)
# Pack the frame into the window
frm_form.pack()

# List of field labels
labels = [
    "Brokerage:",
    "Driver:",
    "Address Line 1:",
    "Address Line 2:",
    "Rate:",
    "State:",
    "Postal Code:",
    "Country:",
]

# Loop over the list of field labels
for idx, text in enumerate(labels):
    # Create a Label widget with the text from the labels list
    label = tk.Label(master=frm_form, text=text)
    # Create an Entry widget
    entry = tk.Entry(master=frm_form, width=50)
    # Use the grid geometry manager to place the Label and
    # Entry widgets in the row whose index is idx
    label.grid(row=idx, column=0, sticky="e")
    entry.grid(row=idx, column=1)

# Create a new frame `frm_buttons` to contain the
# Submit and Clear buttons. This frame fills the
# whole window in the horizontal direction and has
# 5 pixels of horizontal and vertical padding.
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

# Create the "Submit" button and pack it to the
# right side of `frm_buttons`
btn_submit = tk.Button(master=frm_buttons, text="Submit")
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

Line = namedtuple('Line', 'company_id company_name doctype reference currency voucher inv_date due_date open_amt_tc open_amt_bc current months1 months2 months3')



company_re = re.compile(r'(V\d+) (.*) Phone:')
line_re = re.compile(r'\d{2}/\d{2}/\d{4} \d{2}/\d{2}/\d{4}')


lines = []
total_check = 0


# Create the "Clear" button and pack it to the
# right side of `frm_buttons'

# option:: clear text box
def Clear_text_box():
    my_text.delete(1.0, END)

# option::open pdf file, then grab file name,
def open_pdf():

    open_file =filedialog.askopenfilename(
        initialdir="C:/Users/q9077/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*pdf"),
            ("All Files", "*.*")))

            #check for file
    if open_file:
                pdf_file = PyPDF2.PdfFileReader(open_file)
                page = pdf_file.getPage(0)
                # extract text from pdf
                page_text = page.extractText()

                my_text.insert(1.0, page_text)



def Extract_All_Text():

    open_file =filedialog.askopenfilename(
        initialdir="C:/Users/q9077/",
        title="Open PDF File",
        filetypes=(
            ("PDF Files", "*pdf"),
            ("All Files", "*.*")))

            #check for file
    if open_file:
        pdf_file = PyPDF2.PdfFileReader(open_file)
        pageObj = pdf_file.getNumPages()
        for page_count in range(pageObj):
            page = pdf_file.getPage(page_count)
            page_text = page.extractText()

            my_text.insert(1.0, page_text)    




def EncryptPDF():

    open_file =filedialog.askopenfilename(
        initialdir="C:/Users/q9077/",
        title="Encrypt PDF",
        filetypes=(
            ("PDF Files", "*pdf"),
            ("All Files", "*.*")))

            #check for file
    if open_file:
        pdfReader = PyPDF2.PdfFileReader(open_file)
        pdfWriter = PyPDF2.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
         pdfWriter.addPage(pdfReader.getPage(pageNum))
         pdfWriter.encrypt('abc')
         resultPdf = open('encrypted-example.pdf', 'wb')
         pdfWriter.write(resultPdf)
         resultPdf.close()


def Input_Shipment():

    open_file =filedialog.askopenfilename(
        initialdir="C:/Users/q9077/",
        title="Input Shipment",
        filetypes=(
            ("PDF Files", "*pdf"),
            ("All Files", "*.*")))

    if open_file:
        with pdfplumber.open(open_file) as pdf:
            pages = pdf.pages
            for page in pdf.pages:
                text = page.extract_text()
        for line in text.split('\n'):
            my_text.insert(1.0, text)
            comp = company_re.search(line)
            if comp:
                company_id, company_name = comp.group(1), comp.group(2)

                
            elif line.startswith('Rate Confirmation'):
                doctype = 'RATE'

            elif line.startswith('INVOICE'):
                doctype = 'INVOICE'

            elif line_re.search(line):
                items = line.split()
                lines.append(Line(company_id, company_name, doctype, *items))
                
            elif line.startswith('Supplier total'):
                tot = float(line.split()[2].replace(',', ''))
                total_check += tot
        


my_menu = Menu(window)
window.config(menu=my_menu)


# dropdown menus

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_pdf)
file_menu.add_command(label="Clear", command=Clear_text_box)
file_menu.add_command(label="Encrypt PDF", command=EncryptPDF)
file_menu.add_command(label="Extract all Text", command=Extract_All_Text)
file_menu.add_command(label="Input Shipment", command=Input_Shipment)




file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)





# Start the application
window.mainloop()


