from flask import Blueprint, request, redirect, url_for, flash, render_template
from service.OrderService import OrderService
from flask_login import login_required, current_user
from service.CartService import CartService

orderController = Blueprint('orderController', __name__)
orderService = OrderService()
cartService = CartService()

"""
    建立訂單
    Args:
        cart_items 購物車項目
    Returns:
        
    Raises:
        
"""
@orderController.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = cartService.get_cart_items(current_user.user.user_account)
    # order_id = orderService.add_order(current_user.user.user_account, cart_items)
    updated_quantities = {}
    for cart_item_tuple in cart_items:
        cart_item, _, _ = cart_item_tuple
        # 取得訂單數量
        input_name = f'quantity-{cart_item.cart_item_id}'
        updated_quantity = request.form.get(input_name, type=int)
        if updated_quantity is not None:
            updated_quantities[cart_item.cart_item_id] = updated_quantity
        else:
            # 訂單數量沒有更動
            updated_quantities[cart_item.cart_item_id] = cart_item.quantity

    order_id = orderService.add_order(current_user.user.user_account, cart_items, updated_quantities)
    if order_id:
        flash(f"訂單已成功創建", "success")
        return redirect(url_for('orderController.view_order_details', order_id=order_id))
    else:
        flash("結帳失敗", "error")
        return redirect(url_for('cartController.view_cart'))

"""
    查看訂單明細
    Args:
        order_id 訂單ID
    Returns:

    Raises:
        
"""
@orderController.route('/view_order_details/<int:order_id>', methods=['GET'])
@login_required
def view_order_details(order_id):
    order = orderService.get_order_by_id(order_id)
    if not order:
        flash("訂單不存在", "warning")
        return redirect(url_for('productController.getProducts'))

    if order.user_account != current_user.user.user_account:
        flash("您無權訪問此訂單", "warning")
        return redirect(url_for('productController.getProducts'))

    order_items = orderService.get_order_items(order_id)
    return render_template('order/viewOrderDetails.html', order=order, order_items=order_items)

"""
    查看所有訂單
    Args:
        user_account 帳號
    Returns:

    Raises:
        None
"""
@orderController.route('/view_order')
@login_required
def view_order():
    user_account = current_user.user.user_account
    orders = orderService.get_user_orders(user_account)

    return render_template('order/viewOrder.html', orders=orders)