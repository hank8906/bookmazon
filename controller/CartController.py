import json

from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from enumeration.SystemMessage import ShoppingCartSystemCode
from exception.BusinessError import BusinessError
from model.JsonMessage import JsonMessage
from service.CartService import CartService

cartController = Blueprint('cartController', __name__)
cartService = CartService()

"""
    查看購物車
    Args:

    Returns:

    Raises:

"""
@cartController.route('/view_cart', methods=['GET'])
@login_required
def view_cart():
    cart_items = cartService.get_cart_items(current_user.user.user_account)
    total_price = cartService.calculate_total_price(current_user.user.user_account)  # 計算購物車商品總價

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

"""
    加入購物車
    Args:

    Returns:

    Raises:

"""
@cartController.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    item_id = request.form.get('item_id')
    quantity = request.form.get('quantity', type=int)
    json_message = JsonMessage()

    try:
        cartService.add_to_cart(current_user.user.user_account, item_id, quantity)
        json_message.system_code = ShoppingCartSystemCode.ADD_ITEM_SUCCESS.value.get('system_code')
        json_message.system_message = ShoppingCartSystemCode.ADD_ITEM_SUCCESS.value.get('message')
    except BusinessError as e:
        json_message.success = False
        json_message.system_code = e.error_code
        json_message.system_message = e.message

    return json.dumps(json_message.__dict__)

"""
    查看購物車購買數量
    Args:

    Returns:

    Raises:

"""
@cartController.route('/viewCartItemQuantity', methods=['GET'])
@login_required
def view_cart_item_quantity():
    json_message = JsonMessage()
    # 購物車數量顯示
    if current_user.is_authenticated:
        cart_item_quantity = cartService.get_cart_item_count(current_user.user.user_account)
        json_message.data = {'cart_item_quantity': cart_item_quantity}
    return json.dumps(json_message.__dict__)

# 按下刪除按鈕一次數量減一個
@cartController.route('/remove_from_cart/<cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cartService.remove_from_cart(cart_item_id)
    flash('商品已從購物車移除', 'success')
    return redirect(url_for('cartController.view_cart'))
