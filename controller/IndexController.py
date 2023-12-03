from flask import Blueprint, render_template

# 顯示購物車內商品數量
from service.CartService import CartService
from flask_login import current_user
#

indexController = Blueprint('indexController', __name__)


@indexController.route('/')
def index():

    # 購物車數字顯示
    cartService = CartService()
    cart_item_count = 0
    if current_user.is_authenticated:
        cart_item_count = cartService.get_cart_item_count(current_user.user_account)

    return render_template('index.html', cart_item_count=cart_item_count)
    # return render_template('index.html')
