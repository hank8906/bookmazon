from model.Item import Item
from model.Book import Book
from model.Order import Order
from model.OrderItem import OrderItem
from utils.dbUtil import session
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

# Logger
from utils import logger
import logging

app_logger = logger.setup_logger(logging.INFO)

class OrderService:
    def add_order(self, user_account, cart_items, updated_quantities):
        try:
            # session.begin()

            # 檢查庫存是否足夠
            shortage_items = []
            # for cart_item_tuple in cart_items:
            #     cart_item, item, book = cart_item_tuple
            #
            #     if not item or item.book_count < cart_item.quantity:
            #         shortage_items.append(book)

            for cart_item_tuple in cart_items:
                cart_item, item, book = cart_item_tuple
                updated_quantity = updated_quantities.get(cart_item.cart_item_id)

                if not item or item.book_count < updated_quantity:
                    shortage_items.append(book)

            # 如果庫存不足，不進行後續操作
            if shortage_items:
                for book in shortage_items:
                    flash(f"庫存不足: {book.book_name}")
                return None

            # 庫存足夠，進行庫存減少和訂單創建
            for cart_item_tuple in cart_items:
                cart_item, item, _ = cart_item_tuple
                updated_quantity = updated_quantities.get(cart_item.cart_item_id)
                item.book_count -= updated_quantity  # 使用更新后的数量

            # 創建訂單
            order_total_price = sum(
                updated_quantities[cart_item.cart_item_id] * book.book_price for cart_item, item, book in
                cart_items)
            order = Order(user_account=user_account, order_total_price=order_total_price, order_status=0)
            session.add(order)
            session.flush()

            for cart_item, item, book in cart_items:
                updated_quantity = updated_quantities.get(cart_item.cart_item_id)
                order_item = OrderItem(order_id=order.order_id, item_id=cart_item.item_id,
                                       quantity=updated_quantity)
                session.add(order_item)

            # 刪除購物車中的商品
            for cart_item, _, _ in cart_items:
                session.delete(cart_item)

            session.commit()
            return order.order_id

        except SQLAlchemyError as e:
                session.rollback()
                app_logger.error("Create order error: %s", e)
                raise

    def get_user_orders(self, user_account):
        try:
            orders = session.query(Order).filter(Order.user_account == user_account).all()
            return orders
        except SQLAlchemyError as e:
            app_logger.error(f"Get user order error：{str(e)}")
            flash(f"無法獲取訂單資訊，請稍後再試。錯誤訊息：{str(e)}")
            return []

    def get_order_by_id(self, order_id):
        try:
            order = session.query(Order).filter(Order.order_id == order_id).first()
            return order
        except SQLAlchemyError as e:
            app_logger.error("Get order error %s", e)
            flash("無法獲取訂單資訊，請稍後再試。")
            return None

    def get_order_items(self, order_id):
        try:
            order_items = session.query(OrderItem).filter(OrderItem.order_id == order_id) \
                .join(Item, OrderItem.item_id == Item.item_id) \
                .join(Book, Item.book_id == Book.book_id) \
                .add_columns(Book.book_name, Book.book_price) \
                .all()
            return order_items
        except SQLAlchemyError as e:
            app_logger.error("Get order items error：%s", e)
            flash("無法獲取訂單項目資訊，請稍後再試。")
            return []

