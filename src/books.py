import json
import os
import boto3
import requests
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')
books_table = dynamodb.Table(os.environ['BOOKS_TABLE'])
user_books_table = dynamodb.Table(os.environ['USER_BOOKS_TABLE'])
GUTENBERG_API_URL = os.environ['GUTENBERG_API_URL']

def fetch_book(event, context):
    try:
        user_id = event['requestContext']['authorizer']['user_id']
        book_id = event["pathParameters"]["id"]

        if not book_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing book_id"})
            }

        # First, check if the book exists in the books table
        book_response = books_table.get_item(Key={"BookID": book_id})

        # If book doesn't exist in our database, fetch from Gutenberg
        if "Item" not in book_response:
            # Fetch data from Gutenberg API
            response = requests.get(f"{GUTENBERG_API_URL}{book_id}")
            if response.status_code != 200:
                return {
                    "statusCode": response.status_code,
                    "body": json.dumps({"error": "Failed to fetch book"})
                }

            book_data = response.json()

            # Save to books table
            books_table.put_item(
                Item={
                    "BookID": str(book_id),
                    "Metadata": book_data,
                    "created_at": datetime.now().isoformat()
                }
            )
            book_item = {
                "BookID": str(book_id),
                "Metadata": book_data
            }
        else:
            book_item = book_response["Item"]

        # Now save/update the user-book relationship
        user_books_table.put_item(
            Item={
                "user_id": user_id,
                "book_id": str(book_id),
                "added_at": datetime.now().isoformat(),
                "book_metadata": book_item["Metadata"]  # Denormalization for quick access
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Book saved successfully",
                "book": book_item
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }


def get_user_books(event, context):
    try:
        user_id = event['requestContext']['authorizer']['user_id']

        # First, get all book IDs for this user
        user_books_response = user_books_table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ProjectionExpression='book_id'
        )

        # If no books found, return empty list
        if not user_books_response.get('Items'):
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "books": []
                })
            }

        # Prepare book IDs for batch get
        book_ids = [item['book_id'] for item in user_books_response['Items']]

        # BatchGetItem can only process 100 items at a time
        books = []
        for i in range(0, len(book_ids), 100):
            batch_ids = book_ids[i:i + 100]
            response = dynamodb.batch_get_item(
                RequestItems={
                    os.environ['BOOKS_TABLE']: {
                        'Keys': [{'BookID': book_id} for book_id in batch_ids]
                    }
                }
            )

            if response['Responses'].get(os.environ['BOOKS_TABLE']):
                books.extend(response['Responses'][os.environ['BOOKS_TABLE']])

        return {
            "statusCode": 200,
            "body": json.dumps({
                "books": books
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging for debugging
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }

