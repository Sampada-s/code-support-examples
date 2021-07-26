import json
from logging import exception
import boto3
import os

uri = os.environ['trust-uri']
cert_arn = os.environ['certificate']
private_key = os.environ['private-key']
uri = os.environ['trust-uri']
uri = os.environ['trust-uri']

def lambda_handler(event, context):
    client = boto3.client('apigateway')

    domain_names = ['domain-1', 'domain-2', 'domain-3']
    for domain in domain_names:
        try:
            client.create_domain_name(
            domainName=domain,
            certificatePrivateKey=private_key,
            certificateArn=cert_arn,
            endpointConfiguration={
                'types': [
                    'REGIONAL',
                ],
            },
            tags={
                'string': 'string'
            },
            securityPolicy='TLS_1_2',
            mutualTlsAuthentication={
                'truststoreUri': 'string',
                'truststoreVersion': 'string'
            })
        except exception as e:
            print(e)

        try:
            client.update_domain_name(
            domainName=domain,
            patchOperations=[
                {
                    'op': 'add',
                    'path': '/',
                    'value': 'base'
                },
            ]
        )

        except exception as ex:
            print(ex)

            



