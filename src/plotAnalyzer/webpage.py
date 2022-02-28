from bs4 import BeautifulSoup
from requests import get
from os.path import splitext, exists
import tempfile
from pdf2image import convert_from_path

RESULTS_FILENAME = "figureResults.txt"

def getWebPageImages(url):
    url = url.replace('\n',"")
    resp = get(url)
    soup = BeautifulSoup(resp.text, features="html.parser")

    doneFiles = []
    thisResultsFileName = url.split('/')[-2] + "_" + RESULTS_FILENAME
    if exists(thisResultsFileName):
        with open(thisResultsFileName, 'r') as f:
            for line in f.readlines():
                doneFiles.append(line.split(':')[1].replace("\n",""))
    for link in soup.find_all('a'):
        #print(link)
        if link.get('href')[-1] != '/' and link.get('href') not in doneFiles:
            #print(link)
            r = get(url + link.get('href'))
            if splitext(link.get('href'))[1] == '.pdf':
                pdfTmpFile = tempfile.NamedTemporaryFile()

                pdfTmpFile.write(r.content)
                images = convert_from_path(pdfTmpFile.name)

                pdfTmpFile.close()

                with tempfile.NamedTemporaryFile(suffix='.png') as f:
                    images[0].save(f.name, 'PNG')
                    yield f.name, link.get('href')

            else:
                with tempfile.NamedTemporaryFile(suffix=splitext(link.get('href'))[1]) as f:
                    f.write(r.content)
                    yield f.name, link.get('href')
