from utils.dbUtil import session
from sqlalchemy import select
from model.Book import Book
from model.Item import Item
from utils import logger
import logging

# app_logger = logger.setup_logger(logging.INFO)

# book_info_result = (
#         session.query(Book.book_id, Book.book_price, Book.book_name, Book.book_author,
#                       Book.book_publisher, Book.book_publisher)
#         .where(Book.book_id == '0123456789')
#         .all()
#     )
#
# print(book_info_result)

"""
    取得item資訊
    Args:

    Returns:

    Raises:

"""
def get_book_info():
    item_result = (
        session.query(Item.item_id, Book.book_id, Book.book_name, Book.book_author, Book.book_price)
        .join(Book, Item.book_id == Book.book_id)
        .order_by(Item.item_id.asc())
        .all()
    )

    return item_result


"""
    取得詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
def get_detail_book_info(book_id :str):
    book_info_result = (
        session.query(Book.book_id, Book.book_price, Book.book_name, Book.book_author,
                      Book.book_publisher, Book.book_category)
        .where(Book.book_id == book_id)
        .all()
    )

    return book_info_result

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



