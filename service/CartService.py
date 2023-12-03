from model.Cart import Cart
from model.CartItem import CartItem
from model.Book import Book
from model.Item import Item
from utils.dbUtil import session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from contextlib import contextmanager
from flask import flash
from sqlalchemy import func

# Logger
from utils import logger
import logging

app_logger = logger.setup_logger(logging.INFO)

class CartService:
    @contextmanager
    def handle_transaction(self):
        """Context manager for handling database transactions."""
        try:
            yield
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            app_logger.error('Database transaction error: %s', e)
            raise  # 中斷當前的程式流程，拋出異常

    # TODO
    def add_to_cart(self, user_account, item_id):
        """Add a book to the user's cart. Check stock before adding."""
        with self.handle_transaction():
            # 檢查庫存
            item = session.query(Item).filter(Item.item_id == item_id).first()
            if not item or Item.book_count <= 0:
                flash('商品無庫存', 'warning')
                return False

            # 獲取或創建購物車
            cart = self.get_or_create_cart(user_account)
            cart_item = session.query(CartItem).filter(
                CartItem.cart_id == Cart.cart_id, CartItem.item_id == item_id).first()

            # 更新或添加購物車項目
            if cart_item:
                if cart_item.quantity >= item.book_count:
                    flash('購物車中的商品數量超出庫存，無法再添加', 'warning')
                    return False

            self.update_cart_item(cart, item_id)

            return True

    # TODO
    def update_cart_item(self, cart, item_id):

        """Update or add a new item in the cart."""
        cart_item = session.query(CartItem).filter(CartItem.cart_id == Cart.cart_id,
                                               CartItem.item_id == item_id).first()  # 修改：使用 utils 中的 session 進行查詢
        if cart_item:
            cart_item.quantity += 1

        else:
            cart_item = CartItem(cart_id=Cart.cart_id, item_id=item_id, quantity=1, create_datetime=datetime.now())
            session.add(cart_item)

    # TODO
    def get_or_create_cart(self, user_account):
        """Get an existing cart or create a new one for the user."""
        cart = session.query(Cart).filter(Cart.user_account == user_account).first()  # 修改：使用 utils 中的 session 進行查詢
        if not cart:
            cart = Cart(user_account=user_account, create_datetime=datetime.now())
            session.add(cart)
        return cart

    # TODO : 塞假資料去測試是可以用，但實際上未知
    def get_cart_items(self, user_account):
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

    #TODO : 同上
    def remove_from_cart(self, cart_item_id):
        """Remove an item from the cart."""
        with self.handle_transaction():
            cart_item = session.query(CartItem).filter(
                CartItem.cart_item_id == cart_item_id).first()  # 修改：使用 utils 中的 session 進行查詢

            # 數量歸零就刪掉
            if cart_item is not None:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                else:
                    session.delete(cart_item)
                return True

            return False


    # def calculate_total_price(self, user_account):
    #     """Calculate the total price of all items in the user's cart."""
    #     try:
    #         cart_items = self.get_cart_items(user_account)
    #         books = session.query(Book).filter(
    #             Book.book_id.in_([Item.item_id for item in cart_items])).all()  # 修改：使用 utils 中的 session 進行查詢
    #         book_price_map = {Book.book_id: Book.book_price for book in books}
    #         return sum(CartItem.quantity * book_price_map.get(Item.book_id, 0) for item in cart_items)
    #     except SQLAlchemyError as e:
    #         app_logger.error('Error during price calculation: %s', e)
    #         return 0

    def calculate_total_price(self, user_account):
        try:
            cart_items = self.get_cart_items(user_account)
            total_price = sum(cart_item.quantity * book.book_price for cart_item, item, book in cart_items)
            return total_price
        except SQLAlchemyError as e:
            app_logger.error('Error during price calculation: %s', e)
            return 0

    # 把購物車內商品總數顯示在首頁的購物車按鈕的旁邊
    def get_cart_item_count(self, user_account):
        """Get the count of all items in a user's cart."""
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