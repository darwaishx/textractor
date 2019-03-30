# Textractor

You can use textractor to extract text, forms and tables from documents using Amazon Textract and generate output in different formats including raw JSON, JSON for each page in the document, text, text in reading order, key/values exported as CSV, tables exported as CSV. It can also generate insights or translate detected text by using Amazon Comprehend, Amazon Comprehend Medical and Amazon Translate.

## Prerequisites

- Python3
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)

## Setup

- Download [code](./zip/textractor.zip) and unzip on your local machine.

## Usage

Format:
- python3 textractor.py --documents [file|folder|S3Object|S3Folder] --text --forms --tables --region [AWSRegion] --insights --medical-insights --translate [LanguageCode]

Examples:
- python3 textractor.py --documents mydoc.jpg --text
- python3 textractor.py --documents ./mydocs/ --text --forms --tables
- python3 textractor.py --documents s3://mybucket/mydoc.pdf --text --forms --tables
- python3 textractor.py --documents s3://mybucket/myfolder/ --forms
- python3 textractor.py --documents s3://mybucket/myfolder/ --text --forms --tables --region us-east-1 --insights --medical-insights --translate es

> Path to a folder on local drive or S3 bucket must end with /

> Only one of the flags (--text, --forms and --tables) is required at the minimum. You can use combination of all three.

> --region is optional. us-east-1 is default for local files/folder. For documents in S3, region of S3 bucket is selected as default AWS region to call Amazon Textract.

> --insights, --medical-insights and --translate are optional.

## Generated Output

Tool generates several files in the format below:

#### Text, forms and tables related output files

- document-response.json: Raw JSON response of Amazon Textract API call.
- document-page-n-response.json: Raw JSON blocks for each page document.
- document-page-n-text.txt: Detected text for each page in the document.
- document-page-n-text-inreadingorder.txt: Detected text in reading order (multi-column) for each page in the document.
- document-page-n-forms.csv: Key/Value pairs for each page in the document.
- document-page-n-tables.csv: Tables detected for each page in the document.

#### Insights related output files

- document-page-n-text-translation.txt: Translation of detected text for each page in the document.
- document-page-n-insights-entities.json: Entities in detected text for each page in the document.
- document-page-n-insights-sentiment.json: Sentiment in detected text for each page in the document.
- document-page-n-insights-keyPhrases.json: Key phrases in detected text for each page in the document.
- document-page-n-insights-syntax.json: Syntax in detected text for each page in the document.
- document-page-n-medical-insights-entities.json: Medical entities in detected text for each page in the document.
- document-page-n-medical-insights-phi.json: Phi in detected text for each page in the document.

## Arguments

  | Argument  | Description |
  | ------------- | ------------- |
  | --documents  | Name of the document or local folder/S3 bucket |
  | --text  | Extract text from the document |
  | --forms  | Extract key/value pairs from the document |
  | --tables | Extract tables from the document |
  | --region  | AWS region to use for Amazon Textract API call. us-east-1 is default. |
  | --insights  | Generate files with sentiment, entities, syntax, and key phrases. |
  | --medical-insights  | Generate files with medical entities and phi. |
  | --translate  | Generate file with translation. |

## Source Code
- [textractor.py](./src/textractor.py) is the entry point. It parses input arguments, and query S3 or local folder to get input documents. It then iterates over input documents and use [DocumentProcessor](./src/tdp.py) to get response from Amazon Textract APIs. [OutputGenerator](./src/og.py) is then used to generate output which takes advantage of [Document](./src/trp.py) to parse JSON response returned by Amazon Textract.
- [DocumentProcessor](./src/tdp.py) takes document path, call Amazon Textract APIs, takes care of the paging etc. and return complete response for the document.
- [OutputGenerator](./src/og.py) takes Textract response and uses [Document](./src/trp.py) to process response and generate output.
- [Document](./src/trp.py) makes it easier to process response from Amazon Textract.

```

# Call Amazon Textract and get JSON response
docproc = DocumentProcessor(bucketName, filePath, awsRegion, detectText, detectForms, tables)
response = docproc.run()

# Get DOM
doc = Document(response)

# Iterate over elements in the document
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
        print("{}={}".format(field.key.text, field.value.text))

# Document
print(doc)

# Individual Page
print(doc.pages[0])

# A cell in table
print(doc.pages[0].tables[0].rows[0].cells[0].text)

# A form field
print(doc.pages[0].form.fields[0].key.text)
print(doc.pages[0].form.fields[0].value.text)

field = page.form.getFieldByName("Key")
print(field.text.text)
print(field.value.text)

```

## Cost
  - As you run this tool, it calls different APIs (Amazon Textract, optionally Amazon Comprehend, Amazon Comprehend Medical, Amazon Translate) in your AWS account. You will get charged for all the API calls made as part of the analysis.
