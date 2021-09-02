from __future__ import print_function

import json
import urllib
import boto3
import os 
import subprocess
import sys 

print('Loading Function')

s3 = boto3.client('s3', region_name='us-east-1')
s3_resource = boto3.resource('s3', region_name='us-east-1') 

def lambda_handler(event, context):

    # Get the bucket name and event log from lambda logs 
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    print('New file has been uploaded to: ' + key)
    file = ('s3://' + bucket + '/' + key)
    filename = key.rsplit('/',1)[-1]
    filepath = key.rsplit('/',1)[0]

    try:
        print('EFS dir before downloading: ', os.listdir('/mnt/access' + filepath))
        s3.download_file(bucket, key, '/mnt/access/' + key)
        print('EFS dir after downloading: ', os.listdir('/mnt/access' + filepath))
    except Exception as e:
        print(e)
        print("Error getting the object {} from bucket {}. Make sure they exist and your bucket is in the same aws region as this function.".format(key, bucket))
        raise e
