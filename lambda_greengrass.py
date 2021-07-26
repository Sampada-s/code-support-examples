import boto3
import json
import logging
import os
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL","INFO")))

def handler(event, context):
    # Initialize boto 3 clients for iot and greengrass
    iot = boto3.client('iot')
    gg = boto3.client('greengrass')
    
    # Create IAM client
    iam = boto3.client('iam')
    
    # Pull device name from parameters passed in
    thingName = event['device_name']
    
    # Create keys and certificate
    response = iot.create_keys_and_certificate(
        setAsActive=True     
    )
    
    # Retrieve certificate arn from response
    certificateArn = response["certificateArn"]
    certificateId = response["certificateId"]
    certPublicKey = response['keyPair']['PublicKey']
    certPrivateKey = response['keyPair']['PrivateKey']
    certPem = response['certificatePem']
    
    # Describe certificates
    response = iot.describe_certificate(
        certificateId=certificateId
    )
    
    certObject = {
        'certificateId': certificateId,
        'certPublicKey': certPublicKey,
        'certPrivateKey': certPrivateKey,
        'certPem': certPem,
    }
    
    # Create iot thing
    response = iot.create_thing(
        thingName=thingName,
    )
    
    # Retrieve new thingArn and thingId from response
    thingArn = response['thingArn']
    thingId = response['thingId']
    
    # Create a policy
    my_managed_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "greengrass:Discover"
                ],
                "Resource": thingArn
            }
        ]
    }
    
    policy_name = thingName + "_policy"
    response = iot.create_policy(
      policyName=policy_name,
      policyDocument=json.dumps(my_managed_policy)
    )
    
    response = iot.attach_policy(
      policyName=policy_name,
      target=certificateArn
    )
    
    # Attach iot thing to principal
    response = iot.attach_thing_principal(
        thingName=thingName,
        principal=certificateArn
    )
    
    # Create green grass device definition
    response = gg.create_device_definition(
        InitialVersion={
            'Devices': [
                {
                    'CertificateArn': certificateArn,
                    'Id': thingId,
                    'ThingArn': thingArn,
                    'SyncShadow': True,
                },
            ]
        },
        Name=thingName,
    )
    
    # Create group version with created device definition 
    deviceDefinitionArn = response['LatestVersionArn']
    
    subscriptionName = thingName + '_subscriber'
    
    # Create subscription definition to know how to send the data
    response = gg.create_subscription_definition(
        InitialVersion={
            'Subscriptions': [
                {
                    'Id': subscriptionName,
                    'Source': thingArn,
                    'Subject': 'pac/data',
                    'Target': 'cloud'
                },
            ]
        },
        Name= subscriptionName,
    )
    
    # Retrieve and Store subscriptionArn
    subscriptionArn = response['LatestVersionArn']
    
    # ID of group I already have created
    createdGroupId = "abcdefgh"
    
    # Get greengrass group information to pull out latest version
    response = gg.get_group(
        GroupId=createdGroupId    
    )
    
    latestGroupVersion = response['LatestVersion']
    
    # Get green grass group version info to pull CoreDefinitionVersionARN
    response = gg.get_group_version(
        GroupId=createdGroupId,
        GroupVersionId=latestGroupVersion,
    )
    
    coreDefinitionVersionArn = response['Definition']['CoreDefinitionVersionArn']
    
    # # Create group version to be part of deployment
    response = gg.create_group_version(
        DeviceDefinitionVersionArn=deviceDefinitionArn,
        GroupId=createdGroupId,
        CoreDefinitionVersionArn=coreDefinitionVersionArn,
        SubscriptionDefinitionVersionArn=subscriptionArn
    )
    
    # Retrieve group version ID from response when creating group version
    groupVersionId = response['Version'] 
    
    # Create deployment
    response = gg.create_deployment(
        DeploymentType='NewDeployment',
        GroupId=createdGroupId,
        GroupVersionId=groupVersionId
    )

    return certObject