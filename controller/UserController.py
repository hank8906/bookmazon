from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, render_template, session
from model.UserBo import UserBo
from service.UserService import add_user_info, authenticate_user, get_user_info, update_user_profile, \
    change_user_password, check_existing_user
import logging
from utils import logger

# 增加了flask_login
from flask_login import login_user, logout_user


app_logger = logger.setup_logger(logging.INFO)
userController = Blueprint('userController', __name__)


@userController.route('/register', methods=['GET', 'POST'])
def register():
    # 此判斷式，確定使用者輸入資料時，才執行以下步驟
    if request.method == 'POST':
        user_account = request.form['user_account']

        # 檢查使用者是否存在
        if check_existing_user(user_account):
            # 如果使用者存在，導向 already_exist_account 的頁面
            return render_template('already_exist_account.html')

        user = UserBo(
            user_account=user_account,
            user_name=request.form['user_name'],
            user_password=request.form['user_password'],
            user_identification="1",
            user_email=request.form['user_email'],
            user_birthday=request.form['user_birthday']
        )

        try:
            add_user_info(user)
            return redirect(url_for('userController.login'))
        except Exception as e:
            app_logger.error('Failed to add user information: %s', e)
            return render_template('401.html')

    return render_template('register.html')


@userController.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_account = request.form['user_account']
        user_password = request.form['user_password']

        # 使用 UserService 中的函數來驗證用戶帳戶和密碼
        if authenticate_user(user_account, user_password):
            session['user_account'] = user_account

            # login_user
            user = get_user_info(user_account)
            login_user(user)

            flash('Login successful!', 'success')
            return redirect(url_for('indexController.index'))
        # else:
        # flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')


"""
    登出
    Args:

    Returns:

    Raises:

"""


@userController.route('/logout', methods=['GET'])
def logout():
    session.pop('user_account', None)

    logout_user() # 更動

    flash('Logout successful!', 'success')
    return redirect(url_for('userController.login'))


# 保護路由的範例
@userController.route('/protected_route', methods=['GET'])
def protected_route():
    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if 'user_account' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('userController.login'))

    # 這裡可以放您想要保護的內容
    return render_template('protected_route.html')


@userController.route('/user_profile', methods=['GET'])
def user_profile():
    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if 'user_account' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('userController.login'))

    # 取得用戶資訊，這裡假設有一個名為 get_user_info 的函數可以取得用戶資訊
    user_account = session['user_account']
    user_info = get_user_info(user_account)

    return render_template('user_profile.html', user_info=user_info)


@userController.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if 'user_account' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('userController.login'))

    if request.method == 'POST':
        user_account = session['user_account']
        new_user_email = request.form['new_user_email']
        new_user_birthday = request.form['new_user_birthday']

        # 使用 UserService 中的函數來更新用戶資料
        if update_user_profile(user_account, new_user_email, new_user_birthday):
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('userController.user_profile'))
        else:
            flash('Failed to update profile. Please try again.', 'error')

    # 取得用戶資訊，這裡假設有一個名為 get_user_info 的函數可以取得用戶資訊
    user_account = session['user_account']
    user_info = get_user_info(user_account)

    return render_template('update_profile.html', user_info=user_info)


####################################################################

@userController.route('/change_password', methods=['GET', 'POST'])
def change_password():
    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if 'user_account' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('userController.login'))

    if request.method == 'POST':
        user_account = session['user_account']
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        # 使用 UserService 中的函數來修改用戶密碼
        if change_user_password(user_account, current_password, new_password):
            flash('Password changed successfully!', 'success')
            return redirect(url_for('userController.user_profile'))
        else:
            flash('Failed to change password. Please check your current password.', 'error')

    return render_template('change_password.html')

########
