import logging
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy import update
from werkzeug.security import generate_password_hash, check_password_hash

from enumeration.EmailTemplateEnum import EmailTemplateEnum
from enumeration.SystemMessage import UserSystemCode, CommonSystemCode
from enumeration.TokenStatus import TokenStatus
from exception.BusinessError import BusinessError
from model.PasswordResetToken import PasswordResetToken
from model.User import User
from model.UserBo import UserBo
from utils import logger
from utils.EmailUutil import send_htm_email
from utils.config import params
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)

"""
    驗證使用者身份
    Args:
        user_account 使用者帳號
        user_password 使用者密碼

    Returns:
    使用者資訊

    Raises:

"""


def authenticate_user(user_account: str, user_password: str):
    try:
        # 查詢使用者資訊
        user_obj: User = session.scalars(select(User).where(User.user_account == user_account)).one()
    except Exception as e:
        app_logger.error('Authentication failed: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    # 驗證密碼是否正確
    if not check_password_hash(user_obj.user_password, user_password):
        message = UserSystemCode.LOGIN_FAILED.value.get('message')
        system_code = UserSystemCode.LOGIN_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
    新增使用者資訊
    Args:
        user: 使用者

    Returns:
    使用者資訊

    Raises:

"""


def add_user_info(user_bo: UserBo):
    # 在註冊時儲存使用者密碼的哈希值
    hashed_password = generate_password_hash(user_bo.user_password, method='pbkdf2:sha256')

    user = User(
        user_account=user_bo.user_account,
        user_password=hashed_password,
        user_name=user_bo.user_name,
        user_gender=user_bo.user_gender,
        user_identification=user_bo.user_identification,
        user_email=user_bo.user_email,
        user_birthday=user_bo.user_birthday,
        update_datetime=datetime.now(),
        create_datetime=datetime.now()
    )
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to add user information: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
    檢查使用者帳戶是否已存在
    Args:
        user_account 使用者帳號

    Returns:
        檢查結果

    Raises:
        BusinessError
"""


def check_existing_user(user_account: str):
    try:
        result = session.scalars(select(User).where(User.user_account == user_account)).first()
    except Exception as e:
        app_logger.error('Error checking existing user: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    if result is not None:
        message = UserSystemCode.REGISTERED_ACCOUNT.value.get('message')
        system_code = UserSystemCode.REGISTERED_ACCOUNT.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
    檢查使用者 email 是否註冊 或 使用
    Args:
        user_email 使用者Email

    Returns:
        檢查結果

    Raises:
        BusinessError
"""


def check_existing_email(user_account: str, user_email: str):
    try:
        user = session.scalars(select(User).where(User.user_email == user_email)).first()
    except Exception as e:
        app_logger.error('Error checking existing user: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    # 此 Email 沒有被註冊過
    if user is None:
        return

    # 代表 Email 被同為一會員使用
    if user_account == user.user_account:
        return

    # 目前此 Email 正在被使用當中
    message = UserSystemCode.REGISTERED_EMAILED.value.get('message')
    system_code = UserSystemCode.REGISTERED_EMAILED.value.get('system_code')
    raise BusinessError(error_code=system_code, message=message)


"""
    取得使用者資訊
    Args:
        user_account: 使用者帳號

    Returns:
    使用者資訊

    Raises:

"""


def get_user_info(user_account: str):
    try:
        user_obj = session.scalars(select(User).where(User.user_account == user_account)).one()
    except Exception as e:
        app_logger.error('Failed to query user information: %s', e)
        raise e
    return user_obj


"""
    更新使用者資訊
    Args:
        user_account: 使用者帳號
        new_user_email: 新的電子郵件
        new_user_birthday: 新的生日
    Returns:


    Raises:

"""


def update_user_profile(user_account: str, new_user_name: str, new_user_email: str, new_user_birthday: str):
    # 檢查使用者 email是否註冊或使用
    check_existing_email(user_account, new_user_email)

    try:
        statement = update(User).where(User.user_account == user_account).values(
            user_name=new_user_name,
            user_email=new_user_email,
            user_birthday=new_user_birthday
        )
        session.execute(statement)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to update user profile: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
    修改使用者密碼
    Args:
        user_account: 使用者帳號
        current_password: 當前密碼
        new_password: 新密碼
    Returns:
        是否成功修改密碼

    Raises:
        BusinessError 業務邏輯錯誤

"""


def change_user_password(user_account: str, current_password: str, new_password: str):
    # 驗證舊密碼是否正確
    try:
        authenticate_user(user_account, current_password)
        app_logger.error('Failed to change password. Incorrect current password.')
    except BusinessError:
        message = UserSystemCode.IS_NOT_OLD_PASSWORD.value.get('message')
        system_code = UserSystemCode.IS_NOT_OLD_PASSWORD.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    # 驗證舊密碼是否新密碼一樣
    if current_password == new_password:
        message = UserSystemCode.OLD_PASSWORD_NOT_ALLOWED.value.get('message')
        system_code = UserSystemCode.OLD_PASSWORD_NOT_ALLOWED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    # 更新密碼
    try:
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        statement = update(User).where(User.user_account == user_account).values(user_password=hashed_password)
        session.execute(statement)
        session.commit()
        app_logger.info('Password changed successfully.')
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to change user password: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    # 查詢會員名稱
    try:
        result = session.query(User.user_name, User.user_email).where(User.user_account == user_account).first()
    except Exception as e:
        app_logger.error('Error validating reset token: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    user_name = result[0]
    user_email = result[1]

    # 通知會員密碼變更
    try:
        send_htm_email(EmailTemplateEnum.RESET_PASSWORD, [user_email], user_name=user_name)
    except Exception as e:
        app_logger.error('Failed to send user email notification: %s', e)


"""
    檢查會員email是否存在
    Args:
        user_email: 使用者 email
    Returns:
        email是否存在

    Raises:
        BusinessError 業務邏輯錯誤

"""


def check_user_email_validity(user_email: str):
    try:
        # 檢查會員是否存在
        existing_user = session.scalars(select(User).where(User.user_email == user_email)).first()
    except Exception as e:
        app_logger.error('Error checking user email validity: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    if existing_user is None:
        message = UserSystemCode.EMAIL_NOT_EXISTED.value.get('message')
        system_code = UserSystemCode.EMAIL_NOT_EXISTED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


def send_reset_password_email(token: str, user_email: str):
    # 查詢會員名稱
    try:
        result = session.query(User.user_name).filter(User.user_email == user_email).first()
    except Exception as e:
        app_logger.error('Error validating reset token: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)
    user_name = result[0]

    link = f"http://{params['APP_SEVER_HOST_NAME']}:{params['LISTENING_PORT']}/user/reset_password/{token}"
    send_htm_email(EmailTemplateEnum.FORGOT_PASSWORD, [user_email], user_name=user_name, link=link)


"""
    產生重置密碼使用的 token
    Args:
        user_email: 使用者 email
    Returns:
        email是否存在

    Raises:
        BusinessError 業務邏輯錯誤

"""


def generate_reset_token(user_email: str):
    # 產生重置密碼的 token
    reset_token = secrets.token_urlsafe(32)

    # 設定 token 的有效期（例如，5 分鐘）
    update_datetime = datetime.now() + timedelta(minutes=5)

    # 建立一個密碼重置 token object ，並儲存到資料庫
    token_obj = PasswordResetToken(user_email=user_email,
                                   token=reset_token,
                                   token_status=TokenStatus.NOT_USED.value,
                                   update_datetime=update_datetime,
                                   create_datetime=datetime.now())
    # token object 儲存到資料庫
    try:
        save_password_reset_token_to_database(token_obj)
        return reset_token
    except Exception as e:
        app_logger.error('Error generating reset token: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
   儲存重置密碼使用的 token
    Args:
        user_email: 使用者 email
    Returns:
        email是否存在

    Raises:
        BusinessError 業務邏輯錯誤

"""


def save_password_reset_token_to_database(token_obj: PasswordResetToken):
    try:
        # 保存密碼重設 token 到資料庫
        session.add(token_obj)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to save password reset token to database: %s', e)
        raise e


"""
   驗證發出去 token 是否存在且有效
    Args:
        token: 令牌
    Returns:
        

    Raises:
        BusinessError 業務邏輯錯誤

"""


def validate_reset_token(token: str):
    try:
        # 查询資料庫，查找與 token 匹配的紀錄
        token_obj = session.scalars(select(PasswordResetToken).where(PasswordResetToken.token == token)).one()
    except Exception as e:
        app_logger.error('Error validating reset token: %s', e)
        message = CommonSystemCode.DATABASE_FAILED.value.get('message')
        system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    message = UserSystemCode.EXPIRED_TOKEN.value.get('message')
    system_code = UserSystemCode.EXPIRED_TOKEN.value.get('system_code')

    # 檢查 token 註記是否過期
    if token_obj.token_status == TokenStatus.EXPIRED.value:
        raise BusinessError(error_code=system_code, message=message)

    # 檢查 token 時間是否過期
    current_time = datetime.now()
    if token_obj.update_datetime and current_time > token_obj.update_datetime:
        app_logger.warning('Reset token expired: %s', token)

        # 註記 token 過期了
        try:
            mark_token(token=token, mark=TokenStatus.EXPIRED)
        except BusinessError as e:
            raise e

        raise BusinessError(error_code=system_code, message=message)


"""
   （忘記密碼）重設新密碼
    Args:
        token 令牌
        confirm_password 確認新密碼
        new_password 新密碼
    Returns:


    Raises:
        BusinessError 業務邏輯錯誤

"""


def reset_new_password(token: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        message = UserSystemCode.PASSWORD_NOT_SAME.value.get('message')
        system_code = UserSystemCode.PASSWORD_NOT_SAME.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)

    try:
        user_account_list = (session.query(User.user_account)
                             .join(PasswordResetToken, User.user_email == PasswordResetToken.user_email)
                             .where(PasswordResetToken.token == token)
                             .first())
        user_account: str = user_account_list[0]
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        # 更新密碼
        statement = update(User).where(User.user_account == user_account).values(user_password=hashed_password)
        session.execute(statement)
        session.commit()
        app_logger.info('Password changed successfully.')
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to change user password: %s', e)
        message = UserSystemCode.EXPIRED_TOKEN.value.get('message')
        system_code = UserSystemCode.EXPIRED_TOKEN.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)


"""
   註記 token 用過了
    Args:
        token: 令牌
    Returns:


    Raises:
        BusinessError 業務邏輯錯誤

"""


def mark_token_used(token: str):
    # 查询資料庫，查找與 token 匹配的紀錄
    # 註記 token 已經使用過了
    try:
        token_obj = session.scalars(select(PasswordResetToken).where(PasswordResetToken.token == token)).one()
        app_logger.warning('Token not found: %s', token)
        mark_token(token=token, mark=TokenStatus.USED)
    except BusinessError as e:
        raise e


"""
   註記 token
    Args:
        token 令牌
        mark 註記
    Returns:


    Raises:
        BusinessError 業務邏輯錯誤

"""


def mark_token(token: str, mark: TokenStatus):
    try:
        statement = update(PasswordResetToken).where(PasswordResetToken.token == token).values(
            token_status=mark.value, update_datetime=datetime.now())
        session.execute(statement)
        session.commit()
    except Exception as e:
        app_logger.error('Error invalidating reset token: %s', e)
        message = UserSystemCode.EXPIRED_TOKEN.value.get('message')
        system_code = UserSystemCode.EXPIRED_TOKEN.value.get('system_code')
        raise BusinessError(error_code=system_code, message=message)
