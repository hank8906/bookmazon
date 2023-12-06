from flask import Blueprint, render_template, json, url_for
from service.ProductService import *

productController = Blueprint('productController', __name__)

"""
    取得書籍資訊
    Args:

    Returns:

    Raises:

"""
@productController.route('/', methods = ['GET'])
def getProducts():
    data = get_book_info()
    return render_template("product/home.html", data=data)


"""
    查看詳細書籍資訊
    Args:

    Returns:

    Raises:

"""
@productController.route('/getProduct/<id>', methods = ['GET'])
def getDetailProductInfo(id):
    data = get_detail_book_info(id)
    return render_template("product/index.html", data=data)


"""
    查詢書籍資訊
    Args:

    Returns:

    Raises:

"""
# @productController.route('/searchProduct', methods=['GET'])
# def searchProduct():
#     data = get_book_info(book_name = "物聯網技術手冊")
#     return data.book_name
