-- 移除 "order" 表格
DROP TABLE IF EXISTS bookmazon.order;

-- 創建 bookmazon.order 表格
CREATE TABLE bookmazon.order (
    order_id SERIAL NOT NULL,              -- 訂單ID
    user_account VARCHAR(20) NOT NULL,     -- 帳號 (外部鍵)
    recipient_name VARCHAR(50),            -- 收件人真實名字
    order_total_price NUMERIC(10, 2),      -- 訂單總價
    order_status VARCHAR(1),               -- 訂單狀態 (0: 未完成, 1: 完成, 2: 取消)
    payment_status VARCHAR(1),             -- 支付狀態 (0: 未完成, 1: 完成)
    shipping_status VARCHAR(1),            -- 運送狀態 (0: 未完成, 1: 完成)
    shipping_address VARCHAR(255),         -- 運送地址
    payment_method VARCHAR(20),            -- 付款方式
    update_datetime TIMESTAMP,             -- 更新時間
    create_datetime TIMESTAMP,             -- 建立時間
    -- 主鍵
    CONSTRAINT pk_order PRIMARY KEY (order_id)
);

-- 添加 bookmazon.order 表格的註解
COMMENT ON TABLE bookmazon.order IS '訂單資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.order.order_id           IS '訂單ID';
COMMENT ON COLUMN bookmazon.order.user_account       IS '帳號';
COMMENT ON COLUMN bookmazon.order.recipient_name     IS '收件人真實名字';
COMMENT ON COLUMN bookmazon.order.order_total_price  IS '訂單總價';
COMMENT ON COLUMN bookmazon.order.order_status       IS '訂單狀態';
COMMENT ON COLUMN bookmazon.order.payment_status     IS '支付狀態';
COMMENT ON COLUMN bookmazon.order.shipping_address   IS '運送地址';
COMMENT ON COLUMN bookmazon.order.payment_method     IS '付款方式';
COMMENT ON COLUMN bookmazon.order.shipping_status    IS '運送狀態';
COMMENT ON COLUMN bookmazon.order.update_datetime    IS '更新時間';
COMMENT ON COLUMN bookmazon.order.create_datetime    IS '建立時間';
