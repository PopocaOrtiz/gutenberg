import json

default_response = {
    'headers': {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
}


def api_response(body: dict, status_code: int = 200) -> dict:
    return {
        **default_response,
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def error_response(message: str, status_code: int = 400):
    return api_response({"error": message}, status_code)
