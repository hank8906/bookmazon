from datetime import datetime
from flask import Blueprint, render_template
from service.TestService import *

testController = Blueprint('testController', __name__)

"""
    新增使用者資訊
    Args:

    Returns:
    

    Raises:

"""
@testController.route('/add', methods=['GET'])
def add():
    user = User(
        user_account="john_doe",
        user_password='password123',
        user_identification='A',
        user_email='john@example.com',
        user_birthday='1990-01-15',
        update_datetime=datetime.now(),
        create_datetime=datetime.now()
    )

    add_user_info(user)
    return render_template('index.html')

"""
    取得使用者資訊
    Args:

    Returns:

    Raises:

"""
@testController.route('/get', methods=['GET'])
def get():
    data = get_user_info(user_account="john doe")
    return data.user_account

"""
    刪除使用者資訊
    Args:

    Returns:


    Raises:

"""
@testController.route('/delete', methods=['GET'])
def delete():
    data = delete_user_info(user_account="john doe")
    return data

"""
    更新使用者資訊
    Args:

    Returns:


    Raises:

"""
@testController.route('/update', methods=['GET'])
def update():
    data = update_user_info(user_account="john doe", password="123456")
    return data
