# GCP Service Account to AWS IAM Role

This repo contains code that accompanies [the blog post](http://cevo.com.au/) on
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

