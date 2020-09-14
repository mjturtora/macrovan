#! python3
# read_pdf.py - finds List numbers from all pdf's in a folder
# Gets number from third page by finding string following substring "List"
# plagiarized from https://automatetheboringstuff.com/chapter13/

import PyPDF2
import os
import pandas as pd

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


def excel_write(path, lists):
    """export to excel worksheet"""
    df = pd.DataFrame({'List Name': [element[0] for element in lists],
                       'List Number': [element[1] for element in lists],
                       'Doors': [element[2] for element in lists]
                       })
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='List Numbers', index=False)
    writer.save()
    #writer.close()

if __name__ == '__main__':
    # Loop through all the PDF files.
    #path = r'D:\Stuff\Projects\Pol\macrovan\io\Output'
    path = r'D:\Stuff\Projects\Pol\macrovan\io\Output\PDFExports_20200901125934_35_files'
    pdf_files = get_fnames(path)
    lists = []
    for filename in pdf_files:
        #print(filename)
        pdfFileObj = open(r'D:\Stuff\Projects\Pol\macrovan\io\Output\PDFExports_20200901125934_35_files\\' + filename, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        page = pdfReader.getPage(0).extractText()
        first_part, lnum = page.split("Doors:", 1)
        doors = lnum.split("Affiliation")[0]
        #print(doors)

        page = pdfReader.getPage(2).extractText()
        lname, lnum = page.split("List", 1)
        lists.append([lname, lnum, doors])

    print([element[2] for element in lists])
    write_path = r'..\io\Output\PDFExports_20200901125934_35_files\List Numbers.xlsx'
    excel_write(write_path, lists)


