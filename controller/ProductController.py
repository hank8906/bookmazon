import decimal

from _decimal import Decimal
from flask import Blueprint, render_template, request

from service.ProductService import get_book_info, get_detail_book_info, searchProduct, searchProductsByCategory

from service.CartService import get_cart_item_count
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
    cart_item_count = 0
    if current_user.is_authenticated:
        cart_item_count = get_cart_item_count(current_user.user.user_account)

    return render_template("product/home.html", data=data, cart_item_count=cart_item_count)

"""
    查看詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
@productController.route('/getProduct/<item_id>', methods=['GET','POST'])
def getDetailProductInfo(item_id: str):
    data = get_detail_book_info(item_id)

    # 購物車數字顯示
    cart_item_count = 0
    if current_user.is_authenticated:
        cart_item_count = get_cart_item_count(current_user.user.user_account)

    return render_template("product/index.html", data=data, cart_item_count=cart_item_count)

"""
    TODO 查詢書籍資訊
    Args:

    Returns:

    Raises:

"""
# @productController.route('/searchProduct', methods=['GET', 'POST'])
# def search_book_info():
#     if request.method == 'POST':
#         keyword = request.form.get('keyword', '')
#         data = searchProduct(keyword)
#         return render_template("product/search.html", data=data)
#     return render_template("product/home.html")

@productController.route('/searchProductsByCategory',methods=['GET','POST'])
def search_book_filter_info():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        search_field = request.form.get('searchField', '全文')
        min_price = request.form.get('minPrice', 0, type=float)
        max_price = request.form.get('maxPrice', float('inf'), type=float)
        book_category = request.form.get('bookCategory', 'all')

        # 檢查是否有選擇條件
        if search_field == '全文' and book_category == 'all' and min_price == 0 and max_price == float('inf'):
            # 沒有選擇條件，使用 search_book_info
            data = searchProduct(keyword)
        else:
            # 有選擇條件，使用 search_book_filter_info
            data = searchProductsByCategory(keyword, search_field, min_price, max_price, book_category)

        return render_template("product/search.html", data=data)
    return render_template("product/home.html")

@productController.route('/searchProduct', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        search_field = request.form.get('searchField', '全文')
        min_price = Decimal(request.form.get('minPrice')) if request.form.get('minPrice') != '' else Decimal(0)
        max_price = Decimal(request.form.get('maxPrice')) if request.form.get('maxPrice') != '' else Decimal('Infinity')
        book_category = request.form.get('bookCategory', 'all')

        # 檢查是否有選擇條件
        if search_field == '全文' and book_category == 'all' and min_price == 0 and max_price == float('inf'):
            # 沒有選擇條件，使用 search_book_info
            data = searchProduct(keyword)
        else:
            # 有選擇條件，使用 search_book_filter_info
            data = searchProductsByCategory(keyword, search_field, min_price, max_price, book_category)

        return render_template("product/search.html", data=data)
    return render_template("product/home.html")