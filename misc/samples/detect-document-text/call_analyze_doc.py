import boto3
import json
import sys
from pprint import pprint

# Amazon Textract
textract = boto3.client(
 service_name='textract',
 region_name= 'us-east-1')

# Amazon S3
s3 = boto3.resource('s3')

try:
    response = textract.analyze_document(
        Document={
            'S3Object': {
                'Bucket': 'ki-textract-demo-docs',
                'Name': str(sys.argv[1])
            }
        },
        FeatureTypes=["TABLES", "FORMS"]
    )
    pprint(response)

except Exception as e:
    print (e.message)
