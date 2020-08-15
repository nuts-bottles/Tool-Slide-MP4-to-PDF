import glob
import fitz  # pymupdf is needed for the implementation
import os
import time

START_NUM = 0
END_NUM = 500

def jpg2pdf(img_path, pdf_file):
    doc = fitz.open()
    x = 1
    for i in range(START_NUM, END_NUM):
        img_file = img_path + str(i) + ".jpg"
        if not os.path.exists(img_file):
            print("SKIP : " + str(i) + " is not found")
        else:
            print("FOUND: Page" + str(i) + "-->" + str(x))        
            imgdoc = fitz.open(img_file)
            pdfbytes = imgdoc.convertToPDF()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)
            x = x + 1
    doc.save(pdf_file)
    doc.close()


if __name__ == '__main__':
    input_path = './output/'
    output_file = './' +  time.strftime("PDF_%m%d_%H%M%S", time.localtime()) +'.pdf'
    jpg2pdf(img_path=input_path, pdf_file = output_file)
