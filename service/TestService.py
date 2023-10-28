from utils.dbUtil import session
from sqlalchemy import select, delete, update
from model.User import User
from utils import logger
import logging

app_logger = logger.setup_logger(logging.INFO)

"""
    新增使用者資訊
    Args:
        user: 使用者
        
    Returns:
    使用者資訊

    Raises:
            
"""
def add_user_info(user: User):
    try:
        app_logger.info("Hello")
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        app_logger.error('Failed to add user information: %s', e)
        raise e

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
