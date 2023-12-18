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

# 加入購物車
def add_to_cart(user_account, item_id, quantity):
    # 檢查庫存
    item = session.query(Item).filter(Item.item_id == item_id).first()

    # if quantity not integer or quantity <= 0
    if quantity <= 0:
        error_code = ShoppingCartSystemCode.ITEM_NOT_FOUND.value.get('system_code')
        message = ShoppingCartSystemCode.ITEM_NOT_FOUND.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    if quantity > item.book_count:
        error_code = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.QUANTITY_EXCEEDS_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    if not item or item.book_count < 1:
        error_code = ShoppingCartSystemCode.OUT_OF_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.OUT_OF_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 檢查購物車選購數量(購物車原本選購該商品的數量加上選購數量) ->這樣會變成只要購物車裡有一個>=庫存，就沒辦法新增其他商品?
    cart_item_count = get_cart_item_count(user_account) + quantity
    if cart_item_count > item.book_count:
        error_code = ShoppingCartSystemCode.EXCEEDS_MAX_STOCK.value.get('system_code')
        message = ShoppingCartSystemCode.EXCEEDS_MAX_STOCK.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # 建立購物車
    cart = get_or_create_cart(user_account)
    cart_item = session.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id, CartItem.item_id == item_id).first()

    # 加入商品到購物車
    if cart_item:
        if cart_item.quantity >= item.book_count:
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

def update_cart_item(cart, item_id, quantity):
    cart_item = session.query(CartItem).filter(CartItem.cart_id == cart.cart_id,
                                               CartItem.item_id == item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.cart_id, item_id=item_id, quantity=quantity,
                             create_datetime=datetime.now())
        session.add(cart_item)

def get_or_create_cart(user_account):
    """Get an existing cart or create a new one for the user."""
    cart = session.query(Cart).filter(Cart.user_account == user_account).first()  # 修改：使用 utils 中的 session 進行查詢
    if not cart:
        cart = Cart(user_account=user_account, create_datetime=datetime.now())
        session.add(cart)
    return cart

# 顯示購物車內內容
def get_cart_items(user_account):
    try:
        cart = session.query(Cart).filter(Cart.user_account == user_account).first()
        if cart:
            cart_items_query = session.query(CartItem, Item, Book).join(
                Item, CartItem.item_id == Item.item_id).join(
                Book, Item.book_id == Book.book_id).filter(
                CartItem.cart_id == cart.cart_id).all()
            return cart_items_query
        return []
    except SQLAlchemyError as e:
        app_logger.error('Database error during cart retrieval: %s', e)
        return []

# 刪除購物車內內容
def remove_from_cart(cart_item_id):
    """Remove an item from the cart."""
    cart_item = session.query(CartItem).filter(
        CartItem.cart_item_id == cart_item_id).first()

    try:
        session.delete(cart_item)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        app_logger.error('Database transaction error: %s', e)
        error_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

    # if cart_item is not None:
    #     if cart_item.quantity > 1:
    #         cart_item.quantity -= 1
    #     else:
    #         session.delete(cart_item)
    #     return True
    #
    # return False

def calculate_total_price(self, user_account):
    try:
        cart_items = self.get_cart_items(user_account)
        total_price = sum(cart_item.quantity * book.book_price for cart_item, item, book in cart_items)
        return total_price
    except SQLAlchemyError as e:
        app_logger.error('Error during price calculation: %s', e)
        return 0

# 把購物車內商品總數顯示在首頁的購物車按鈕的旁邊
def get_cart_item_count(user_account):
    try:
        cart = session.query(Cart).filter(Cart.user_account == user_account).first()
        if not cart:
            return 0

        total_count = session.query(func.sum(CartItem.quantity)).filter(
            CartItem.cart_id == cart.cart_id).scalar()
        return total_count if total_count is not None else 0

    except SQLAlchemyError as e:
        app_logger.error('Error during count: %s', e)
        return 0
