import boto3


def lambda_handler(event, context):

    client = boto3.client('iotevents-data')

    response = client.list_alarms(
        alarmModelName='string',
        nextToken='string',
        maxResults=123
    )
    for alarm_name in response['alarmSummaries']['alarmModelName']:
        describe_alarm = client.describe_alarm(
            alarmModelName=alarm_name,
            keyValue='string')
        return describe_alarm
