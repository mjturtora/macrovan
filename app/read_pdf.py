#! python3
# read_pdf.py - finds index numbers from all pdf's in a folder
# plagiarized from https://automatetheboringstuff.com/chapter13/

import PyPDF2
import os

def get_fnames(path):
    # Get all the PDF filenames.
    pdf_files = []
    for filename in os.listdir(path):
        #print(filename)
        if filename.endswith('.pdf'):
            pdf_files.append(filename)
    pdf_files.sort(key=str.lower)
    #print(pdf_files)
    return pdf_files

if __name__ == '__main__':
    # Loop through all the PDF files.
    path = r'D:\Stuff\Projects\Pol\macrovan\io\Output'
    pdf_files = get_fnames(path)
    for filename in pdf_files:
        print(filename)
        # pdfFileObj = open(filename, 'rb')
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
