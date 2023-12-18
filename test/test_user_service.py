import logging
import random
import secrets
import string

import pytest
from sqlalchemy import select
from werkzeug.security import check_password_hash

from enumeration.SystemMessage import UserSystemCode
from exception.BusinessError import BusinessError
from model.User import User
from model.UserBo import UserBo
from service.UserService import authenticate_user, add_user_info, check_user_email_validity, update_user_profile, \
    validate_reset_token, change_user_password, check_existing_user, reset_new_password
from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)


def generate_random_user_account(prefix="user_", length=8):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}{random_string}"


def generate_random_user_email():
    email_prefix = ''.join(random.choices(string.ascii_lowercase, k=8))
    email_suffix = '@example.com'
    return email_prefix + email_suffix


# 使用預設前綴 "user_" 和長度 8 生成隨機 user_account
user_account = generate_random_user_account()
# print(user_account)

# re set token
reset_token = secrets.token_urlsafe(32)


class TestUserService:
    ## 1 驗證會員身分
    # 1.1 測試驗證會員登入的身份 成功 : 驗證會員身分
    @pytest.mark.auth_success
    def test_authenticate_user_success(self):
        try:
            authenticate_user('Justin', '12345')
            assert True
        except BusinessError:
            assert False

    # 1.2 測試驗證會員登入的身份 失敗 : 驗證會員是否存在
    @pytest.mark.auth_failed
    def test_authenticate_user_failed(self):
        try:
            authenticate_user('test_user1', 'password')
            assert False
        except BusinessError:
            assert True

    ## 2 註冊會員資料
    # 2.1 註冊會員資料 成功 : 正確的會員資料
    @pytest.mark.add_user_success
    def test_add_user_success(self):
        user_bo = UserBo(
            user_account=generate_random_user_account(),
            user_password="test_password",
            user_name="TestUser",
            user_gender="M",
            user_identification="1",
            user_email="test@example.com",
            user_birthday="1995-01-01"
        )

        try:
            add_user_info(user_bo)
            assert True
        except BusinessError as e:
            # pytest.fail(f"Unexpected BusinessError: {e}")
            assert False

    # 2.2 註冊會員資料 失敗 : 重複的會員帳號已存在
    @pytest.mark.add_user_failed
    def test_add_user_failed_check_existing(self):
        try:
            check_existing_user('Justin')
            assert False
        except BusinessError:
            assert True

    # 2.3 註冊會員資料 成功 : 檢查使用者 email 註冊 或 使用 成功，因為正確的 email
    @pytest.mark.check_user_email_validity_success
    def test_check_user_email_validity_success(self):
        try:
            check_user_email_validity('rename001@gmail.cc')
            assert True
        except BusinessError:
            assert False

    # 2.4 註冊會員資料 失敗 : 檢查使用者 email 註冊 或 使用 失敗，因為已註冊過的 email
    @pytest.mark.check_user_email_validity_failed
    def test_check_user_email_validity_failed(self):
        try:
            check_user_email_validity('user001@gmail.cc')
            assert False
        except BusinessError:
            assert True

    ## 3 會員資料修改
    # 3.1 會員資料修改 成功 : 正確的資料更新
    @pytest.mark.update_user_profile_success
    def test_update_user_profile_success(self):
        try:
            update_user_profile('test_user_001', 'test_user_Justin', 'Justin@cc.cc', '2002-02-03')
            assert True
        except BusinessError:
            assert False

    # 3.2 會員資料修改 失敗: 更新不存在的使用者
    @pytest.mark.update_user_profile_failed
    def test_update_user_profile_failed(self):
        try:
            update_user_profile('test_user_001_lisa', 'test_user_Justin', 'Justin@cc.cc', '2002-02-03')
            assert False
        except BusinessError:
            assert True

    ## 4 變更會員密碼
    # 4.1 變更會員密碼 成功 : 驗證舊密碼是否正確、更新密碼
    @pytest.mark.change_user_password_success
    def test_change_user_password_success(self):
        try:
            change_user_password("Justin", "12345", "123456")
            user_obj: User = session.scalars(select(User).where(User.user_account == "Justin")).one()
            # 驗證密碼是否正確
            if check_password_hash(user_obj.user_password, "123456"):
                assert True
            else:
                assert False
        except BusinessError:
            assert False
        change_user_password("Justin", "123456", "12345")

    # 4.2 變更會員密碼 失敗 : 驗證舊密碼是否新密碼一樣 ( 舊密碼 = 新密碼 )
    @pytest.mark.change_user_password_failed
    def test_change_user_password_failed(self):
        try:
            change_user_password("Justin", "12345", "12345")
        except BusinessError as e:
            system_code = UserSystemCode.OLD_PASSWORD_NOT_ALLOWED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    ## 5 生成重置密碼的 Token，# generate_reset_token
    # 5.1 生成重置密碼的 Token 成功 : 測試正確生成 token 並儲存到資料庫，used
    # 5.2 生成重置密碼的 Token 失敗 : 測試嘗試將相同的使用者 email 產生兩次 token

    ## 6 驗證重置 token # validate_reset_token 大魔王
    # 6.1.1 驗證重置 token 成功 : 檢查 token 是否存在，註記是否過期，時間是否過期
    # 6.1.2 驗證重置 token 失敗 : 檢查 token 是否存在，註記是否過期，時間是否過期
    @pytest.mark.validate_reset_token_failed
    def test_validate_reset_token_failed(self):
        try:
            validate_reset_token(reset_token)
            assert False
        except BusinessError:
            assert True

    # 6.2 重置新密碼失敗
    @pytest.mark.reset_new_password_failed
    def test_reset_new_password_failed(self):
        with pytest.raises(BusinessError):
            reset_new_password(reset_token, "12345", "12345678")

    ## 7 標記 token 使用過
    # 7.1 標記 token 使用過 成功/失敗 : 查询資料庫，查找與 token 匹配的紀錄
    # 7.2 標記 token 使用過 成功/失敗 : 檢查 token 是否存在，used
    # 7.3 標記 token 使用過 成功/失敗 : 註記 token 已經使用過了
