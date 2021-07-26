import json


def lambda_handler(event, context):
    message_bytes = responseData.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)

    return json.dumps({
        'isBase64Encoded': 'true',
        'statusCode': 200,
        'body': base64_bytes,
    })
