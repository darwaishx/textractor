import json
from helper import FileHelper
from ta import TextAnalyzer, TextMedicalAnalyzer, TextTranslater
from trp import *

class OutputGenerator:
    def __init__(self, response, fileName, forms, tables):
        self.response = response
        self.fileName = fileName
        self.forms = forms
        self.tables = tables

        self.document = Document(self.response)

    def outputText(self, page, p):
        text = page.text
        FileHelper.writeToFile("{}-page-{}-text.txt".format(self.fileName, p), text)

        textInReadingOrder = page.getTextInReadingOrder()
        FileHelper.writeToFile("{}-page-{}-text-inreadingorder.txt".format(self.fileName, p), textInReadingOrder)

    def outputForm(self, page, p):
        csvData = []
        for field in page.form.fields:
            csvItem  = []
            if(field.key):
                csvItem.append(field.key.text)
            else:
                csvItem.append("")
            if(field.value):
                csvItem.append(field.value.text)
            else:
                csvItem.append("")
            csvData.append(csvItem)
        csvFieldNames = ['Key', 'Value']
        FileHelper.writeCSV("{}-page-{}-forms.csv".format(self.fileName, p), csvFieldNames, csvData)

    def outputTable(self, page, p):

        csvData = []
        for table in page.tables:
            csvRow = []
            csvRow.append("Table")
            csvData.append(csvRow)
            for row in table.rows:
                csvRow  = []
                for cell in row.cells:
                    csvRow.append(cell.text)
                csvData.append(csvRow)
            csvData.append([])
            csvData.append([])

        FileHelper.writeCSVRaw("{}-page-{}-tables.csv".format(self.fileName, p), csvData)

    def run(self):

        if(not self.document.pages):
            return

        FileHelper.writeToFile("{}-response.json".format(self.fileName), json.dumps(self.response))

        print("Total Pages in Document: {}".format(len(self.document.pages)))

        p = 1
        for page in self.document.pages:

            FileHelper.writeToFile("{}-page-{}-response.json".format(self.fileName, p), json.dumps(page.blocks))

            self.outputText(page, p)

            if(self.forms):
                self.outputForm(page, p)

            if(self.tables):
                self.outputTable(page, p)

            p = p + 1

    def _generateInsightsPerDocument(self, page, p, insights, medicalInsights, translate, ta, tma, tt):

        maxLen = 1000

        text = page.text

        start = 0
        sl = len(text)

        sentiment = []
        syntax = []
        entities = []
        keyPhrases = []
        medicalEntities = []
        phi = []
        translation = ""

        while(start < sl):
            end = start + maxLen
            if(end > sl):
                end = sl

            subText = text[start:end]

            if(insights):
                sentiment.append(ta.getSentiment(subText))
                syntax.extend(ta.getSyntax(subText))
                entities.extend(ta.getEntities(subText))
                keyPhrases.extend(ta.getKeyPhrases(subText))

            if(medicalInsights):
                medicalEntities.extend(tma.getMedicalEntities(subText))
                phi.extend(tma.getPhi(subText))

            if(translate):
                translation = translation + tt.getTranslation(subText) + "\n"

            start = end

        if(insights):
            FileHelper.writeToFile("{}-page-{}-insights-sentiment.json".format(self.fileName, p), json.dumps(sentiment))
            FileHelper.writeToFile("{}-page-{}-insights-syntax.json".format(self.fileName, p), json.dumps(syntax))
            FileHelper.writeToFile("{}-page-{}-insights-entities.json".format(self.fileName, p), json.dumps(entities))
            FileHelper.writeToFile("{}-page-{}-insights-keyPhrases.json".format(self.fileName, p), json.dumps(keyPhrases))

        if(medicalInsights):
            FileHelper.writeToFile("{}-page-{}-medical-insights-entities.json".format(self.fileName, p), json.dumps(medicalEntities))
            FileHelper.writeToFile("{}-page-{}-medical-insights-phi.json".format(self.fileName, p), json.dumps(phi))

        if(translate):
            FileHelper.writeToFile("{}-page-{}-text-translation.txt".format(self.fileName, p), translation)

    def generateInsights(self, insights, medicalInsights, translate, awsRegion):

        print("Generating insights...")

        if(not self.document.pages):
            return

        ta = TextAnalyzer('en', awsRegion)
        tma = TextMedicalAnalyzer(awsRegion)

        tt = None
        if(translate):
            tt = TextTranslater('en', translate, awsRegion)

        p = 1
        for page in self.document.pages:
            self._generateInsightsPerDocument(page, p, insights, medicalInsights, translate, ta, tma, tt)
            p = p + 1
