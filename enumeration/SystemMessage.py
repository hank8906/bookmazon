from enum import Enum

class CommonSystemCode(Enum):
    SUCCESS = {'system_code': '0000', 'message': '系統成功'}
    DATABASE_FAILED = {'system_code': '0001', 'message': '目前資料庫異常，請稍候嘗試，或聯繫網站管理人員'}
    SYSTEM_FAILED = {'system_code': '0002', 'message': '目前系統異常，請稍候嘗試，或聯繫網站管理人員'}

class UserSystemCode(Enum):
    REGISTER_SUCCESS = {'system_code': '1001', 'message': '帳號註冊成功，您可以登入了'}
    REGISTERED_ACCOUNT = {'system_code': '1002', 'message': '這個帳號已經被註冊了，請更換一另組帳號'}
    REGISTER_FAILED = {'system_code': '1003', 'message': '帳號註冊失敗，請您稍候嘗試，或聯繫網站管理人員'}
    LOGIN_FAILED = {'system_code': '1004', 'message': '登入失敗！請您確認帳號、或密碼是否輸入有誤'}
    LOGOUT = {'system_code': '1005', 'message': '登出成功！'}
    UPDATE_USER_INFO_SUCCESS = {'system_code': '1006', 'message': '會員資料更新成功！'}
    UPDATE_USER_INFO_FAILED = {'system_code': '1007', 'message': '登出成功！'}
    UPDATE_PASSWD_SUCCESS = {'system_code': '1007', 'message': '更換密碼成功！'}
    UPDATE_PASSWD_FAILED = {'system_code': '1008', 'message': '更換密碼失敗！'}
    IS_NOT_OLD_PASSWORD = {'system_code': '1009', 'message': '舊密碼輸入錯誤'}
    OLD_PASSWORD_NOT_ALLOWED = {'system_code': '1010', 'message': '新密碼不得與舊密碼一樣'}
    EMAIL_NOT_EXISTED = {'system_code': '1011', 'message': '輸入電子郵件地址不存在'}
    RESET_EMAIL_SENT = {'system_code': '1012', 'message': '更換密碼信件已送出，請查收信箱'}
    EXPIRED_TOKEN = {'system_code': '1013', 'message': 'Token 已經過期，請重新申請變更密碼'}
    TOKEN_NOT_EXISTED = {'system_code': '1014', 'message': 'Token 已經過期，請重新申請變更密碼'}
    PASSWORD_NOT_SAME = {'system_code': '1015', 'message': '兩次輸入的密碼不一致，請確保兩次輸入的密碼相同'}
    REGISTERED_EMAILED = {'system_code': '1016', 'message': '這個Email已經被註冊使用了，請更換一另組Email'}

class ShoppingCartSystemCode(Enum):
    ADD_ITEM_SUCCESS = {'system_code': '6000', 'message': '商品加入成功'}
    OUT_OF_STOCK = {'system_code': '6001', 'message': '商品無庫存'}
    ITEM_NOT_FOUND = {'system_code': '6002', 'message': '商品不存在'}
    REMOVE_FROM_CART_FAILED = {'system_code': '6003', 'message': '商品已從購物車移除'}
    ADD_TO_CART_SUCCESS = {'system_code': '6004', 'message': '商品已加入購物車'}
    QUANTITY_EXCEEDS_STOCK = {'system_code': '6005', 'message': '購物車中的商品數量超出庫存，無法再添加'}
    EXCEEDS_MAX_STOCK = {'system_code': '6006', 'message': '選購的商品數量超出庫存'}
    ITEM_REMOVED = {'system_code': '6007', 'message': '商品已從購物車移除'}

class OrderSystemCode(Enum):
    PLACE_ORDER_SUCCESS = {'system_code': '6000', 'message': '訂單已建立成功，請等候數個工作天收貨'}
    PLACE_ORDER_FAILED = {'system_code': '6001', 'message': '下單失敗，請稍候嘗試'}
