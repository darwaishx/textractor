# Bring current boto3 or other libraries to Lambda

Follow steps below to package layer zip file and then bring it to your Lambda function.

[Or follow these steps instead](UseProvidedLayer.md) to use an existing package already provided for you.

## 1. Launch and connect to an EC2 Instance (use Amazon Linux AMI with AWS command line tools etc.)
- Launch an EC2 instance
- SSH into the EC2 instance

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html

## 2. Once connected to the EC2 instance
- sudo yum -y update
- sudo yum -y upgrade
- sudo yum install python36
- python3 --version
- curl -O https://bootstrap.pypa.io/get-pip.py
- python3 get-pip.py --user
- mkdir layer
- cd layer
- mkdir python
- cd python
- pip3 install boto3 --target .
- You can add other libraries similarly (example): pip3 install Pillow --target .
- cd ..
- zip -r boto3-layer.zip ./python
- exit
- mkdir layer
- scp -i YOUR-KEY.pem ec2-user@YOUR-EC2-DNS.amazonaws.com:/home/ec2-user/boto3-layer.zip ./layer

## 3. Create Layer
- In AWS Console go to Lambda
- Click on Layers and Create Layer
- Name: Boto3
- Upload boto3-layer.zip file you just downloaded.
- Compatible runtimes: Python3.6 and Python 3.7
- Click Create

## 4. Add Layer in Lambda Function
- Go to your Lambda function in AWS Console
- Click on Layers
- Click on Add a Layer
- Under Compatible Layer, select layer you added above
- Choose Version
- Click Add
- Click Save
