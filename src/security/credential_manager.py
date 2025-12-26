#!/usr/bin/env python3
"""
Secure Credential Manager - Uses AWS default credentials and stores Google service account key
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

def store_google_service_account():
    """Store Google service account key in AWS Secrets Manager"""
    
    # Read the service account JSON file
    service_account_path = "../cannabis-genetics-db-261c538aa94f.json"
    
    with open(service_account_path, 'r') as f:
        service_account_data = json.load(f)
    
    # Use default AWS credentials from ~/.aws/credentials
    secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
    
    secret_name = "cannabis-genetics-google-service-account"
    
    try:
        # Create the secret
        response = secrets_client.create_secret(
            Name=secret_name,
            Description="Google Cloud service account key for Cannabis Genetics Database",
            SecretString=json.dumps(service_account_data)
        )
        
        print(f"SUCCESS: Secret created successfully!")
        print(f"Secret ARN: {response['ARN']}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            # Update existing secret
            response = secrets_client.update_secret(
                SecretId=secret_name,
                SecretString=json.dumps(service_account_data)
            )
            print(f"SUCCESS: Secret updated successfully!")
            print(f"Secret ARN: {response['ARN']}")
        else:
            print(f"ERROR: {e}")
            return False
    
    return True

def get_google_credentials():
    """Retrieve Google service account credentials from AWS Secrets Manager"""
    
    secrets_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret_name = "cannabis-genetics-google-service-account"
    
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except ClientError as e:
        print(f"ERROR: Error retrieving Google credentials: {e}")
        return None

if __name__ == "__main__":
    # Store the Google service account key
    store_google_service_account()