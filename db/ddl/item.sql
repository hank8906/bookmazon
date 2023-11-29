-- 移除 "item" 表格
DROP TABLE bookmazon.item;
-- 創建 "item" 表格
CREATE TABLE bookmazon.item (
    item_id SERIAL NOT NULL,            -- 品項ID
    book_id VARCHAR(13) NOT NULL,       -- 書籍ID (外部鍵)
    item_status VARCHAR(1),             -- 商品狀態 (0: 有販售, 1: 已販售)
    book_count INTEGER NOT NULL,        -- 庫存數
    provider_account VARCHAR(20),       -- 提供者帳號 (外部鍵)
    update_datetime TIMESTAMP,          -- 更新時間
    create_datetime TIMESTAMP,          -- 建立時間
    CONSTRAINT pk_item PRIMARY KEY (item_id)
);

-- 添加 "item" 表格的註解
COMMENT ON TABLE bookmazon.item IS '商品資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.item.item_id          IS '品項ID';
COMMENT ON COLUMN bookmazon.item.book_id          IS '書籍ID';
COMMENT ON COLUMN bookmazon.item.item_status      IS '商品狀態';
COMMENT ON COLUMN bookmazon.item.book_count       IS '庫存數';
COMMENT ON COLUMN bookmazon.item.provider_account IS '提供者帳號';
COMMENT ON COLUMN bookmazon.item.update_datetime  IS '更新時間';
COMMENT ON COLUMN bookmazon.item.create_datetime  IS '建立時間';
