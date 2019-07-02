import time
import random
import boto3
import os
import commands
from decimal import Decimal
from datetime import datetime,timedelta
from ec2_metadata import ec2_metadata
 
numCircle = 15
transIDstr = "test10"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('tblTrans2')
print "Start : %s" % time.ctime()

#read src Tag
#cmdout = commands.getstatusoutput('curl http://169.254.169.254/latest/meta-data/instance-id/')
#curInstanceId = 'i-0a15dbc8d44be27ff'
curInstanceId = ec2_metadata.instance_id
print(curInstanceId)

ec2res = boto3.resource('ec2','us-east-1')
curInstance = ec2res.Instance(curInstanceId)

tags = curInstance.tags
print(tags)
for tag in tags:
    if tag["Key"] == 'srcID':
        transIDstr = tag["Value"]

print(transIDstr)

tmCost = 0
for i in range(1,numCircle):
    tl = random.randint(12,20)
    tmCost = tmCost+tl
    tmCoststr = str(tmCost)
    strProgress = str(i*100/numCircle)+'%'
    
    #update progress
    response = table.update_item(
        Key={
            'srcFilename': transIDstr
        },
        UpdateExpression="set strIndiProgress = :u, execInstanceID = :i, timeCost=:c",
        ExpressionAttributeValues={
            ':u': strProgress,
            ':i': curInstanceId,
            ':c': tmCoststr
        },
        ReturnValues="UPDATED_NEW"
    )
    #simluate time cost block
    time.sleep( tl )
    print(i, tl)
    
#push result file
outputFile = 's3://xxxrsltbucket1/rslt_'+transIDstr
os.system('aws s3 cp /home/ec2-user/test/rslt.dat '+outputFile)

#update rslt info
response = table.update_item(
    Key={
        'srcFilename': transIDstr
    },
    UpdateExpression="set strIndiProgress = :u, rsltFilename = :o",
    ExpressionAttributeValues={
        ':u': '100%',
        ':o': outputFile
    },
    ReturnValues="UPDATED_NEW"
)
time.sleep(1)
response = curInstance.terminate('false')
print(response)