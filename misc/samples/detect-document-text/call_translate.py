import boto3
import json
import sys
import time
import uuid

# Amazon Textract
textract = boto3.client(
 service_name='textract',
 region_name= 'us-east-1')

# Amazon S3
s3 = boto3.resource('s3')

# Amazon Translate
translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

try:
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'ki-textract-demo-docs',
                'Name': str(sys.argv[1])
            }
        }
    )

    print ('')
    for item in response["Blocks"]:
      if item["BlockType"] == "LINE":

        print ('\033[94m' +  item["Text"] + '\033[0m')
        result = translate.translate_text(Text=item["Text"], SourceLanguageCode="en", TargetLanguageCode="de")
        print ('\033[92m' + result.get('TranslatedText') + '\033[0m')

        print ('')
except Exception as e:
    print (e.message)
