-- 移除 "item" 表格
DROP TABLE bookmazon.item;
-- 創建 "item" 表格
CREATE TABLE bookmazon.item (
    item_id serial NOT NULL,      -- Item_ID
    book_id varchar(13) NOT NULL, -- Book_ID (外部鍵)
    item_status varchar(1),       -- 商品狀態 (0: 有販售, 1: 已販售)
    book_count integer NOT NULL,  -- 庫存
    update_datetime timestamp,    -- 更新時間
    create_datetime timestamp,    -- 建立時間
    CONSTRAINT pk_item PRIMARY KEY (item_id)
);

-- 添加 "item" 表格的註解
COMMENT ON TABLE bookmazon.item IS '商品資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.item.item_id IS '商品ID';
COMMENT ON COLUMN bookmazon.item.book_id IS '書籍ID (外部鍵)';
COMMENT ON COLUMN bookmazon.item.item_status IS '商品狀態 (0: 有販售, 1: 已販售)';
COMMENT ON COLUMN bookmazon.item.book_count IS '庫存';
COMMENT ON COLUMN bookmazon.item.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.item.create_datetime IS '建立時間';
