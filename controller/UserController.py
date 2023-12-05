import logging

from flask import Blueprint, request, redirect, url_for, flash, render_template, session

from form.LoginForm import LoginForm
from form.RegistryForm import RegistryForm
from model.UserBo import UserBo
from model.UserIdentity import UserIdentity
from service.UserService import add_user_info, authenticate_user, get_user_info, update_user_profile, \
    change_user_password, check_existing_user
from utils import logger

# 增加了flask_login
from flask_login import login_user, logout_user


app_logger = logger.setup_logger(logging.INFO)
userController = Blueprint('userController', __name__)

"""
    登入
    Args:
        user_account 帳號
        user_password 密碼
        user_name 名字
        user_email 電子信箱
        user_birthday 生日
    Returns:

    Raises:

"""
@userController.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistryForm()

    if form.validate_on_submit():
        user_account = form.user_account.data

        # Check if the user already exists
        if check_existing_user(user_account):
            flash('這個帳號已經被註冊了，請更換一另組帳號。', 'danger')
            return render_template('register.html', form=form)

        user = UserBo(
            user_account=user_account,
            user_name=form.user_name.data,
            user_gender=form.user_gender.data,
            user_password=form.user_password.data,
            user_identification=UserIdentity.CUSTOMER,
            user_email=form.user_email.data,
            user_birthday=form.user_birthday.data
        )

        try:
            add_user_info(user)
            flash('帳號註冊成功，您可以登入了。', 'success')
            return redirect(url_for('userController.login'))
        except Exception as e:
            app_logger.error('Failed to add user information: %s', e)
            flash('帳號註冊失敗，請您稍候嘗試，或聯繫網站管理人員。', 'danger')
            return render_template('401.html')

    return render_template('register.html', form=form)

"""
    登入
    Args:
        user_account 帳號
        user_password 密碼
    Returns:

    Raises:

"""
@userController.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_account = form.user_account.data
        user_password = form.user_password.data

        # Use your authentication function to validate user credentials
        if authenticate_user(user_account, user_password):
            session['user_account'] = user_account
            flash('登入成功!', 'success')

            # login_user
            user = get_user_info(user_account)
            login_user(user)

            flash('Login successful!', 'success')
            return redirect(url_for('indexController.index'))
        else:
            flash('登入失敗！請您確認帳號、或密碼是否輸入有誤。', 'danger')

    return render_template('login.html', form=form)


"""
    登出
    Args:

    Returns:

    Raises:

"""
@userController.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('登出成功！', 'success')

    logout_user()  # 更動

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
