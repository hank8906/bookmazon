import logging
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from enumeration.SystemMessage import ShoppingCartSystemCode, CommonSystemCode
from exception.BusinessError import BusinessError
from model.Book import Book
from model.Cart import Cart
from model.CartItem import CartItem
from model.Item import Item
# Logger
from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)

"""
    加入購物車
    Args:
        user_account 會員帳號     
        item_id      商品ID
        quantity     購買數量
    Returns:

    Raises:
        BusinessError
"""
def add_item_to_cart(user_account, item_id, quantity):
    # 檢查庫存
    item = session.query(Item).where(Item.item_id == item_id).first()

    # 庫存不夠要告知會員
    if not item or item.book_count < 1:
        error_code = ShoppingCartSystemCode.OUT_OF_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.OUT_OF_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 加入購物車數量不得小於 1
    if quantity < 1:
        error_code = ShoppingCartSystemCode.ITEM_NOT_FOUND.value.get('system_code')
        message = ShoppingCartSystemCode.ITEM_NOT_FOUND.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 加入購物車數量不能大於庫存數
    if quantity > item.book_count:
        error_code = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 檢查購物車選購數量(購物車原本選購該商品的數量加上選購數量)
    cart_item_count = get_cart_designated_item_count(user_account, item_id) + quantity
    if cart_item_count > item.book_count:
        error_code = ShoppingCartSystemCode.EXCEEDS_MAX_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.EXCEEDS_MAX_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 建立購物車
    try:
        cart = get_or_create_cart(user_account)
        cart_item = session.query(CartItem).where(
            CartItem.cart_id == cart.cart_id, CartItem.item_id == item_id).first()
    except SQLAlchemyError as e:
        app_logger.error('Database transaction error: %s', e)
        error_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 購物車的數量大於庫存數
    if cart_item is not None and cart_item.quantity >= item.book_count:
        error_code = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    try:
        update_cart_item(cart, item_id, quantity)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        app_logger.error('Database transaction error: %s', e)
        error_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

"""
    加總會員購物車裡面的特定商品數量
    Args:
        user_account 會員帳號     
        item_id      商品ID
    Returns:
        特定商品數量    
    Raises:

"""
def get_cart_designated_item_count(user_account: str, item_id: int):
    try:
        cart = session.query(Cart).where(Cart.user_account == user_account).first()
        if not cart:
            return 0

        total_count = session.query(func.sum(CartItem.quantity)).where(
            CartItem.cart_id == cart.cart_id).where(
            CartItem.item_id == item_id).scalar()
        return total_count if total_count is not None else 0

    except SQLAlchemyError as e:
        app_logger.error('Error during count cart designated item: %s', e)
        error_code = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

"""
    建立或取得購物車
    Args:
        user_account 會員帳號
    Returns:
        Cart 購物車
    Raises:

"""
def get_or_create_cart(user_account):
    cart = session.query(Cart).where(Cart.user_account == user_account).first()
    if not cart:
        cart = Cart(user_account=user_account, create_datetime=datetime.now())
        session.add(cart)
    return cart

"""
    更新購物車品項數量
    Args:
        user_account 會員帳號     
        item_id      商品ID
        quantity     購買數量
    Returns:

    Raises:

"""
def update_cart_item(cart, item_id, quantity):
    cart_item = session.query(CartItem).where(CartItem.cart_id == cart.cart_id,
                                              CartItem.item_id == item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.cart_id, item_id=item_id, quantity=quantity,
                             create_datetime=datetime.now())

        session.add(cart_item)

"""
    查詢購物車品項
    Args:
        user_account 會員帳號
    Returns:
        購物車品項
    Raises:
        BusinessError
"""
def get_cart_items(user_account):
    try:
        cart = session.query(Cart).where(Cart.user_account == user_account).first()
        if cart:
            cart_items_query = session.query(CartItem, Item, Book).join(
                Item, CartItem.item_id == Item.item_id).join(
                Book, Item.book_id == Book.book_id).where(
                CartItem.cart_id == cart.cart_id).all()
            return cart_items_query
        return []
    except SQLAlchemyError as e:
        app_logger.error('Database error during cart retrieval: %s', e)
        error_code = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

"""
    刪除購物車品項
    Args:
        cart_item_id 購物車品項 ID
    Returns:
    
    Raises:
        BusinessError
"""
def remove_item_from_cart(cart_item_id):
    try:
        cart_item = session.query(CartItem).where(
            CartItem.cart_item_id == cart_item_id).first()
        session.delete(cart_item)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        app_logger.error('Database transaction error: %s', e)
        error_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

"""
    計算購物車內商品總價
    Args:
        cart_item_id 購物車品項 ID
    Returns:
        購物車內商品總數
    Raises:

"""
def calculate_total_price(user_account):
    try:
        cart_items = get_cart_items(user_account)
        total_price = sum(cart_item.quantity * book.book_price for cart_item, item, book in cart_items)
        return total_price
    except SQLAlchemyError as e:
        app_logger.error('Error during price calculation: %s', e)
        return 0

"""
    把購物車內商品總數顯示在首頁的購物車按鈕的旁邊
    Args:
        cart_item_id 購物車品項 ID
    Returns:
        購物車內商品總數
    Raises:
        
"""
def get_cart_item_count(user_account):
    try:
        cart = session.query(Cart).where(Cart.user_account == user_account).first()
        if not cart:
            return 0

        total_count = session.query(func.sum(CartItem.quantity)).where(
            CartItem.cart_id == cart.cart_id).scalar()
        return total_count if total_count is not None else 0

    except SQLAlchemyError as e:
        app_logger.error('Error during count: %s', e)
        return 0
