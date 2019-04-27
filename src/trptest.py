from helper import FileHelper
import json
from trp import *
from og import OutputGenerator
from textractor import *

def traverseDocument(doc):
    for page in doc.pages:
        for line in page.lines:
            print("Line: {}--{}".format(line.text, line.confidence))
            for word in line.words:
                print("Word: {}--{}".format(word.text, word.confidence))
        for table in page.tables:
            print("TABLE")
            r = 1
            for row in table.rows:
                c = 1
                for cell in row.cells:
                    print("Table[{}][{}] = {}-{}".format(r, c, cell.text, cell.confidence))
                    c += 1
                r += 1
        for field in page.form.fields:
            k = ""
            v = ""
            if(field.key):
                k = field.key.text
            if(field.value):
                v = field.value.text
            print("{}={}".format(k,v))

        f = page.form.getFieldByName("Full Name:")
        print("{}={}".format(f.key.text, f.value.text))

        print("\nPrinting Form\n=========")
        print(page.form)

def generateOutput(filePath, response):
    print("Generating output...")
    name, ext = FileHelper.getFileNameAndExtension(filePath)
    opg = OutputGenerator(response,
                "{}-v2-{}".format(name, ext), True, True)
    opg.run()
    opg.generateInsights(True, True, 'es', 'us-east-1')

def run():
    filePath = "temp-response.json"
    response = json.loads(FileHelper.readFile(filePath))

    doc = Document(response)

    #print(doc)
    #traverseDocument(doc)
    generateOutput(filePath, response)

run()

