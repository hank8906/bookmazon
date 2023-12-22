import logging
import random
import secrets
import string
from datetime import datetime

import pytest
from sqlalchemy import select
from werkzeug.security import check_password_hash

from enumeration import TokenStatus
from enumeration.SystemMessage import UserSystemCode, CommonSystemCode
from exception.BusinessError import BusinessError
from model.PasswordResetToken import PasswordResetToken
from model.User import User
from model.UserBo import UserBo
from service.UserService import authenticate_user, add_user_info, check_user_email_validity, update_user_profile, \
    validate_reset_token, change_user_password, check_existing_user, reset_new_password, generate_reset_token, \
    mark_token, get_user_info, send_reset_password_email, mark_token_used
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


class TestUserService:
    ## 1 驗證會員身分
    # authenticate_user(user_account, user_password)
    # 1.1 測試驗證會員登入的身份 成功 : 驗證會員身分
    @pytest.mark.auth_success
    def test_authenticate_user_success(self):
        try:
            authenticate_user('PotonLee', '123')
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

    # 1.3 確認 hash 密碼成功
    # check_password_hash
    # PotonLee
    # 123
    @pytest.mark.check_password_hash_success
    def test_check_password_hash_success(self):
        try:
            check_password_hash(
                'pbkdf2:sha256:600000$gyHYvHdvTkZjIzy6$f8fe0a2683b0093899452fae7607527263775090839fc04761c010767725c8b6',
                '123')
            assert True
        except BusinessError:
            assert False

    # 1.4 確認 hash 密碼失敗
    @pytest.mark.check_password_hash_failed
    def test_check_password_hash_failed(self):
        try:
            check_password_hash(
                'pbkdf2:sha256:600000$gyHYvHdvTkZjIzy6$f8fe0a2683b0093899452fae7607527263775090839fc04761c010767725c8b6',
                '12345')
        except BusinessError as e:
            system_code = UserSystemCode.LOGIN_FAILED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    # 1.5 取得使用者資訊成功
    @pytest.mark.get_user_info_success
    def test_get_user_info_success(self):
        try:
            get_user_info('PotonLee')
            user_obj: User = session.scalars(select(User).where(User.user_account == "PotonLee")).one()
            # 驗證密碼是否正確
            if user_obj:
                assert True
            else:
                assert False
        except BusinessError:
            assert False

    # 1.6 取得使用者資訊失敗
    """
    # NO_RESULT_FOUND
    @pytest.mark.get_user_info_failed
    def test_get_user_info_failed(self):
        try:
            get_user_info('PotonLeeLee')
            assert True
        except BusinessError:
            assert False
    """
    ## 2 註冊會員資料
    # add_user_info(user_bo)
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
    # check_user_email_validity(email)
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
    # update_user_profile(user_account, new_user_name, new_user_email, new_user_birthday)
    # 3.1 會員資料修改 成功 : 正確的資料更新

    @pytest.mark.update_user_profile_success
    def test_update_user_profile_success(self):
        try:
            update_user_profile('test_user_001',
                                'test_user_Justin',
                                'Justin@cc.cc',
                                '2002-02-03')
            assert True
        except BusinessError:
            assert False

    # 3.2 會員資料修改 失敗: 更新不存在的使用者
    @pytest.mark.update_user_profile_failed
    def test_update_user_profile_failed(self):
        try:
            update_user_profile('test_user_001_lisa',
                                'test_user_Justin',
                                'Justin@cc.cc',
                                '2002-02-03')
            assert False
        except BusinessError:
            assert True

    ## 4 變更會員密碼
    # change_user_password(user_account, current_password, new_password)
    # 4.1 變更會員密碼 成功 : 驗證舊密碼是否正確、更新密碼
    @pytest.mark.change_user_password_success
    def test_change_user_password_success(self):
        try:
            change_user_password("Lisa", "123", "12345")
            user_obj: User = session.scalars(select(User).where(User.user_account == "Lisa")).one()
            # 驗證密碼是否正確
            if check_password_hash(user_obj.user_password, "12345"):
                assert True
            else:
                assert False
        except BusinessError:
            assert False
        change_user_password("Lisa", "12345", "123")

    # 4.2 變更會員密碼 失敗 : 驗證舊密碼是否新密碼一樣 ( 舊密碼 = 新密碼 )
    @pytest.mark.change_user_password_failed
    def test_change_user_password_failed(self):
        try:
            change_user_password("Bob", "12345", "12345")
        except BusinessError as e:
            system_code = UserSystemCode.OLD_PASSWORD_NOT_ALLOWED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    # 4.3 傳送重置信箱，從資料庫尋找會員名稱 成功 發生 RuntimeError :
    """
    @pytest.mark.send_reset_password_email_success
    def test_send_reset_password_email_success(self):
        try:
            send_reset_password_email('sU2UEYIho2hrhC9-U7N17FXMMu9Bs6Slmw18ueq0tKU','s1081625@yzu.edu.tw')
        except BusinessError as e:
            system_code = CommonSystemCode.DATABASE_FAILED.value.get('message')
            if e.error_code == system_code:
                assert True
            else:
                assert False
    """

    ## 5. 生成重置密碼的 Token，
    # generate_reset_token(user_email)
    # 5.1 生成重置密碼的 Token 成功 : 測試正確生成 Token 並儲存到資料庫
    @pytest.mark.generate_reset_token_success
    def test_generate_reset_token_success(self):
        try:
            generate_reset_token("111423059@cc.ncu.edu.tw")
            assert True
        except BusinessError:
            assert False

    # 5.2 生成重置密碼的 Token 失敗 : 測試嘗試將相同的使用者 email 產生兩次 Token，在相同的時間
    @pytest.mark.generate_reset_token_failed
    def test_generate_reset_token_failed(self):
        try:
            generate_reset_token("111423059@cc.ncu.edu.tw")
        except BusinessError as e:
            system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    ## 6. 驗證重置 Token # validate_reset_token 大魔王

    # 6.1.1 驗證重置 Token 失敗 :
    # 檢查 Token 存在
    # 為 Token 時間是否過期，如果時間過期了，標記為過期，則失敗不可驗證重置 Token
    # 現在的狀況是 Token 根本不存在，所以會失敗
    @pytest.mark.validate_reset_token_failed
    def test_validate_reset_token_failed(self):
        try:
            validate_reset_token("123")
        except BusinessError as e:
            system_code = CommonSystemCode.DATABASE_FAILED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    # 6.2.1 重置密碼成功
    # reset_new_password(token, new_password, confirm_password)
    # 這個測試時，要發送信箱，找到最新的 Token。
    @pytest.mark.reset_new_password_success
    def test_reset_new_password_success(self):
        try:
            reset_new_password('3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM', "123456", "123456")
        except BusinessError as e:
            system_code = UserSystemCode.OLD_PASSWORD_NOT_ALLOWED.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False
        reset_new_password('3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM', "1234567", "1234567")

    # 6.2.2 重置新密碼失敗
    @pytest.mark.reset_new_password_failed
    def test_reset_new_password_failed(self):
        try:
            reset_new_password("3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM", "12345", "12345678")
            assert False
        except BusinessError:
            assert True

    ## 7. 標記 Token 使用過
    ## mark_token(token, TokenStatus)
    # 7.1.1 標記 Token 更新成功 : 查询資料庫，查找與 Token 匹配的紀錄
    # 在 DB 裡面去找相對應的欄位，更新那個目標。 NOT_USED = USED
    @pytest.mark.mark_token_success
    def test_mark_token_success(self):
        try:
            mark_token('dJQTLDrKwKs3GQEUjKzUeLVge1dw_aKRz7DpVk2raLs', TokenStatus.TokenStatus.USED)
            assert True
        except BusinessError:
            assert False
        mark_token('dJQTLDrKwKs3GQEUjKzUeLVge1dw_aKRz7DpVk2raLs', TokenStatus.TokenStatus.NOT_USED)

    # 7.1.2 標記 Token 更新失敗 : 查询資料庫，查找與 Token 匹配的紀錄
    # 因為已經更新成功為 USED
    @pytest.mark.mark_token_failed
    def test_mark_token_failed(self):
        try:
            mark_token('dJQTLDrKwKs3GQEUjKzUeLVge1dw_aKRz7DpVk2raLs', TokenStatus.TokenStatus.USED)
        except BusinessError as e:
            system_code = UserSystemCode.EXPIRED_TOKEN.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False

    ## mark_token_used(token: str)
    # 7.2.1 標記 Token 使用過成功 : 查询資料庫，查找與 Token 匹配的紀錄
    @pytest.mark.mark_token_used_success
    def test_mark_token_used_success(self):
        try:
            mark_token_used('3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM')
            assert True
        except BusinessError:
            assert False

    # 7.2.2 標記 Token 使用過失敗 : 查询資料庫，查找與 Token 匹配的紀錄
    """
    @pytest.mark.mark_token_used_failed
    def test_mark_token_used_failed(self):
        try:
            mark_token_used('3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM')
            mark_token('3GTPtl4Nwj3zZcqsDIt0hDIA8xcTmZio2q8ks8RMTKM', TokenStatus.TokenStatus.USED)
            system_code = UserSystemCode.EXPIRED_TOKEN.value.get('system_code')
            if e.error_code == system_code:
                assert True
            else:
                assert False
        except BusinessError:
            assert True
    """