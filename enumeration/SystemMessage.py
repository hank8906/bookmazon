from enum import Enum

class CommonSystemCode(Enum):
    SUCCESS = {'system_code': '0000', 'message': '系統成功'}
    DATABASE_FAILED = {'system_code': '0001', 'message': '資料庫異常'}

class ShoppingCartSystemCode(Enum):
    ADD_ITEM_SUCCESS = {'system_code': '6000', 'message': '商品加入成功'}
    OUT_OF_STOCK = {'system_code': '6001', 'message': '商品無庫存'}
    ITEM_NOT_FOUND = {'system_code': '6002', 'message': '商品不存在'}
    REMOVE_FROM_CART_FAILED = {'system_code': '6003', 'message': '商品已從購物車移除'}
    ADD_TO_CART_SUCCESS = {'system_code': '6004', 'message': '商品已加入購物車'}
    QUANTITY_EXCEEDS_STOCK = {'system_code': '6005', 'message': '購物車中的商品數量超出庫存，無法再添加'}
    EXCEEDS_MAX_STOCK = {'system_code': '6006', 'message': '選購的商品數量超出庫存'}
