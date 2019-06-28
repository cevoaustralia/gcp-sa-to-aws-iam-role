import boto3
import cfnresponse
import json
import os
from botocore.exceptions import ClientError

iam = boto3.client("iam")

def create_provider(url, thumbprints, audiences):
    resp = iam.create_open_id_connect_provider(
        Url=url,
        ThumbprintList=thumbprints
    )
    arn = resp['OpenIDConnectProviderArn']

    for client in audiences:
        iam.add_client_id_to_open_id_connect_provider(
            OpenIDConnectProviderArn=arn,
            ClientID=client
        )

    return arn, "Created provider " + arn

def update_provider(arn, thumbprints, audiences):
    iam.update_open_id_connect_provider_thumbprint(
        OpenIDConnectProviderArn=arn,
        ThumbprintList=thumbprints
    )

    current_provider = iam.get_open_id_connect_provider(
        OpenIDConnectProviderArn=arn
    )

    for client in current_provider['ClientIDList']:
        if not client in audiences:
            print("Removing client " + client + " from ClientIDList of " + arn)
            iam.remove_client_id_from_open_id_connect_provider(
                OpenIDConnectProviderArn=arn,
                ClientID=client
            )

    # this is idempotent, so no issue if client ID already exists
    for client in audiences:
        print("Ensuring client " + client + " is in ClientIDList of " + arn)
        iam.add_client_id_to_open_id_connect_provider(
            OpenIDConnectProviderArn=arn,
            ClientID=client
        )

    return "OIDC Provider " + arn + " updated"


def delete_provider(arn):
    resp = iam.delete_open_id_connect_provider(OpenIDConnectProviderArn=arn)
    return "OIDC Provider " + arn + " deleted"

def lambda_handler(event, context):
    res = False
    responseData = {}
    provider_arn = "UNKNOWN"
    account = os.getenv("AWS_ACCOUNT_ID", "unknown")

    print( "Got event: " + json.dumps(event) )

    try:
        url = event['ResourceProperties']['Url']
        tprints = event['ResourceProperties']['ThumbprintList']
        audiences = event['ResourceProperties']['Audiences'] or []
        provider_arn = "arn:aws:iam::" + account + ":oidc-provider/" + url.split('/')[2]
        res = True

        if event['RequestType'] == 'Create':
            provider_arn, reason = create_provider(url, tprints, audiences)
        elif event['RequestType'] == 'Update':
            reason = update_provider(provider_arn, tprints, audiences)
        elif event['RequestType'] == 'Delete':
            reason = delete_provider(provider_arn)
        else:
            res = False
            reason = "Unknown operation: " + event['RequestType']
    except Exception as e:
        res = False
        reason = "Lambda failed: " + str(e)

    responseData['Reason'] = reason
    responseData['Arn'] = provider_arn


    provider_name = provider_arn.rsplit('/')[1]
    print( "Returning " + str(responseData) + " provider_arn " + provider_arn)

    if res:
        cfnresponse.send(event, context, cfnresponse.SUCCESS, reason, responseData, provider_name)
    else:
        cfnresponse.send(event, context, cfnresponse.FAILED, reason, responseData, provider_name)

if __name__ == "__main__":
    event = {
        "RequestType": "Create",
        "ResourceProperties": {
            "Url": "https://idp.example.com",
            "ThumbprintList": [
                "abcd1234abcd1234"
            ]
        }
    }
    context = {}
    lambda_handler(event, context)
