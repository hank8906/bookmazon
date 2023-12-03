from flask import Blueprint, request, flash, redirect, url_for, render_template
from service.CartService import CartService
from flask_login import login_required, current_user

cartController = Blueprint('cartController', __name__)
cartService = CartService()

@cartController.route('/view_cart', methods=['GET'])
@login_required
def view_cart():
    cart_items = cartService.get_cart_items(current_user.user_account)
    total_price = cartService.calculate_total_price(current_user.user_account) # 計算購物車商品總價

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# TODO
@cartController.route('/add_to_cart/<item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    success = cartService.add_to_cart(current_user.user_account, item_id)
    if success:
        flash('商品已加入購物車', 'success')
    else:
        flash('加到購物車失敗', 'warning')
    return redirect(url_for('index'))

# 按下刪除按鈕一次數量減一個
@cartController.route('/remove_from_cart/<cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cartService.remove_from_cart(cart_item_id)
    flash('商品已從購物車移除', 'success')
    return redirect(url_for('cartController.view_cart'))