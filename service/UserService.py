from datetime import datetime

from model.UserBo import UserBo
from utils.dbUtil import session
from sqlalchemy import select, delete, update
from model.User import User
from utils import logger
import logging

app_logger = logger.setup_logger(logging.INFO)


# 在 UserService 中新增 authenticate_user 函式
def authenticate_user(user_account: str, user_password: str):
    try:
        # 查詢使用者資訊
        user_obj = session.scalars(select(User).where(User.user_account == user_account)).one()

        # 驗證密碼是否正確
        if user_obj.user_password == user_password:
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
    user = User(
        user_account=user_bo.user_account,
        user_password=user_bo.user_password,
        user_identification=user_bo.user_identification,
        user_email=user_bo.user_email,
        user_birthday=user_bo.user_birthday,
        update_datetime=datetime.now(),
        create_datetime=datetime.now()
    )
    try:
        app_logger.info("Hello")
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to add user information: %s', e)
        raise e


# 檢查使用者帳戶是否已存在的函數
def check_existing_user(user_account):
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
    # CRUD 只有查詢不需要做 commit、rollback
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


def update_user_profile(user_account: str, new_user_email: str, new_user_birthday: str):
    try:
        statement = update(User).where(User.user_account == user_account).values(
            user_email=new_user_email,
            user_birthday=new_user_birthday
        )
        session.execute(statement)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to update user profile: %s', e)
        raise e

    # 更新理論上不用回傳資料，為方便測試有更新到資料，回傳字串
    return 'profile_updated'


def change_user_password(user_account: str, current_password: str, new_password: str):
    try:
        # 驗證當前密碼是否正確
        if not authenticate_user(user_account, current_password):
            app_logger.error('Failed to change password. Incorrect current password.')
            return False

        # 更新密碼
        statement = update(User).where(User.user_account == user_account).values(user_password=new_password)
        session.execute(statement)
        session.commit()

        app_logger.info('Password changed successfully.')
        return True
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to change user password: %s', e)
        return False


"""
    更新使用者資訊
    Args:
        user_account: 使用者帳號
        new_user_email: 新的電子郵件
        new_user_birthday: 新的生日
    Returns:


    Raises:

"""


def update_user_info(user_account: str, password: str):
    try:
        statement = update(User).where(User.user_account == user_account).values(user_password=password)
        session.execute(statement)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to update user information: %s', e)
        raise e

    # 更新理論上不用回傳資料，為方便測試有更新到資料，回傳字串
    return 'updated'


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