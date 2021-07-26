import boto3


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('your_bucket')

    keys = []

    for obj in bucket.objects.filter(Prefix='path/to/files/'):

        if obj.key.endswith('py'):
            keys.append(obj.key)

    print(keys)

    for key in keys:
        bucket.download_file(key)

    return ('Success')
