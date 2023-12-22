-- 移除 "password_reset_tokens" 表格
DROP TABLE bookmazon.password_reset_tokens;

CREATE TABLE bookmazon.password_reset_tokens (
    id              SERIAL       NOT NULL,
    user_email      VARCHAR(255) NOT NULL,
    token           VARCHAR(255) NOT NULL,
    token_status    VARCHAR(1),
    update_datetime TIMESTAMP,
    create_datetime TIMESTAMP,
    CONSTRAINT pk_password_reset_tokens PRIMARY KEY (id)
);

-- 添加 "password_reset_tokens" 表格的註解
COMMENT ON TABLE bookmazon.password_reset_tokens               IS '會員忘記密碼申請表';
COMMENT ON COLUMN bookmazon.password_reset_tokens.id           IS '會員忘記密碼申請表ID';
COMMENT ON COLUMN bookmazon.password_reset_tokens.user_email   IS '會員Email';
COMMENT ON COLUMN bookmazon.password_reset_tokens.token        IS 'Token';
COMMENT ON COLUMN bookmazon.password_reset_tokens.token_status IS 'Token 狀態';
COMMENT ON COLUMN bookmazon.order_item.update_datetime         IS '更新時間';
COMMENT ON COLUMN bookmazon.order_item.create_datetime         IS '建立時間';
