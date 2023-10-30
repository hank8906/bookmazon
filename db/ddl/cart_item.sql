-- 移除 "cart_item" 表格
DROP TABLE bookmazon.cart_item;

-- 創建 "cart_item" 表格
CREATE TABLE bookmazon.cart_item (
    cart_item_id serial NOT NULL,     -- cart_item_ID
    cart_id serial NOT NULL,          -- Order_ID
    book_id varchar(13) NOT NULL,     -- Book_ID (外部鍵)
    quantity integer NOT NULL,        -- 商品數量
    update_datetime timestamp,        -- 更新時間
    create_datetime timestamp,        -- 建立時間
    CONSTRAINT pk_cart_item PRIMARY KEY (cart_item_id)
);

-- 添加 "cart_item" 表格的註解
COMMENT ON TABLE bookmazon.cart_item IS '購物車商品項目表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.cart_item.cart_item_id IS '購物車商品項目表ID';
COMMENT ON COLUMN bookmazon.cart_item.order_id IS '購物車ID';
COMMENT ON COLUMN bookmazon.cart_item.book_id IS '書籍ID (外部鍵)';
COMMENT ON COLUMN bookmazon.cart_item.quantity IS '商品數量';
COMMENT ON COLUMN bookmazon.cart_item.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.cart_item.create_datetime IS '建立時間';