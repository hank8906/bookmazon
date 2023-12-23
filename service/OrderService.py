import logging
from datetime import datetime

from flask import flash
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError

from enumeration.SystemMessage import OrderSystemCode, CommonSystemCode
from exception.BusinessError import BusinessError
from model.Book import Book
from model.CheckoutBo import CheckoutBo
from model.Item import Item
from model.Order import Order
from model.OrderItem import OrderItem
# Logger
from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)

def add_order(checkout_bo: CheckoutBo):
    # 檢查庫存是否足夠
    for cart_item_tuple in checkout_bo.cart_items:
        cart_item, item, book = cart_item_tuple
        if item.book_count < cart_item.quantity:
            # 如果庫存數不足，不得下單
            error_code = OrderSystemCode.PLACE_ORDER_FAILED.value.get('system_code')
            message = OrderSystemCode.PLACE_ORDER_FAILED.value.get('message')
            raise BusinessError(message=message, error_code=error_code)

    # 庫存足夠，現有庫存數扣除會員購買的數量
    for cart_item_tuple in checkout_bo.cart_items:
        cart_item, item, _ = cart_item_tuple
        item.book_count -= cart_item.quantity

    try:
        # 建立訂單
        order_total_price = sum(
            cart_item.quantity * book.book_price for cart_item, item, book in
            checkout_bo.cart_items)
        order = Order(user_account=checkout_bo.user_account,
                      recipient_name=checkout_bo.recipient_name,
                      order_total_price=order_total_price,
                      order_status='0',
                      payment_status='0',
                      shipping_status='0',
                      shipping_address=f'{checkout_bo.recipient_city}{checkout_bo.recipient_district}{checkout_bo.recipient_address}',
                      update_datetime=datetime.now(),
                      create_datetime=datetime.now()
                      )
        session.add(order)
        session.flush()
        for cart_item, item, book in checkout_bo.cart_items:
            order_item = OrderItem(order_id=order.order_id, item_id=cart_item.item_id,
                                   quantity=cart_item.quantity, update_datetime=datetime.now(),
                                   create_datetime=datetime.now())
            session.add(order_item)

        # 刪除購物車中的商品
        for cart_item, _, _ in checkout_bo.cart_items:
            session.delete(cart_item)

        session.commit()
        return order.order_id
    except SQLAlchemyError as e:
        session.rollback()
        app_logger.error("Create order error: %s", e)
        error_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)
    except Exception as e:
        app_logger.error("Create order error: %s", e)
        error_code = CommonSystemCode.SYSTEM_FAILED.value.get('system_code')
        message = CommonSystemCode.SYSTEM_FAILED.value.get('message')
        raise BusinessError(message=message, error_code=error_code)

def get_user_orders(user_account):
    try:
        orders = session.query(Order).filter(Order.user_account == user_account).all()
        return orders
    except SQLAlchemyError as e:
        app_logger.error(f"Get user order error：{str(e)}")
        flash(f"無法獲取訂單資訊，請稍後再試。錯誤訊息：{str(e)}")
        return []

def get_order_by_id(order_id):
    try:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        return order
    except SQLAlchemyError as e:
        app_logger.error("Get order error %s", e)
        flash("無法獲取訂單資訊，請稍後再試。")
        return None

def get_order_items(order_id):
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

def update_order(order_id, new_order_data):
    try:
        # 查詢指定訂單
        order = session.query(Order).filter(Order.order_id == order_id).first()

        # 檢查訂單是否存在
        if not order:
            app_logger.error("訂單不存在", "warning")
            return None

        # 檢查是否有權修改此訂單
        if order.user_account != current_user.user.user_account:
            app_logger.error("您無權修改此訂單", "warning")
            return None

        # 更新訂單的相應內容
        for field, value in new_order_data.items():
            setattr(order, field, value)

        # 提交事務
        session.commit()
        return order_id

    except SQLAlchemyError as e:
        # 更新失敗時回滾事務並顯示錯誤 Flash 訊息
        session.rollback()
        app_logger.error(f"訂單修改失敗，請稍後再試。錯誤資訊：{str(e)}")
        return None

def cancel_an_order(order_id):
    try:
        # 查詢要取消的訂單
        order = session.query(Order).filter(Order.order_id == order_id).first()

        # 檢查訂單是否存在
        if not order:
            raise ValueError("訂單不存在")

        # 檢查是否會員是否有權限消此訂單
        if order.user_account != current_user.user.user_account:
            raise PermissionError("您無權取消此訂單")

        # order_status!=0就不可以取消訂單
        if order.order_status != '0':
            raise PermissionError("此訂單無法取消")

        # 在這裡處理取消訂單的邏輯
        order.status = "Cancelled"
        order.order_status = '2'  # 訂單狀態改成 2: 取消

        session.commit()

    except SQLAlchemyError as e:
        # 處理取消訂單的 DB 錯誤
        session.rollback()
        raise PermissionError(f"取消訂單失敗：{str(e)}")
