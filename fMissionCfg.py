import os
import boto3
import time
#import commands
from decimal import Decimal
from datetime import datetime,timedelta

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('tblMission')
    
    ticks = time.time()
    localtime = time.asctime( time.localtime(ticks) )
    
    '''
    myIPaddr = 'test'
    myIPaddr = commands.getoutput('curl http://icanhazip.com/')
    
    response = table.put_item(
        Item={
            'timePush': localtime,
            'callIP': myIPaddr
         }
    )
    '''
   
    response = table.put_item(
        Item={
            'timePush': 'M001',
            'bidMode': 'lowerPrice',
            'bidInstanceType': 'm4.large',
            'maxUnitprice': '0.08',
            'maxWaitTime': '600',
            'timeCfg': localtime,
            'transNumber': '10',
            'transOK': '0',
            'notifyEmail': 'No',
            'rsltList':['rsltList']
         }
    )
   
  
    
    return;
    