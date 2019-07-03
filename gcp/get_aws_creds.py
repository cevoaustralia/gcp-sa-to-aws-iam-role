#!/usr/bin/env python3
#
# This code must run on a VM instance with a service account associated with it.
# The service account must be granted the 'Service Account Token Creator' IAM Role

import os
import sys
from os import path
import requests
import boto3

role = sys.argv[1]

# Set up the URL to request
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT", "default")
BASE_URL = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/'
AUDIENCE = 'potato'
FORMAT = 'full'
METADATA_HEADERS = { 'Metadata-Flavor': 'Google' }

# Construct a URL with the audience and format
url = BASE_URL + SERVICE_ACCOUNT + "/identity?audience=" + AUDIENCE + "&format=" + FORMAT

# Get the service token
r = requests.get(url, headers=METADATA_HEADERS)
token = r.text

# Turn the token into AWS credentials
sts = boto3.client('sts')
res = sts.assume_role_with_web_identity(
        RoleArn=role,
        WebIdentityToken=token,
        RoleSessionName='example')

creds = res['Credentials']

key = str(creds['AccessKeyId'])
secret = str(creds['SecretAccessKey'])
token = str(creds['SessionToken'])

output = "[default]\naws_access_key_id=%s\naws_secret_access_key=%s\naws_session_token=%s\n" % (key, secret, token)

try:
    os.mkdir(path.join(os.getenv('HOME'), '.aws'))
except:
    pass

with open(path.join(os.getenv('HOME'), '.aws', 'credentials'), 'w') as fp:
        print(output, file=fp)

