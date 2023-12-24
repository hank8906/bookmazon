import logging

from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import login_user, logout_user, current_user, login_required

from enumeration.SystemMessage import UserSystemCode
from exception.BusinessError import BusinessError
from form.ChangePassword import ChangePasswordForm
from form.EditUserProfile import EditUserProfile
from form.ForgotPasswordForm import ForgotPasswordForm
from form.LoginForm import LoginForm
from form.RegistryForm import RegistryForm
from form.ResetPasswordForm import ResetPasswordForm
from model.AuthUser import AuthUser
from model.UserBo import UserBo
from model.UserIdentity import UserIdentity
from service.UserService import add_user_info, authenticate_user, get_user_info, change_user_password, \
    check_existing_user, check_user_email_validity, generate_reset_token, validate_reset_token, mark_token_used, \
    reset_new_password, update_user_profile, send_reset_password_email, check_existing_email, update_user_avatar
from utils import logger

app_logger = logger.setup_logger(logging.INFO)
userController = Blueprint('userController', __name__)

"""
    帳號註冊
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
        user_email = form.user_email.data

        # 檢查顧客是否存在
        # 檢查使用者 email是否註冊或使用
        try:
            check_existing_user(user_account)
            check_existing_email(user_account, user_email)
        except BusinessError as e:
            flash(e.message, 'danger')
            return render_template('login/register.html', form=form)

        user = UserBo(
            user_account=user_account,
            user_name=form.user_name.data,
            user_gender=form.user_gender.data,
            user_password=form.user_password.data,
            user_identification=UserIdentity.CUSTOMER,
            user_email=user_email,
            user_birthday=form.user_birthday.data,
            user_profile_pic=form.user_profile_picture.data
        )

        try:
            add_user_info(user)
            message = UserSystemCode.REGISTER_SUCCESS.value.get('message')
            flash(message, 'success')
            return redirect(url_for('userController.login'))
        except BusinessError as e:
            flash(e.message, 'danger')
            return redirect(url_for('userController.register'))

    return render_template('login/register.html', form=form)

"""
    帳號登入
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

        # 驗證顧客身份
        try:
            authenticate_user(user_account, user_password)
            user = get_user_info(user_account)
            login_user(AuthUser(user=user))
            return redirect(url_for('productController.getProducts'))
        except BusinessError as e:
            flash(e.message, 'danger')
            return redirect(url_for('userController.login'))

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
    message = UserSystemCode.LOGOUT.value.get('message')
    flash(message, 'success')
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
    編輯會員大頭貼
    Args:

    Returns:

    Raises:

"""
@userController.route('/update_profile_picture', methods=['POST'])
@login_required
def update_profile_picture():
    try:
        avatar = request.files['avatar']
        update_user_avatar(current_user.user.user_account, avatar)
    except BusinessError as e:
        flash(e.message, 'danger')
    user_info = get_user_info(current_user.user.user_account)
    return render_template('login/user_profile.html', user_info=user_info)

"""
    更改會員資料
    Args:
        user_name 會員姓名
        user_email 會員信箱
        user_birthday 會員生日
    Returns:

    Raises:

"""

@userController.route('edit_user_profile', methods=['GET', 'POST'])
@login_required
def edit_user_profile():
    form = EditUserProfile()
    if form.validate_on_submit():
        try:
            update_user_profile(current_user.user.user_account, form.user_name.data, form.user_email.data,
                                form.user_birthday.data)
            message = UserSystemCode.UPDATE_USER_INFO_SUCCESS.value.get('message')
            flash(message, 'success')
            return redirect(url_for('userController.edit_user_profile'))
        except BusinessError as e:
            app_logger.error('Failed to update user information: %s', e)
            flash(e.message, 'danger')
            return redirect(url_for('userController.edit_user_profile'))

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

@userController.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    # 檢查用戶是否登入，如果沒有，導向到登入頁面
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        try:
            change_user_password(current_user.user.user_account, current_password, new_password)
            message = UserSystemCode.UPDATE_PASSWD_SUCCESS.value.get('message')
            flash(message, 'success')
            return redirect(url_for('userController.change_password'))
        except BusinessError as e:
            flash(e.message, 'danger')
            return redirect(url_for('userController.change_password'))

    return render_template('login/change_password.html', form=form)

"""
    申請忘記密碼
    Args:
        user_account 帳號
        user_current_password 現有的密碼
        user_new_password 新的密碼
    Returns:

    Raises:
"""
@userController.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user_email = form.user_email.data
        app_logger.debug(user_email)

        try:
            # 驗證會員電子郵件地址是否存在
            check_user_email_validity(user_email)
            # 電子郵件地址有存在才再寄信出去
            token = generate_reset_token(user_email)
        except BusinessError as e:
            flash(e.message, 'danger')
            return redirect(url_for('userController.forgot_password'))

        send_reset_password_email(token=token, user_email=user_email)
        message = UserSystemCode.RESET_EMAIL_SENT.value.get('message')
        flash(message, 'success')
        return redirect(url_for('userController.login'))

    return render_template('login/forgot_password.html', form=form)

"""
    （忘記密碼）重設新密碼
    Args:
        user_account 帳號
        user_current_password 現有的密碼
        user_new_password 新的密碼
    Returns:

    Raises:
"""
@userController.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token: str):
    # 在 GET 請求時進行令牌驗證
    try:
        validate_reset_token(token)
    except BusinessError as e:
        return render_template('common/403.html', error_message=e.message)

    form = ResetPasswordForm()
    if form.validate_on_submit():
        # 在 POST 請求時處理表單提交
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        try:
            # 變更密碼
            reset_new_password(token, new_password, confirm_password)
            # 註記 Token 用過了
            mark_token_used(token)
            message = UserSystemCode.UPDATE_PASSWD_SUCCESS.value.get('message')
            flash(message, 'success')
            return redirect(url_for('userController.login'))
        except BusinessError as e:
            return render_template('common/403.html', error_message=e.message)

    return render_template('login/reset_password.html', form=form, token=token)
