from flask import Blueprint, render_template

from service.ProductService import get_book_info, get_detail_book_info

from service.CartService import CartService
from flask_login import current_user

productController = Blueprint('productController', __name__)

"""
    取得書籍資訊
    Args:

    Returns:

    Raises:

"""
@productController.route('/', methods=['GET'])
def getProducts():
    data = get_book_info()

    # 購物車數字顯示
    cartService = CartService()
    cart_item_count = 0
    if current_user.is_authenticated:
        cart_item_count = cartService.get_cart_item_count(current_user.user_account)

    return render_template("product/home.html", data=data, cart_item_count=cart_item_count)

"""
    查看詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
@productController.route('/getProduct/<item_id>', methods=['GET'])
def getDetailProductInfo(item_id: str):
    data = get_detail_book_info(item_id)

    # 購物車數字顯示
    cartService = CartService()
    cart_item_count = 0
    if current_user.is_authenticated:
        cart_item_count = cartService.get_cart_item_count(current_user.user_account)

    return render_template("product/index.html", data=data, cart_item_count=cart_item_count)

"""
    TODO 查詢書籍資訊
    Args:

    Returns:

    Raises:

"""
# @productController.route('/searchProduct', methods=['GET'])
# def searchProduct():
#     data = get_book_info(book_name = "物聯網技術手冊")
#     return data.book_name
