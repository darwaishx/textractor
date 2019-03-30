# Bring current boto3 to Lambda

Follow steps below. [Or follow these steps if you would instead like](CreateLayer.md) to package a layer from scratch or add additional libraries.

## 1. Download packaged layer
- Download [boto3-layer.zip](boto3-layer.zip)

## 2. Create Layer
- In AWS Console go to Lambda
- Click on Layers and Create Layer
- Name: Boto3
- Upload boto3-layer.zip file you just downloaded.
- Compatible runtimes: Python3.6 and Python 3.7
- Click Create

## 3. Add Layer in Lambda Function
- Go to your Lambda function in AWS Console
- Click on Layers
- Click on Add a Layer
- Under Compatible Layer, select layer you added above
- Choose Version
- Click Add
- Click Save
