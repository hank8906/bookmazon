from flask import Blueprint, request, redirect, url_for, flash, render_template
from service.OrderService import add_order, get_order_by_id, get_order_items, get_user_orders, update_order, \
    cancel_an_order
from flask_login import login_required, current_user
from service.CartService import CartService

orderController = Blueprint('orderController', __name__)

cartService = CartService()

"""
    建立會員的訂單
    Args:
        cart_items 購物車項目
    Returns:
        
    Raises:
        
"""


@orderController.route('/checkout', methods=['POST'])
@login_required
def checkout():
    # 獲取目前使用者的購物車項目
    cart_items = cartService.get_cart_items(current_user.user.user_account)

    # 初始化用於儲存更新後數量的字典
    updated_quantities = {}

    # 迭代購物車項目
    for cart_item_tuple in cart_items:
        # 元組拆包
        # 元组拆包，將 cart_item_tuple 中的值分配给相應的變數
        # cart_item 用於 save 元組的第一個值，可能表示購物車中的一個項
        # 第二個下劃線 _ 表示忽略元組的第二個值
        # 第三個下劃線 _ 表示同樣不關心元组的第三個值
        cart_item, _, _ = cart_item_tuple
        # 取得訂單數量的表單欄位名稱
        input_name = f'quantity-{cart_item.cart_item_id}'
        # 從表單中獲取更新後的數量
        updated_quantity = request.form.get(input_name, type=int)

        # 檢查是否有更新，若無則使用原本的數量
        if updated_quantity is not None:
            updated_quantities[cart_item.cart_item_id] = updated_quantity
        else:
            updated_quantities[cart_item.cart_item_id] = cart_item.quantity

    # 使用 add_order 函式創建訂單
    order_id = add_order(current_user.user.user_account, cart_items, updated_quantities)

    # 檢查是否成功創建訂單，並顯示相應的 Flash 訊息
    if order_id:
        flash(f"訂單已成功創建", "success")
        return redirect(url_for('orderController.view_order_details', order_id=order_id))
    else:
        flash("結帳失敗", "error")
        return redirect(url_for('cartController.view_cart'))


"""
    查看會員的訂單明細
    Args:
        order_id 訂單ID
    Returns:

    Raises:
        
"""


@orderController.route('/view_order_details/<int:order_id>', methods=['GET'])
@login_required
def view_order_details(order_id):
    # 使用 get_order_by_id 函式獲取指定訂單
    order = get_order_by_id(order_id)

    # 檢查訂單是否存在
    if not order:
        flash("訂單不存在", "warning")
        return redirect(url_for('productController.getProducts'))

    # 檢查當前使用者是否有權訪問此訂單
    if order.user_account != current_user.user.user_account:
        flash("您無權訪問此訂單", "warning")
        return redirect(url_for('productController.getProducts'))

    # 使用 get_order_items 函式獲取訂單項目
    order_items = get_order_items(order_id)

    # 將訂單和訂單項目傳遞給模板，並呈現訂單詳細資訊的頁面
    return render_template('order/viewOrderDetails.html', order=order, order_items=order_items)


"""
    查看會員所有的訂單
    Args:
        user_account 帳號
    Returns:

    Raises:
        None
"""


@orderController.route('/view_order')
@login_required
def view_order():
    # 獲取當前使用者的帳號
    user_account = current_user.user.user_account

    # 使用 get_user_orders 函式獲取該使用者的所有訂單
    orders = get_user_orders(user_account)

    # 將訂單列表傳遞給模板，並呈現訂單總覽的頁面
    return render_template('order/viewOrder.html', orders=orders)


# 修改訂單
@orderController.route('/modify_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def modify_order(order_id):
    # 獲取要修改的訂單
    order = get_order_by_id(order_id)

    # 檢查訂單是否存在
    if not order:
        flash("訂單不存在", "warning")
        return redirect(url_for('productController.getProducts'))

    # 檢查是否有權修改此訂單
    if order.user_account != current_user.user.user_account:
        flash("您無權修改此訂單", "warning")
        return redirect(url_for('productController.getProducts'))

    # 處理修改訂單的 POST 請求
    if request.method == 'POST':
        try:
            # 在這裡處理修改訂單的邏輯
            updated_quantity = request.form.get('quantity', type=int)

            # 準備要更新的訂單資料，這裡要更新的數量
            new_order_data = {'quantity': updated_quantity}

            # 使用 OrderService 更新訂單
            result = update_order(order_id, new_order_data)

            if result:
                flash("訂單已修改", "success")
                return redirect(url_for('orderController.view_order_details', order_id=order_id))
            else:
                # 若更新失敗，導向一個適當的頁面
                flash("訂單修改失敗", "error")
                return redirect(url_for('productController.getProducts'))

        except Exception as e:
            # 處理其他可能的錯誤
            flash(f"發生錯誤: {str(e)}", "error")
            return redirect(url_for('productController.getProducts'))

    # 渲染修改訂單的模板
    return render_template('order/modifyOrder.html', order=order)


# 取消訂單
@orderController.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    # 獲取要取消的訂單
    order = get_order_by_id(order_id)

    # 檢查訂單是否存在
    if not order:
        flash("訂單不存在", "warning")
        return redirect(url_for('productController.getProducts'))

    # 檢查是否有權取消此訂單
    if order.user_account != current_user.user.user_account:
        flash("您無權取消此訂單", "warning")
        return redirect(url_for('productController.getProducts'))
    else:
        cancel_an_order(order_id)
        # 在這裡處理取消訂單的邏輯
        flash("訂單已取消", "success")
        return redirect(url_for('orderController.view_order'))
