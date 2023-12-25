import logging
from datetime import timedelta

from sqlalchemy import func, or_, String

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
            session.query(Item.item_id, Book.book_id, Book.book_name, Book.book_author, Book.book_price,
                          Book.book_image_path)
                .join(Book, Item.book_id == Book.book_id)
                .order_by(Item.item_id.asc())
                .all()
        )
    except Exception as e:
        return ''
        # app_logger.error('Failed to fetch product information: %s', e)

"""
    取得詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
def get_detail_book_info(item_id: str):
    try:
        return (
            session.query(Item.item_id, Item.item_status, Item.book_count, Item.create_datetime, Item.update_datetime,
                          Item.provider_account, Book.book_id, Book.book_price, Book.book_name, Book.book_author,
                          Book.book_publisher, Book.book_category, Book.book_image_path)
                .join(Book, Item.book_id == Book.book_id)
                .where(Item.item_id == item_id)
                .one()
        )
    except Exception as e:
        return ''
        # app_logger.error('Failed to fetch product information: %s', e)

"""
    查詢書籍資訊
    Args:

    Returns:

    Raises:

"""
def searchProduct(keyword:str):
    try:
        query = (session.query(Item.item_id, Item.item_status, Item.book_count, Item.create_datetime, Item.update_datetime,
                          Item.provider_account, Book.book_id, Book.book_price, Book.book_name, Book.book_author,
                          Book.book_publisher, Book.book_category, Book.book_image_path)
                 .join(Book, Item.book_id == Book.book_id))

        query = query.filter(
            or_(
                func.lower(Book.book_name).like(func.lower(f"%{keyword}%")),
                func.lower(Book.book_author).like(func.lower(f"%{keyword}%")),
                func.lower(Book.book_publisher).like(func.lower(f"%{keyword}%")),
                func.lower(Book.book_id).like(func.lower(f"%{keyword}%")),
                func.lower(Item.provider_account).like(func.lower(f"%{keyword}%")),
                func.lower(Book.book_category).like(func.lower(f"%{keyword}%"))
            )
        )
        return query.all()

    except Exception as e:
        return ''
        # app_logger.error('Failed to fetch product information: %s', e)

"""
    查詢分類書籍資訊
    Args:

    Returns:

    Raises:

"""
def searchProductsByCategory(keyword:str, search_field:str, min_price, max_price, book_category:str):
    try:
        query = (session.query(Item.item_id, Item.item_status, Item.book_count, Item.create_datetime, Item.update_datetime,
                          Item.provider_account, Book.book_id, Book.book_price, Book.book_name, Book.book_author,
                          Book.book_publisher, Book.book_category, Book.book_image_path)
                 .join(Book, Item.book_id == Book.book_id))

        # 價格範圍搜尋
        if min_price is not None and max_price is not None:
            query = query.filter(Book.book_price.between(min_price, max_price))

        # 進階搜尋
        if keyword:
            if search_field == '全文':
                query = query.filter(
                    or_(
                        func.lower(Book.book_name).like(func.lower(f"%{keyword}%")),
                        func.lower(Book.book_author).like(func.lower(f"%{keyword}%")),
                        func.lower(Book.book_publisher).like(func.lower(f"%{keyword}%")),
                        func.lower(Item.provider_account).like(func.lower(f"%{keyword}%")),
                        func.lower(Item.book_id).like(func.lower(f"%{keyword}%")),
                    )
                )
            elif search_field == '書名':
                query = query.filter(func.lower(Book.book_name).like(func.lower(f"%{keyword}%")))
            elif search_field == '作者':
                query = query.filter(func.lower(Book.book_author).like(func.lower(f"%{keyword}%")))
            elif search_field == '出版商':
                query = query.filter(func.lower(Book.book_publisher).like(func.lower(f"%{keyword}%")))
            elif search_field == '提供者':
                query = query.filter(func.lower(Item.provider_account).like(func.lower(f"%{keyword}%")))
            elif search_field == 'ISBN':
                query = query.filter(func.lower(Book.book_id).like(func.lower(f"%{keyword}%")))

        # 分類搜尋
        if book_category and book_category != 'all':
            print(book_category)
            query = query.filter(func.lower(Book.book_category) == func.lower(book_category))

        return query.all()

    except Exception as e:
        return ''
        # app_logger.error('Failed to fetch product information: %s', e)

