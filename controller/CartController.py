from flask import Blueprint, request, flash, redirect, url_for, render_template
from service.CartService import CartService
from flask_login import login_required, current_user
from flask import jsonify

cartController = Blueprint('cartController', __name__)
cartService = CartService()

@cartController.route('/view_cart', methods=['GET'])
@login_required
def view_cart():
    cart_items = cartService.get_cart_items(current_user.user_account)
    total_price = cartService.calculate_total_price(current_user.user_account) # 計算購物車商品總價

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cartController.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    # form = AddToCartForm()
    # if form.validate_on_submit():
    #     success = cartService.add_to_cart(current_user.user_account, form.item_id.data, form.quantity.data)
    #     return jsonify({'success': success})
    # else:
    #     return jsonify({'success': False})

    # 從請求中獲取資料
    item_id = request.form.get('item_id')
    # quantity = request.form.get('quantity', type=int)

    # 資料驗證
    # if not item_id or not quantity or quantity <= 0:
    #     return jsonify({'success': False, 'message': '參數錯誤!'})
    if not item_id:
        return jsonify({'success': False, 'message': '參數錯誤!'})

    # 業務邏輯
    success = cartService.add_to_cart(current_user.user_account, item_id, 1)
    if success:
        return jsonify({'success': True, 'message': '商品已加入購物車'})
    else:
        return jsonify({'success': False, 'message': '加入購物車失敗'})

# 按下刪除按鈕一次數量減一個
@cartController.route('/remove_from_cart/<cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cartService.remove_from_cart(cart_item_id)
    flash('商品已從購物車移除', 'success')
    return redirect(url_for('cartController.view_cart'))