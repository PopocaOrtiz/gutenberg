import json

from books import _get_book, _get_user_books

def test_get_new_book():
    res = _get_book(75122, '9754ae02-0593-478f-8b34-d4fb724c843a')
    assert res['statusCode'] == 200
    assert json.loads(res['body'])['message'] == "Book saved successfully"

def test_user_books():
    res = _get_user_books('9754ae02-0593-478f-8b34-d4fb724c843a')
    assert len(res['books']) == 1
