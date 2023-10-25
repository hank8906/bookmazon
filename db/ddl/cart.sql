-- 創建 "cart" 表格
CREATE TABLE bookmazon.cart (
    cart_id serial,                 -- Cart_ID
    user_account varchar(20),       -- 帳號 (外部鍵)
    book_id varchar(13),            -- Book_ID (外部鍵)
    quantity integer,               -- 商品數量
    update_datetime timestamp,      -- 更新時間
    create_datetime timestamp,      -- 建立時間
    CONSTRAINT pk_cart PRIMARY KEY (cart_id)
);

-- 添加 "cart" 表格的註解
COMMENT ON TABLE bookmazon.cart IS '購物車資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.cart.cart_id IS '購物車ID';
COMMENT ON COLUMN bookmazon.cart.user_account IS '帳號 (外部鍵)';
COMMENT ON COLUMN bookmazon.cart.book_id IS '書籍ID (外部鍵)';
COMMENT ON COLUMN bookmazon.cart.quantity IS '商品數量';
COMMENT ON COLUMN bookmazon.cart.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.cart.create_datetime IS '建立時間';