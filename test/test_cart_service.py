import pytest
import logging

from service.CartService import (calculate_total_price, get_cart_items,
                                 get_cart_item_count, add_item_to_cart,
                                 remove_item_from_cart,
                                 get_cart_designated_item_count,
                                 get_or_create_cart, update_cart_item)

from exception.BusinessError import BusinessError

from model.Book import Book
from model.Cart import Cart
from model.User import User
from model.CartItem import CartItem
from model.Item import Item

from utils import logger
from utils.dbUtil import session

app_logger = logger.setup_logger(logging.INFO)


# get a valid user account
def get_valid_user_account():
    return session.query(User).first().user_account


# get a valid item id, which item_status = 1
def get_valid_item_id():
    return session.query(Item).where(Item.item_status == '1').first().item_id


user = get_valid_user_account()
invalid_user = 'invalid_user_account1'
item = get_valid_item_id()


class TestCartService:

    ## 1 加入購物車
    # add_item_to_cart(user_account, item_id, quantity)
    # 1.1 加入購物車 成功
    @pytest.mark.add_to_cart_success
    def test_add_to_cart_success(self):
        user_account = user
        item_id = item
        quantity = 1
        # original cart item count
        old_item_count = get_cart_designated_item_count(user_account, item_id)

        try:
            item_count = session.query(Item).where(Item.item_id == item_id).first().book_count

            # if cart item count already >= item quantity, delete cart item first
            if get_cart_designated_item_count(user_account, item_id) >= item_count:
                cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id
                remove_item_from_cart(cart_item_id)
                count = 0
            else:
                count = old_item_count

            # add item to cart
            add_item_to_cart(user_account, item_id, quantity)
            new_item_count = get_cart_designated_item_count(user_account, item_id)

            assert count + quantity == new_item_count
        except BusinessError:
            assert False

        # modify the item amount back to the original amount
        cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id
        remove_item_from_cart(cart_item_id)
        add_item_to_cart(user_account, item_id, old_item_count)

        # user_account = user
        # item_id = item
        # quantity = 1
        #
        # try:
        #     item_count = session.query(Item).where(Item.item_id == item_id).first().book_count
        #
        #     # if cart item count already > item quantity, delete cart item first
        #     if get_cart_designated_item_count(user_account, item_id) >= item_count:
        #         # cart item id from specific item id
        #         cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id
        #         remove_item_from_cart(cart_item_id)
        #
        #     # add item to cart
        #     old_item_count = get_cart_designated_item_count(user_account, item_id)
        #     add_item_to_cart(user_account, item_id, quantity)
        #     new_item_count = get_cart_designated_item_count(user_account, item_id)
        #
        #     assert old_item_count + 1 == new_item_count
        #
        # except BusinessError:
        #     assert False

    # 1.2 加入購物車 失敗  : 購物車內的商品數量已經 >= 原有庫存 或 欲加入購物車的數量大於原有庫存
    @pytest.mark.add_to_cart_failed
    def test_add_to_cart_failed(self):
        user_account = user
        item_id = item
        # check item stock
        quantity = session.query(Item).where(Item.item_id == item_id).first().book_count
        exceed_quantity = quantity + 1
        # cart item count
        cart_item_count = get_cart_designated_item_count(user_account, item_id)

        try:
            # 購物車內的數量已經 >= 原有庫存
            if cart_item_count >= quantity:
                add_item_to_cart(user_account, item_id, 1)
                assert False
            # 加入購物車的數量大於原有庫存
            else:
                add_item_to_cart(user_account, item_id, exceed_quantity)
                assert False
        except BusinessError:
            assert True

    # 1.3 加入購物車 失敗 : 數值包含負數
    @pytest.mark.add_to_cart_invalid_value_negative
    def test_add_to_cart_invalid_value_negative(self):
        user_account = user
        item_id = item
        # invalid quantity
        invalid_value = -1

        try:
            add_item_to_cart(user_account, item_id, invalid_value)
            assert False
        except BusinessError:
            assert True

    # 1.4 加入購物車 失敗 : 數值包含 0
    @pytest.mark.add_to_cart_invalid_value_zero
    def test_add_to_cart_invalid_value_zero(self):
        user_account = user
        item_id = item
        # invalid quantity
        invalid_value = 0

        try:
            add_item_to_cart(user_account, item_id, invalid_value)
            assert False
        except BusinessError:
            assert True

    # 1.5 加入購物車 失敗 : 數值包含小數
    @pytest.mark.add_to_cart_invalid_value_float
    def test_add_to_cart_invalid_value_float(self):
        user_account = user
        item_id = item
        # invalid quantity
        invalid_value = 1.5

        try:
            add_item_to_cart(user_account, item_id, invalid_value)
            assert False
        except BusinessError:
            assert True

    # # # 1.6 加入購物車 失敗 : 數值包含字串
    # @pytest.mark.add_to_cart_invalid_value_string
    # def test_add_to_cart_invalid_value_string(self):
    #     user_account = user
    #     item_id = item
    #     # invalid quantity
    #     invalid_value = 'not integer'
    #
    #     try:
    #         add_item_to_cart(user_account, item_id, invalid_value)
    #         assert False
    #     except BusinessError:
    #         assert True

    # 1.7 加入購物車 失敗 : 商品狀態為 0
    # @pytest.mark.add_to_cart_invalid_status
    # def test_add_to_cart_invalid_status(self):
    #     # get a invalid item id, which item_status = 0
    #     invalid_item_id = session.query(Item).where(Item.item_status == '0').first().item_id
    #     user_account = user
    #     quantity = 1
    #
    #     try:
    #         add_item_to_cart(user_account, invalid_item_id, quantity)
    #         assert False
    #     except BusinessError:
    #         assert True

    ## 2 加總會員購物車裡面的特定商品數量
    # get_cart_designated_item_count(user_account, item_id)
    # 2.1 加總會員購物車裡面的特定商品數量 成功
    @pytest.mark.get_cart_designated_item_count_success
    def test_get_cart_designated_item_count_success(self):
        user_account = user
        item_id = item
        try:
            cart_items = get_cart_items(user_account)
            if cart_items is None:
                assert get_cart_designated_item_count(user_account, item_id) == 0
            else:
                # check cart items count
                count = session.query(CartItem).where(CartItem.item_id == item_id).first().quantity
                assert get_cart_designated_item_count(user_account, item_id) == count
        except BusinessError:
            assert False

    # 2.2 加總會員購物車裡面的特定商品數量 失敗 : 會員帳號不存在
    @pytest.mark.get_cart_designated_item_count_invalid_user
    def test_get_cart_designated_item_count_invalid_user(self):
        item_id = item
        try:
            assert get_cart_designated_item_count(invalid_user, item_id) == 0
            # assert False
        except BusinessError:
            assert True

    # 2.3 加總會員購物車裡面的特定商品數量 失敗 : 商品不存在
    @pytest.mark.get_cart_designated_item_count_invalid_item
    def test_get_cart_designated_item_count_invalid_item(self):
        user_account = user
        invalid_item_id = 999
        try:
            assert get_cart_designated_item_count(user_account, invalid_item_id) == 0
            # assert False
        except BusinessError:
            assert True

    ## 3 建立或取得購物車
    # get_or_create_cart(user_account)
    # 3.1 建立或取得購物車 成功
    @pytest.mark.get_or_create_cart_success
    def test_get_or_create_cart_success(self):
        # get a valid user account in cart table
        valid_user_account = session.query(Cart).first().user_account
        try:
            get_or_create_cart(valid_user_account)
            assert True
        except BusinessError:
            assert False

    # 3.2 建立或取得購物車 失敗 : 會員帳號不存在
    # @pytest.mark.get_or_create_cart_failed
    # def test_get_or_create_cart_failed(self):
    #     try:
    #         cart = get_or_create_cart(invalid_user)
    #         assert cart is None
    #     except BusinessError:
    #         assert True

    ## 4 更新購物車品項數量
    # 4.1 更新購物車品項數量 成功
    # @pytest.mark.update_cart_item
    # def test_update_cart_item(self):
    #     pass

    ## 5 查詢購物車品項
    # get_cart_items(user_account)
    # 5.1 查詢購物車品項 成功
    @pytest.mark.get_cart_items_success
    def test_get_cart_items_success(self):
        user_account = user
        try:
            cart_items = get_cart_items(user_account)
            if cart_items is None:
                assert get_cart_items(user_account) is None
            else:
                assert get_cart_items(user_account) is not None
        except BusinessError:
            assert False

    # 5.2 查詢購物車品項 失敗 : 會員帳號不存在
    @pytest.mark.get_cart_items_failed
    def test_get_cart_items_failed(self):
        try:
            get_cart_items(invalid_user)
            # assert False
        except BusinessError:
            assert True

    # 6 刪除購物車品項
    # remove_item_from_cart(cart_item_id)
    # 6.1 刪除購物車品項 成功
    @pytest.mark.remove_item_from_cart_success
    def test_remove_item_from_cart_success(self):
        user_account = user
        item_id = item
        # original quantity of specific item in cart
        quantity = get_cart_designated_item_count(user_account, item_id)

        try:
            # item_count = get_cart_designated_item_count(user_account, item_id)
            cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id

            if quantity > 0:
                remove_item_from_cart(cart_item_id)
                new_item_count = get_cart_designated_item_count(user_account, item_id)
                assert new_item_count == 0
        except BusinessError:
            assert False
        # add the deleted item back to cart
        if quantity > 0:
            add_item_to_cart(user_account, item_id, quantity)

    # 6.2 刪除購物車品項 失敗 : 品項不存在
    @pytest.mark.remove_item_from_cart_failed
    def test_remove_item_from_cart_failed(self):
        invalid_cart_item_id = 999
        try:
            # remove_item_from_cart(invalid_cart_item_id)
            assert remove_item_from_cart(invalid_cart_item_id) is None
        except BusinessError:
            assert True

    ## 7 計算購物車內商品總價
    # calculate_total_price(user_account)
    # 7.1 計算購物車內商品總價 成功
    @pytest.mark.calculate_total_price_success
    def test_calculate_total_price_success(self):
        user_account = user
        total_price = 0
        # get cart id from specific user account
        cart_id = session.query(Cart).where(Cart.user_account == user_account).first().cart_id

        try:
            # check if the cart is empty
            cart_items = get_cart_items(user_account)
            if cart_items is None:
                assert calculate_total_price(user_account) == 0
            else:
                # get all item id and it's quantity from the same cart
                cart_items = session.query(CartItem).where(CartItem.cart_id == cart_id).all()
                for cart_item in cart_items:
                    item_id = cart_item.item_id
                    item_book_id = session.query(Item).where(item_id == Item.item_id).first().book_id

                    # get book price from book table
                    item_price = session.query(Book).where(Book.book_id == item_book_id).first().book_price

                    # calculate total price
                    total_price += item_price * cart_item.quantity

                assert calculate_total_price(user_account) == total_price

        except BusinessError:
            assert False

    # 7.2 計算購物車內商品總價 失敗 : 會員帳號不存在
    @pytest.mark.calculate_total_price_failed
    def test_calculate_total_price_failed(self):
        try:
            price = calculate_total_price(invalid_user)
            assert price == 0
        except BusinessError:
            assert True

    ## 8 把購物車內商品總數顯示在首頁的購物車按鈕的旁邊
    # get_cart_item_count(user_account)
    # 8.1 把購物車內商品總數顯示在首頁的購物車按鈕的旁邊 成功
    @pytest.mark.get_cart_item_count_success
    def test_get_cart_item_count_success(self):
        user_account = user
        cart_id = session.query(Cart).where(Cart.user_account == user_account).first().cart_id
        try:
            # check if the cart is empty
            cart_items = get_cart_items(user_account)
            if cart_items is None:
                assert get_cart_item_count(user_account) == 0
            else:
                # get all quantity from the same cart
                items = session.query(CartItem).where(CartItem.cart_id == cart_id).all()
                count = 0
                for item in items:
                    count += item.quantity
                assert get_cart_item_count(user_account) == count

        except BusinessError:
            assert False

    # 8.2 把購物車內商品總數顯示在首頁的購物車按鈕的旁邊 失敗 : 會員帳號不存在
    @pytest.mark.get_cart_item_count_failed
    def test_get_cart_item_count_failed(self):
        try:
            assert get_cart_item_count(invalid_user) == 0
            # assert False
        except BusinessError:
            assert True
