import json
#from __future__ import print_function 
import boto3
import time
from decimal import Decimal
from datetime import datetime,timedelta


def lambda_handler(event, context):
    srcFilename = 'test'
    bucketstr = 'xxxtestbucket1'
    trigName= 'CodePush'
    n = 0
    numrec = '0'
    ticks = time.time()
    localtime = time.asctime( time.localtime(ticks) )
    trigTime = localtime
    
    #debug skip

    for record in event['Records']:
        n = n+1
        bucketstr = record['s3']['bucket']['name']
        srcFilename = record['s3']['object']['key']
        trigTime = record['eventTime']
        trigName = record['eventName']
        numrec = str(n)
        #ticks = time.time()
        #localtime = time.asctime( time.localtime(ticks) )+srcFilename
        #dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        #table = dynamodb.Table('tblMission')
        #response = table.put_item(
        #    Item={
        #        'timePush': localtime,
        #        'bucket': bucketstr,
        #        'srcFilename': srcFilename,
        #        'trigTime': trigTime,
        #        'trigName': trigName,
        #        'numlog': numrec
        #     }
        #)

    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('tblTrans2')
    
    #Check ahead to avoid redo again
    try:
        existRec = table.get_item(
            Key={
                'srcFilename': srcFilename
            }
        )
        #print(existRec)
        strIndi = 'Item'
        if ('Item' in existRec):
            print('exist')
            existItem = existRec['Item']['bucketname']
            existLog = existRec['Item']['numlog']+'+1'
            response = table.update_item(
                Key={
                    'srcFilename': srcFilename
                },
                UpdateExpression="set numlog = :a",
                ExpressionAttributeValues={
                    ':a': existLog
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            print('null')
            
            #======= append a trans log  =================
            response = table.put_item(
                Item={
                    'srcFilename': srcFilename,
                    'timeBoarding': localtime,
                    'bucketname': bucketstr, 
                    'trigTime': trigTime,
                    'trigName': trigName,
                    'numlog': numrec
                 }
            )
            
            spot_region = 'us-east-1'
            wantInstaceType = 'm4.large'
            ebs_device_name = '/dev/sda1'
            ebs_volume_type = 'gp2'
            ebs_volume_size = 10
            amiIDstr = 'ami-02xxxxxxxx18bff94'
            tmplID = 'lt-013xxxxxxxx700ff0'
            tmplVer = '1'    
                
            
            #======= get price =================
            ec2client = boto3.client('ec2',region_name = spot_region)
            
            response = ec2client.describe_spot_price_history(
                AvailabilityZone='us-east-1a',
                StartTime=datetime(2019, 4, 25),
                EndTime=datetime(2019, 4, 29),
                InstanceTypes=[wantInstaceType],
                MaxResults=1,
                ProductDescriptions=['Linux/UNIX (Amazon VPC)']
            )
            
            i = 1
            for query_spot_price in response["SpotPriceHistory"]:
                #print('Spot Price ' + str(i))
                #print(query_spot_price['AvailabilityZone'])
                #print(query_spot_price['InstanceType'])
                #print(query_spot_price['SpotPrice'])
                #print(query_spot_price['Timestamp'])
                #print('\r\n')
                curPrice = float(query_spot_price['SpotPrice'])*2;
                print('bidPrice:', curPrice)
                bidPrice = str(curPrice)
                i = i + 1
            
            #======= spin a spot instance =================
            ec2res = boto3.resource('ec2',region_name = spot_region)
            
            response = ec2res.create_instances(
                #DryRun=True,
                #ImageId=amiIDstr,
                InstanceType=wantInstaceType,
                KeyName='myLabNV',
                MinCount=1,
                MaxCount=1,
                #EbsOptimized=True
                InstanceMarketOptions={
                    'MarketType': 'spot',
                    'SpotOptions': {
                        'MaxPrice': bidPrice,
                        'SpotInstanceType': 'one-time',
                        'BlockDurationMinutes': 60,
                        #'ValidUntil': datetime(2019, 5, 30),
                        'InstanceInterruptionBehavior': 'terminate'
                    }
                },
                LaunchTemplate={
                    'LaunchTemplateId': tmplID,
                    #'LaunchTemplateName': 'tmplMB3demo',
                    'Version': tmplVer
                },
                #UserData="IyEvYmluL2Jhc2gKc3VkbyBweXRob24gL2hvbWUvZWMyLXVzZXIvdGVzdC9qb2JydW4ucHk=",
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'testSpot-'+srcFilename 
                            },
                            {
                                'Key': 'srcID',
                                'Value': srcFilename 
                            }
                        ]
                    }
                ]
            )
            print(response[0].id)
    except:
        print('error')
    
print('End')
