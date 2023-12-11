from flask import Blueprint, request, redirect, url_for, flash, render_template
from service.OrderService import OrderService
from flask_login import login_required, current_user
from service.CartService import CartService

orderController = Blueprint('orderController', __name__)
orderService = OrderService()
cartService = CartService()

@orderController.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = cartService.get_cart_items(current_user.user.user_account)
    order_id = orderService.add_order(current_user.user.user_account, cart_items)
    if order_id:
        flash("訂單已成功創建", "success")
        return redirect(url_for('orderController.view_order_details', order_id=order_id))
    else:
        flash("結帳失敗", "error")
        return redirect(url_for('cartController.view_cart'))

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
