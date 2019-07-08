import time
import random
import boto3
import os
import commands
from decimal import Decimal
from datetime import datetime,timedelta
from ec2_metadata import ec2_metadata


def lambda_handler(event, context):
    rsltFilename  = 'NULL'
    trigTime = 'right now'
    listArr = ['TestSrc']
    idstr = 'M001'
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('tblMission')
    
    try:
        #for record in event['Records']:
        #    rsltFilename = record['s3']['object']['key']
        #    trigTime = record['eventTime']
        listArr.append(rsltFilename)
    except:
        print('err')
        listArr= ['Testrlst']
    
    
    response = table.update_item(
        Key={
            'timePush': idstr
        },
        UpdateExpression="set rsltList = :rlist",
        ExpressionAttributeValues={
            ':rlist': listArr
        },
        ReturnValues="UPDATED_NEW"
    )
            

    if ('Item' in missionRec):
        print('exist')
        numTotal = missionRec['Item']['transNumber']
        numSucc = missionRec['Item']['transOK']
        listArr = missionRec['Item']['rsltList']
        noteMail = missionRec['Item']['notifyEmail']
        print(listArr)
        
        if (rsltFilename not in listArr):
            listArr.append(rsltFilename)
            numSucc = str(int(numSucc)+1)
            if ( int(numSucc)>=int(numTotal) and noteMail!='Yes'):
                #Send noti Mail
                strMsg = 'HPC mission '+ idstr +' accomplished at '+ trigTime +'.'
                sns = boto3.resource('sns')
                topic = sns.Topic('arn:aws:sns:us-east-1:11xxxxxxxx55:NotifyMe')
                mailmess = topic.publish(
                    Message= strMsg
                )
                print(mailmess)
                noteMail = 'Yes'
                    
            response = table.update_item(
                Key={
                    'timePush': idstr
                },
                UpdateExpression="set transOK = :succ, rsltList = :rlist, notifyEmail = :m",
                ExpressionAttributeValues={
                    ':succ': numSucc,
                    ':rlist': listArr,
                    ':m': noteMail
                },
                ReturnValues="UPDATED_NEW"
            )
            print(response)
