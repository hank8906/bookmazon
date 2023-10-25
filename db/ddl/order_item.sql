-- 創建 "order_item" 表格
CREATE TABLE bookmazon.order_item (
    order_item_id serial,           -- Order_Item_ID
    order_id serial,                -- Order_ID
    book_id varchar(13),            -- Book_ID (外部鍵)
    quantity integer,               -- 商品數量
    update_datetime timestamp,       -- 更新時間
    create_datetime timestamp,        -- 建立時間
    CONSTRAINT pk_order_item PRIMARY KEY (order_item_id)
);

-- 添加 "order_item" 表格的註解
COMMENT ON TABLE bookmazon.order_item IS '訂單商品項目表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.order_item.order_item_id IS '訂單商品項目表ID';
COMMENT ON COLUMN bookmazon.order_item.order_id IS '訂單ID';
COMMENT ON COLUMN bookmazon.order_item.book_id IS '書籍ID (外部鍵)';
COMMENT ON COLUMN bookmazon.order_item.quantity IS '商品數量';
COMMENT ON COLUMN bookmazon.order_item.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.order_item.create_datetime IS '建立時間';