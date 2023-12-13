from model.CartItem import CartItem
from model.Item import Item
from model.Order import Order
from model.OrderItem import OrderItem
from utils.dbUtil import session
from flask import flash
from sqlalchemy.exc import SQLAlchemyError

class OrderService:
    def add_order(self, user_account, cart_items):
        try:
            session.begin()

            # 合併庫存檢查和訂單創建
            insufficient_stock_items = []
            for cart_item in cart_items:
                item = session.query(Item).filter(Item.item_id == cart_item.item_id).with_for_update().first()
                if item and item.book_count >= cart_item.quantity:
                    item.book_count -= cart_item.quantity
                else:
                    insufficient_stock_items.append(item)

            if insufficient_stock_items:
                session.rollback()
                for item in insufficient_stock_items:
                    flash(f"庫存不足: {item.book_name}, 剩餘庫存: {item.book_count}")
                return None

            # 創建訂單
            order = Order(user_account=user_account, order_total_price=sum([ci.quantity * ci.item.book_price for ci in cart_items]))
            session.add(order)
            session.flush()

            for cart_item in cart_items:
                order_item = OrderItem(order_id=order.order_id, item_id=cart_item.item_id, quantity=cart_item.quantity)
                session.add(order_item)

            # 刪除購物車中的商品
            for cart_item in cart_items:
                session.delete(cart_item)

            session.commit()
            return order.order_id

        except SQLAlchemyError as e:
            session.rollback()
            flash(f"結帳失敗，請稍後再試。錯誤信息：{str(e)}")
            return None

    def get_user_orders(self, user_account):
        try:
            orders = session.query(Order).filter(Order.user_account == user_account).all()
            return orders
        except SQLAlchemyError as e:
            flash(f"無法獲取訂單資訊，請稍後再試。錯誤信息：{str(e)}")
            return []