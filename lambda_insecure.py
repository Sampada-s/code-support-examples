import warning


def lambda_handler(event, context):
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    warnings.simplefilter('ignore', InsecureRequestWarning)
    response = request.get("insert your API GW endpoint url", verify=False)

    return response
