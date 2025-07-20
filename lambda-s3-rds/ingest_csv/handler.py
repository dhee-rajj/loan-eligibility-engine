import json
import boto3
import requests
import os

def handler(event, context):
    try:
        # Extract S3 bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        # Compose webhook URL (n8n should expose this)
        n8n_webhook_url = os.environ['N8N_WEBHOOK_URL']  # e.g. http://<n8n-host>:5678/webhook/s3-trigger/

        # Payload to send to n8n
        payload = {
            "bucket": bucket,
            "key": key
        }

        # Send POST to n8n
        response = requests.post(n8n_webhook_url, json=payload)

        if response.status_code >= 200 and response.status_code < 300:
            return {
                'statusCode': 200,
                'body': json.dumps(f'Successfully notified n8n: {key}')
            }
        else:
            raise Exception(f"n8n responded with status {response.status_code}: {response.text}")

    except Exception as e:
        print("Lambda Handler Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error triggering n8n: {str(e)}')
        }
