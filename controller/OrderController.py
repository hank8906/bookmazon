from flask import Blueprint, request, redirect, url_for, flash, render_template

from enumeration.SystemMessage import OrderSystemCode
from exception.BusinessError import BusinessError
from model.CheckoutBo import CheckoutBo
from service.OrderService import add_order, get_order_by_id, get_order_items, get_user_orders, \
    cancel_an_order
from flask_login import login_required, current_user
from service.CartService import get_cart_items

orderController = Blueprint('orderController', __name__)

"""
    建立會員的訂單
    Args:
        cart_items 購物車項目
    Returns:
        
    Raises:
        
"""

@orderController.route('/checkout', methods=['POST'])
@login_required
def checkout():
    # 拿到目前使用者的購物車商品
    cart_items = get_cart_items(current_user.user.user_account)

    checkout_bo = CheckoutBo(
        user_account=current_user.user.user_account,
        cart_items=cart_items,
        recipient_name=request.form.get('recipient-name'),
        recipient_city=request.form.get('recipient-city'),
        recipient_district=request.form.get('recipient-district'),
        recipient_address=request.form.get('recipient-address'),
        payment_method=request.form.get('payment_method')
    )

    # 建立訂單
    try:
        order_id = add_order(checkout_bo)
        message = OrderSystemCode.PLACE_ORDER_SUCCESS.value.get('message')
        flash(message, "success")
        return redirect(url_for('orderController.view_order_details', order_id=order_id))
    except BusinessError as e:
        flash(e.message, "danger")
        return redirect(url_for('cartController.view_cart'))

"""
    查看會員的訂單明細
    Args:
        order_id 訂單ID
    Returns:

    Raises:
        
"""

@orderController.route('/view_order_details/<int:order_id>', methods=['GET'])
@login_required
def view_order_details(order_id):
    # 勞取指定訂單
    try:
        order = get_order_by_id(order_id)
    except BusinessError as e:
        # 訂單不存在
        flash(e.message, "warning")
        return redirect(url_for('productController.getProducts'))

    # 檢查當前使用者是否有權訪問此訂單
    if order.user_account != current_user.user.user_account:
        message = OrderSystemCode.NOT_ORDER_OWNER.value.get('message')
        flash(message, "warning")
        return redirect(url_for('productController.getProducts'))

    # 使用 get_order_items 函式獲取訂單項目
    order_items = []
    try:
        order_items = get_order_items(order_id)
    except BusinessError as e:
        flash(e.message, "warning")

    # 將訂單和訂單項目傳遞給模板，並呈現訂單詳細資訊的頁面
    return render_template('order/viewOrderDetails.html', order=order, order_items=order_items)

"""
    查看會員所有的訂單
    Args:
        user_account 帳號
    Returns:

    Raises:
        None
"""

@orderController.route('/view_order')
@login_required
def view_order():
    # 獲取當前使用者的帳號
    user_account = current_user.user.user_account

    # 使用 get_user_orders 函式獲取該使用者的所有訂單
    orders = []
    try:
        orders = get_user_orders(user_account)
    except BusinessError as e:
        flash(e.message, "warning")

    # 將訂單列表傳遞給模板，並呈現訂單總覽的頁面
    return render_template('order/viewOrder.html', orders=orders)

# 取消訂單
@orderController.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    # 獲取要取消的訂單
    order = get_order_by_id(order_id)

    # 檢查訂單是否存在
    if not order:
        flash("訂單不存在", "warning")
        return redirect(url_for('productController.getProducts'))

    # 檢查是否有權取消此訂單
    if order.user_account != current_user.user.user_account:
        flash("您無權取消此訂單", "warning")
        return redirect(url_for('productController.getProducts'))
    else:
        cancel_an_order(order_id)
        # 在這裡處理取消訂單的邏輯
        flash("訂單取消中，等待管理人員審核", "success")
        return redirect(url_for('orderController.view_order'))
