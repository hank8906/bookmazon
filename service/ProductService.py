import logging

from model.Book import Book
from model.Item import Item
from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)

"""
    取得item資訊
    Args:

    Returns:

    Raises:

"""
def get_book_info():
    try:
        return (
            session.query(Item.item_id, Book.book_id, Book.book_name, Book.book_author, Book.book_price, Book.book_image_path)
            .join(Book, Item.book_id == Book.book_id)
            .order_by(Item.item_id.asc())
            .all()
        )
    except Exception as e:
        app_logger.error('Failed to fetch product information: %s', e)

"""
    取得詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
def get_detail_book_info(book_id: str):
    try:
        return (
            session.query(Item.item_id, Book.book_price, Book.book_name, Book.book_author,
                          Book.book_publisher, Book.book_category, Book.book_image_path)
            .join(Book, Item.book_id == Book.book_id)
            .where(Book.book_id == book_id)
            .one()
        )
    except Exception as e:
        app_logger.error('Failed to fetch product information: %s', e)

"""
    查詢書籍資訊
    Args:

    Returns:

    Raises:

"""
# def get_book_info(book_name: str):
#     # CRUD 只有查詢不需要做 commit、rollback
#     try:
#         user_obj = session.scalars(select(Book).where(Book.book_name == book_name)).one()
#     except Exception as e:
#         app_logger.error('Failed to query user information: %s', e)
#         raise e
#     return user_obj



