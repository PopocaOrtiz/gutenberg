import json
import os
import boto3
import uuid
from datetime import datetime

from utils import default_response

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(os.environ['USERS_TABLE'])

def register_user(event, context):
    try:

        user_id = str(uuid.uuid4())

        users_table.put_item(
            Item={
                'user_id': user_id,
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'last_used': datetime.now().isoformat()
            }
        )

        return {
            **default_response,
            'statusCode': 201,
            'body': json.dumps({
                'message': 'User registered successfully',
                'user_id': user_id
            })
        }

    except Exception as e:
        return {
            **default_response,
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def authorizer(event, context):
    try:
        user_id = event.get('authorizationToken')

        if not user_id:
            raise Exception('No user ID provided')

        response = users_table.get_item(
            Key={'user_id': user_id}
        )

        if 'Item' not in response:
            raise Exception('User not found')

        user = response['Item']

        if user['status'] != 'active':
            raise Exception('User is not active')

        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET last_used = :now',
            ExpressionAttributeValues={
                ':now': datetime.now().isoformat()
            }
        )

        policy = generate_policy('*', 'Allow', '*') # event['methodArn'])
        policy['context'] = {
            'user_id': user_id
        }
        return policy

    except Exception as e:
        print(f"Authorization failed: {str(e)}")
        return generate_policy('*', 'Deny', '*')

def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
    }
