-- 移除 "cart_item" 表格
DROP TABLE bookmazon.cart_item;

-- 創建 "cart_item" 表格
CREATE TABLE bookmazon.cart_item (
    cart_item_id SERIAL NOT NULL,     -- 購物車商品項目表ID
    cart_id  INTEGER NOT NULL,        -- 購物車ID (外部鍵)
    item_id  INTEGER NOT NULL,        -- 品項ID (外部鍵)
    quantity INTEGER NOT NULL,        -- 商品數量
    update_datetime TIMESTAMP,        -- 更新時間
    create_datetime TIMESTAMP,        -- 建立時間
    CONSTRAINT pk_cart_item PRIMARY KEY (cart_item_id)
);

-- 添加 "cart_item" 表格的註解
COMMENT ON TABLE bookmazon.cart_item IS '購物車商品項目表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.cart_item.cart_item_id    IS '購物車商品項目表ID';
COMMENT ON COLUMN bookmazon.cart_item.cart_id         IS '購物車ID';
COMMENT ON COLUMN bookmazon.cart_item.item_id         IS '品項ID';
COMMENT ON COLUMN bookmazon.cart_item.quantity        IS '商品數量';
COMMENT ON COLUMN bookmazon.cart_item.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.cart_item.create_datetime IS '建立時間';