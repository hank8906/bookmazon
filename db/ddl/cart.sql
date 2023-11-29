-- 移除 "cart" 表格
DROP TABLE bookmazon.cart;
-- 創建 "cart" 表格
CREATE TABLE bookmazon.cart (
    cart_id serial NOT NULL,            -- 購物車ID
    user_account varchar(20) NOT NULL,  -- 帳號 (外部鍵)
    update_datetime timestamp,          -- 更新時間
    create_datetime timestamp,          -- 建立時間
    CONSTRAINT pk_cart PRIMARY KEY (cart_id)
);

-- 添加 "cart" 表格的註解
COMMENT ON TABLE bookmazon.cart IS '購物車資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.cart.cart_id         IS '購物車ID';
COMMENT ON COLUMN bookmazon.cart.user_account    IS '帳號';
COMMENT ON COLUMN bookmazon.cart.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.cart.create_datetime IS '建立時間';