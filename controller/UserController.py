import logging

from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, current_user, login_required

from form.ChangePassword import ChangePasswordForm
from form.EditUserProfile import EditUserProfile
from form.ForgetPassword import ForgetPassword
from form.LoginForm import LoginForm
from form.RegistryForm import RegistryForm
from form.ResetPasswordForm import ResetPasswordForm
from model.AuthUser import AuthUser
from model.UserBo import UserBo
from model.UserIdentity import UserIdentity
from service.UserService import add_user_info, authenticate_user, get_user_info, change_user_password, \
    check_existing_user, check_user_email_validity, generate_reset_token, validate_reset_token, invalidate_reset_token, \
    reset_new_password, update_user_profile
from utils import logger
from utils.EmailUutil import send_email

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
        user_gender 性別
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
            return render_template('login/register.html', form=form)

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

    return render_template('login/register.html', form=form)


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

        if authenticate_user(user_account, user_password):
            user = get_user_info(user_account)
            auth_user = AuthUser(user=user)
            login_user(auth_user)
            return redirect(url_for('productController.getProducts'))
        else:
            flash('登入失敗！請您確認帳號、或密碼是否輸入有誤。', 'danger')

    return render_template('login/login.html', form=form)


"""
    登出
    Args:

    Returns:

    Raises:

"""


@userController.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('登出成功！', 'success')
    return redirect(url_for('userController.login'))


"""
    會員資料
    Args:

    Returns:

    Raises:

"""


@userController.route('/user_profile', methods=['GET'])
@login_required
def user_profile():
    user_info = get_user_info(current_user.user.user_account)
    return render_template('login/user_profile.html', user_info=user_info)


"""
    更改會員資料
    Args:
        user_name
        user_email
        user_birthday
    Returns:

    Raises:

"""


@userController.route('edit_user_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    form = EditUserProfile()
    if form.validate_on_submit():
        try:
            # current_user.user.user_name = form.user_name.data
            # current_user.user.user_email = form.user_email.data
            # current_user.user.user_birthday = form.user_birthday.data

            # 使用服務函數更新用戶資料
            update_user_profile(current_user.user.user_account, form.user_name.data, form.user_email.data, form.user_birthday.data)

            flash('會員資料更新成功！', 'success')
            return redirect(url_for('userController.user_profile'))
        except Exception as e:
            app_logger.error('Failed to update user information: %s', e)
            flash('會員資料更新失敗，清稍後嘗試。', 'danger')
            return render_template('401.html')
    # 表單上顯示當前的會員資料
    form.user_name.data = current_user.user.user_name
    form.user_email.data = current_user.user.user_email
    form.user_birthday.data = current_user.user.user_birthday

    return render_template('login/edit_user_profile.html', form=form)


"""
    更換密碼
    Args:
        user_account 帳號
        user_current_password 現有的密碼
        user_new_password 新的密碼
    Returns:

    Raises:
"""


# update_user_profile function

@userController.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        # 修改這一行，確保在 session 中儲存了用戶的帳號
        if change_user_password(current_user.user.user_account, current_password, new_password):
            flash('更換密碼成功!', 'success')
            return redirect(url_for('userController.user_profile'))
        else:
            flash('更換密碼失敗，請重新嘗試', 'danger')
            return redirect(url_for('userController.change_password'))

    return render_template('login/change_password.html', form=form)


@userController.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    try:
        app_logger.info('forget_password')
        form = ForgetPassword()

        if form.validate_on_submit():
            app_logger.info('validate_on_submit')

            user_email = form.user_email.data
            app_logger.info(user_email)

            try:
                if check_user_email_validity(user_email):
                    reset_token = generate_reset_token(user_email)
                    subject = "Password Reset Request"
                    body = f"Click the following link to reset your password: http://127.0.0.1:5001/user/reset_password/{reset_token}"
                    send_email(reset_token, subject, body)
                    return redirect(url_for('userController.login'))
                else:
                    raise ValueError('Invalid email address')

            except Exception as e:
                app_logger.error('Error processing forget password request: %s', e)
                flash('發生錯誤，請稍後再試。', 'danger')

        return render_template('login/forget_password.html', form=form)

    except Exception as e:
        app_logger.error('An unexpected error occurred: %s', e)
        flash('發生意外錯誤，請聯繫系統管理員。', 'danger')
        return render_template('401.html')


@userController.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    if not token:
        flash('缺少重設密碼令牌', 'danger')
        return render_template('401.html')

    # 在 GET 請求時進行令牌驗證
    is_valid = validate_reset_token(token)
    if not is_valid:
        flash('重設密碼令牌無效或已過期', 'danger')
        return render_template('404.html')
    try:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            # 在 POST 請求時處理表單提交
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            if new_password == confirm_password:
                if reset_new_password(token, new_password):
                    # 使重設令牌無效
                    invalidate_reset_token(token)
                    flash('密碼已成功重設', 'success')
                    return redirect(url_for('userController.login'))
                else:
                    flash('重設密碼失敗，請重試', 'danger')
            else:
                flash('兩次輸入的密碼不一致，請確保兩次輸入的密碼相同', 'danger')

        return render_template('login/reset_password.html', form=form, token=token)

    except Exception as e:
        app_logger.error('An unexpected error occurred: %s', e)
        flash('發生意外錯誤，請聯繫系統管理員。', 'danger')
        return render_template('404.html')
