import logging
import secrets
from datetime import datetime, timedelta

from flask import url_for
from sqlalchemy import delete, update
from sqlalchemy import select, and_
from werkzeug.security import generate_password_hash, check_password_hash

from model.PasswordResetToken import PasswordResetToken
from model.User import User
from model.UserBo import UserBo
from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)


# 在 UserService 中新增 authenticate_user 函式
def authenticate_user(user_account: str, user_password: str):
    try:
        # 查詢使用者資訊
        user_obj: User = session.scalars(select(User).where(User.user_account == user_account)).one()

        # 驗證密碼是否正確
        if check_password_hash(user_obj.user_password, user_password):
            # 更新最後登入時間
            user_obj.update_datetime = datetime.now()

            # 提交更改到資料庫
            session.commit()
            return True
        else:
            return False

    except Exception as e:
        app_logger.error('Authentication failed: %s', e)
        return False


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
        raise e


# 檢查使用者帳戶是否已存在的函數
def check_existing_user(user_account: str):
    try:
        existing_user = session.scalars(select(User).where(User.user_account == user_account)).first()
        return existing_user is not None
    except Exception as e:
        app_logger.error('Error checking existing user: %s', e)
        return False


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
    刪除使用者資訊
    Args:
        user_account: 使用者帳號

    Returns:


    Raises:

"""


def delete_user_info(user_account: str):
    try:
        statement = delete(User).where(User.user_account == user_account)
        session.execute(statement)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to delete user information: %s', e)
        raise e
    # 更新理論上不用回傳資料，為方便測試有更新到資料，回傳字串
    return 'deleted'


"""
    更新使用者資訊
    Args:
        user_account: 使用者帳號
        password: 密碼
    Returns:


    Raises:

"""


def update_user_profile(user_account: str, new_user_name: str, new_user_email: str, new_user_birthday: str):
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
        raise e

    # 理論上不用回傳資料，為方便測試有更新到資料，回傳字串
    return 'profile_updated'


"""
    更新使用者資訊
    Args:
        user_account: 使用者帳號
        new_user_email: 新的電子郵件
        new_user_birthday: 新的生日
    Returns:


    Raises:

"""




"""
    修改使用者密碼
    Args:
        user_account: 使用者帳號
        current_password: 當前密碼
        new_password: 新密碼
    Returns:
        是否成功修改密碼

    Raises:

"""


def change_user_password(user_account: str, current_password: str, new_password: str):
    try:
        # 驗證當前密碼是否正確
        if not authenticate_user(user_account, current_password):
            app_logger.error('Failed to change password. Incorrect current password.')
            return False
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
        # 更新密碼
        statement = update(User).where(User.user_account == user_account).values(user_password=hashed_password)
        session.execute(statement)
        session.commit()

        app_logger.info('Password changed successfully.')
        return True
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to change user password: %s', e)
        return False


"""
    變更密碼
    Args:
        user_account: 使用者帳號
        current_password: 原始密碼
        new_password: 欲變更密碼
    Returns:


    Raises:

"""


def user_exists_and_email_correct(self, user_account, email):
    try:
        # 檢查會員是否存在並且電子郵件正確
        query = select([UserBo]).where(and_(UserBo.user_account == user_account, UserBo.email == email))
        result = session.execute(query).fetchone()
        return result is not None
    except Exception as e:
        app_logger.error('Error checking user existence and email correctness: %s', e)
        return False


def check_user_email_validity(user_email: str):
    try:
        # 檢查用戶是否存在
        existing_user = session.scalars(select(User).where(User.user_email == user_email)).first()
        return existing_user is not None
    except Exception as e:
        app_logger.error('Error checking user email validity: %s', e)
        return False


def generate_random_token():
    return secrets.token_urlsafe(32)


def save_password_reset_token_to_database(token_obj: PasswordResetToken):
    try:
        # 保存密碼重設 token 到資料庫
        session.add(token_obj)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to save password reset token to database: %s', e)
        raise e


def generate_reset_token(user_email: str):
    try:
        # 檢查用戶是否存在
        if not check_user_email_validity(user_email):
            return None

        # 先清除舊的密碼重設 token ，以確保一個用戶只有一個有效的 token
        clear_old_password_reset_tokens(user_email)

        # 產生重置密碼的 token
        reset_token = generate_random_token()

        # 設定 token 的有效期（例如，300 分鐘）
        update_datetime = datetime.now() + timedelta(minutes=300)

        # 建立一個密碼重置 token object ，並儲存到資料庫
        token_obj = PasswordResetToken(user_email=user_email, token=reset_token,
                                       update_datetime=update_datetime,
                                       create_datetime=datetime.now())
        # 儲存到資料庫
        save_password_reset_token_to_database(token_obj)

        return reset_token
    except Exception as e:
        app_logger.error('Error generating reset token: %s', e)
        return None


def clear_old_password_reset_tokens(user_email: str):
    try:
        # 清除舊的密碼重設 token，以確保一個用戶只有一個有效的 token
        session.query(PasswordResetToken).filter(PasswordResetToken.user_email == user_email).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to clear old password reset tokens: %s', e)
        raise e


def validate_reset_token(token: str):
    try:
        # 查询資料庫，查找與 token 匹配的紀錄
        token_obj = session.scalars(select(PasswordResetToken).where(PasswordResetToken.token == token)).one()

        # 檢查 token 是否存在
        if not token_obj:
            app_logger.warning('Reset token not found: %s', token)
            return False

        # 检查 token 是否過期
        current_time = datetime.now()
        if token_obj.update_datetime and current_time > token_obj.update_datetime:
            app_logger.warning('Reset token expired: %s', token)
            return True

        # 如果驗證通過，返回 token 對應的用户 gmail
        return token_obj.user_email

    except Exception as e:
        app_logger.error('Error validating reset token: %s', e)
        return False


def invalidate_reset_token(token: str):
    try:
        # 查询資料庫，查找與 token 匹配的紀錄
        token_obj = session.scalars(select(PasswordResetToken).where(PasswordResetToken.token == token)).one()

        # 檢查 token 是否存在
        if not token_obj:
            app_logger.warning('Reset token not found: %s', token)
            return False

        # 更新 token 的狀態，可以将其標記为已使用 或者 直接從資料庫中删除
        token_obj.used = True  # 如果 model 有一个表示 token 是否已使用的 string ，可以設置為 True
        token_obj.used_datetime = datetime.now()  # 可以紀錄 token 的使用时间

        # 提交更改到資料庫
        session.commit()

        return True

    except Exception as e:
        app_logger.error('Error invalidating reset token: %s', e)
        return False


def reset_new_password(token: str, new_password: str):
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
        return True
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to change user password: %s', e)
        return False
