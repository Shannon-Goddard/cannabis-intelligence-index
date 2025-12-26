#!/usr/bin/env python3
"""
AWS Secrets Manager - Store Google Service Account Key
"""

import boto3
import json
from botocore.exceptions import ClientError

def store_google_credentials(service_account_json_path, aws_access_key, aws_secret_key, region='us-east-1'):
    """Store Google service account key in AWS Secrets Manager"""
    
    # Read the service account JSON file
    with open(service_account_json_path, 'r') as f:
        service_account_data = json.load(f)
    
    # Initialize AWS Secrets Manager client
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    
    secrets_client = session.client('secretsmanager')
    
    secret_name = "cannabis-genetics-google-service-account"
    
    try:
        # Create the secret
        response = secrets_client.create_secret(
            Name=secret_name,
            Description="Google Cloud service account key for Cannabis Genetics Database",
            SecretString=json.dumps(service_account_data)
        )
        
        print(f"✅ Secret created successfully!")
        print(f"Secret ARN: {response['ARN']}")
        print(f"Secret Name: {secret_name}")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceExistsException':
            # Update existing secret
            response = secrets_client.update_secret(
                SecretId=secret_name,
                SecretString=json.dumps(service_account_data)
            )
            print(f"✅ Secret updated successfully!")
            print(f"Secret ARN: {response['ARN']}")
        else:
            print(f"❌ Error: {e}")
            return False
    
    return True

def retrieve_google_credentials(aws_access_key, aws_secret_key, region='us-east-1'):
    """Retrieve Google service account key from AWS Secrets Manager"""
    
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    
    secrets_client = session.client('secretsmanager')
    secret_name = "cannabis-genetics-google-service-account"
    
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(response['SecretString'])
        return secret_data
    except ClientError as e:
        print(f"❌ Error retrieving secret: {e}")
        return None

if __name__ == "__main__":
    # You'll need to provide these values
    AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY_HERE"
    AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY_HERE" 
    AWS_REGION = "us-east-1"
    
    # Path to your Google service account JSON file
    service_account_path = "cannabis-genetics-db-261c538aa94f.json"
    
    # Store the credentials
    store_google_credentials(
        service_account_path, 
        AWS_ACCESS_KEY, 
        AWS_SECRET_KEY, 
        AWS_REGION
    )