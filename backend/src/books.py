import json
import os
import boto3
import requests
from datetime import datetime
from boto3.dynamodb.conditions import Key
from bs4 import BeautifulSoup

from utils import api_response, error_response

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')

BOOKS_TABLE = os.environ['BOOKS_TABLE']
books_table = dynamodb.Table(BOOKS_TABLE)

user_books_table = dynamodb.Table(os.environ['USER_BOOKS_TABLE'])
GUTENBERG_API_URL = os.environ['GUTENBERG_API_URL']


def get_book(event, context):
    try:
        user_id = event['headers']['Authorization']
        book_id = int(event["pathParameters"]["id"])

        if not book_id:
            return error_response("Missing book_id")

        return _get_book(book_id, user_id)
    except Exception as e:
        return error_response(str(e), 500)


def _get_book(book_id: int, user_id: int):
        # First, check if the book exists in the books table
        book_response = books_table.get_item(Key={"book_id": book_id})

        # If book doesn't exist in our database, fetch from Gutenberg
        if "Item" in book_response:
            book_item = book_response["Item"]
            book_data = book_item['book_data']
        else:
            # Fetch data from Gutenberg API
            response = requests.get(f"{GUTENBERG_API_URL}/ebooks/{book_id}")
            if response.status_code != 200:
                return error_response("Failed to fetch book", response.status_code)

            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1').text

            book_data = {
                'book_id': str(book_id),
                'title': title
            }

            # Save to books table
            books_table.put_item(
                Item={
                    "book_id": book_id,
                    "book_data": book_data,
                    "created_at": datetime.now().isoformat()
                }
            )

        # Now save/update the user-book relationship
        user_books_table.put_item(
            Item={
                "user_id": user_id,
                "book_id": book_id,
                "added_at": datetime.now().isoformat(),
                "book_data": book_data
            }
        )

        return api_response({
            "message": "Book saved successfully",
            "book": book_data
        }, 200)



def get_user_books(event, context):
    try:
        user_id = event['requestContext']['authorizer']['user_id']
        result = _get_user_books(user_id)
        return api_response(result, 200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return error_response(str(e), 500)


def _get_user_books(user_id: str) -> dict:

    # First, get all book IDs for this user
    user_books_response = user_books_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id),
        ProjectionExpression='book_data'
    )
    
    items = user_books_response.get('Items')

    if not items:
        return {
            "books": []
        }

    return {
        "books": [item['book_data'] for item in items]
    }