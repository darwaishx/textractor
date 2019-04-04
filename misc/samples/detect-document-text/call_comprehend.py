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

# Amazon Comprehend
comprehend_client = boto3.Session(region_name='us-east-1').client('comprehend')

try:
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': 'ki-textract-demo-docs',
                'Name': str(sys.argv[1])
            }
        }
    )

    para = ""
    for item in response["Blocks"]:
      if item["BlockType"] == "LINE":
        para = para + " " + item["Text"]

    sentiment_analysis = comprehend_client.detect_sentiment(LanguageCode="en", Text=para)
    print ('Sentiment: ' + sentiment_analysis.get('Sentiment'))
    print ('')

except Exception as e:
    print (e.message)
