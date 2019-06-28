#!/usr/bin/env python3
#
# This code must run on a VM instance with a service account associated with it.
# The service account must be granted the 'Service Account Token Creator' IAM Role

import requests
import boto3

SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT", "default")
BASE_URL = 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/'
AUDIENCE = 'potato'
FORMAT = 'full'
METADATA_HEADERS = { 'Metadata-Flavor': 'Google' }

# Construct a URL with the audience and format
url = BASE_URL + f"{SERVICE_ACCOUNT}/identity?audience={AUDIENCE}&format={FORMAT}"

r = requests.get(url, headers=METADATA_HEADERS)
token = r.text

print(token)
