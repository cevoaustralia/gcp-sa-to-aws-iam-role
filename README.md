# GCP Service Account to AWS IAM Role

This repo contains code that accompanies [the blog post](https://cevo.com.au/post/2019-07-29-using-gcp-service-accounts-to-access-aws/) on
using GCP Service Accounts to acquire AWS IAM Role credentials.

## Preparation

1. Create the GCP Service Account
1. Get the Service Account numeric Client ID

## Creating the stack

1. Acquire AWS credentials with rights to manage IAM Identity Providers, Lambda
   functions, and IAM Roles.
1. Build the rendered template and create the stack:

    ```shell
    CLIENT_ID=<service-account-client-id> make deploy
    ```
1. Copy the ARN of the role from the Outputs of the stack

## Acquiring Credentials

1. Create an Ubuntu VM in GCP, and associate the Service Account you created above
   with it
1. Log in to that VM
1. Install pre-requisites:
    ```shell
    apt-get update && apt-get install -y python3-pip
    ```
1. Download this repo onto that system:

    ```shell
    curl -L -o gcp-to-aws.zip https://github.com/cevoaustralia/gcp-sa-to-aws-iam-role/archive/master.zip
    ```
1. Unpack the repo:
    ```shell
    unzip gcp-to-aws.zip
    ```
1. Install the dependencies:
    ```shell
    cd gcp-sa-to-aws-iam-role-master/gcp
    pip3 install -r requirements.txt
    ```
1. Run the script with the ARN of the IAM Role created by the stack (above) as
   the argument:
    ```shell
    ./get_aws_creds.py arn:aws:iam::123456789012:role/DeploymentRole
    ```
1. Validate that your VM now has AWS credentials:
    ```shell
    aws sts get-caller-identity
    ```
1. Profit!

