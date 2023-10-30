-- 移除 "order" 表格
DROP TABLE bookmazon.order;

-- 創建 order. 表格
CREATE TABLE bookmazon.order (
    order_id serial NOT NULL,              -- Order_ID
    user_account varchar(20) NOT NULL,     -- 帳號 (外部鍵)
    order_total_price integer,             -- 訂單總價
    order_date timestamp,                  -- 訂單日期
    order_status varchar(1),               -- 訂單狀態 (0: 未完成, 1: 完成, 2: 取消)
    update_datetime timestamp,             -- 更新時間
    create_datetime timestamp,             -- 建立時間
    CONSTRAINT pk_order PRIMARY KEY (order_id)
);

-- 添加 bookmazon.order. 表格的註解
COMMENT ON TABLE bookmazon.order IS '訂單資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.order.order_id IS '訂單ID';
COMMENT ON COLUMN bookmazon.order.user_account IS '帳號 (外部鍵)';
COMMENT ON COLUMN bookmazon.order.order_total_price IS '訂單總價';
COMMENT ON COLUMN bookmazon.order.order_date IS '訂單日期';
COMMENT ON COLUMN bookmazon.order.order_status IS '訂單狀態 (0: 未完成, 1: 完成, 2: 取消)';
COMMENT ON COLUMN bookmazon.order.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.order.create_datetime IS '建立時間';
