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
item = get_valid_item_id()


class TestCartService:
    # 加入購物車
    @pytest.mark.add_to_cart_success
    def test_add_to_cart_success(self):
        user_account = user
        item_id = item
        quantity = 1

        try:
            item_count = session.query(Item).where(Item.item_id == item_id).first().book_count

            # if cart item count already > item quantity, delete cart item first
            if get_cart_designated_item_count(user_account, item_id) >= item_count:
                # cart item id from specific item id
                cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id
                remove_item_from_cart(cart_item_id)

            # add item to cart
            old_item_count = get_cart_designated_item_count(user_account, item_id)
            add_item_to_cart(user_account, item_id, quantity)
            new_item_count = get_cart_designated_item_count(user_account, item_id)

            assert old_item_count + quantity == new_item_count
        except BusinessError:
            assert False

    # 加入購物車失敗，驗證庫存數量
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
            add_item_to_cart(user_account, item_id, exceed_quantity)
            assert False
        except BusinessError:
            assert True

    # 加入購物車失敗，驗證加入的數值是否包含負數、小數或字串
    @pytest.mark.add_to_cart_unvalid_value
    def test_add_to_cart_invalid_value(self):
        user_account = user
        item_id = item
        # invalid quantity array
        invalid_value = [0, -1, 1.5, 'not a number']

        try:
            for value in invalid_value:
                add_item_to_cart(user_account, item_id, value)
                assert False
        except BusinessError:
            assert True

    # @pytest.mark.get_cart_designated_item_count
    # def test_get_cart_designated_item_count(self):
    #     user_account = user
    #     item_id = item
    #     try:
    #         cart_items = get_cart_items(user_account)
    #         if cart_items is None:
    #             assert get_cart_designated_item_count(user_account, item_id) == 0
    #         else:
    #             # check cart items count
    #             count = session.query(CartItem).where(CartItem.item_id == item_id).first().quantity
    #             assert get_cart_designated_item_count(user_account, item_id) == count
    #     except BusinessError:
    #         assert False
    #
    # @pytest.mark.get_or_create_cart
    # def test_get_or_create_cart(self):
    #     pass
    #
    # @pytest.mark.update_cart_item
    # def test_update_cart_item(self):
    #     pass

    @pytest.mark.get_cart_items
    def test_get_cart_items(self):
        user_account = user
        try:
            cart_items = get_cart_items(user_account)
            if cart_items is None:
                assert get_cart_items(user_account) is None
            else:
                assert get_cart_items(user_account) is not None
        except BusinessError:
            assert False

    # 刪除購物車內商品
    # @pytest.mark.remove_item_from_cart
    # def test_remove_item_from_cart(self):
    #     user_account = user
    #     item_id = item
    #
    #     try:
    #         item_count = get_cart_designated_item_count(user_account, item_id)
    #         cart_item_id = session.query(CartItem).where(CartItem.item_id == item_id).first().cart_item_id
    #
    #         if item_count > 0:
    #             remove_item_from_cart(cart_item_id)
    #             new_item_count = get_cart_designated_item_count(user_account, item_id)
    #             assert new_item_count == 0
    #         else:
    #             assert False
    #     except BusinessError:
    #         assert False

    # 計算購物車總價
    @pytest.mark.calculate_total_price
    def test_calculate_total_price(self):
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

    # 查看購物車內商品總數量
    @pytest.mark.get_cart_item_count
    def test_get_cart_item_count(self):
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
