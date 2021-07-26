import boto3
import datetime


def lambda_handler(event, context):


    client = boto3.client('cloudwatch')

    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'string',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'string',
                        'MetricName': 'string',
                        'Dimensions': [
                            {
                                'Name': 'string',
                                'Value': 'string'
                            },
                        ]
                    },
                    'Period': 123,
                    'Stat': 'string',
                    'Unit': 'Seconds'
                },
                'Expression': 'string',
                'Label': 'string',
                'ReturnData': True | False,
                'Period': 123
            },
        ],
        StartTime=datetime(2015, 1, 1),
        EndTime=datetime(2021, 1, 1),
        NextToken='string',
        ScanBy='TimestampDescending',
        MaxDatapoints=123,
        LabelOptions={
            'Timezone': 'string'
        }
    )

    return response
