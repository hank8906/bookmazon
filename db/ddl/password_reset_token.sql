CREATE SCHEMA IF NOT EXISTS bookmazon;

CREATE TABLE IF NOT EXISTS bookmazon.password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    update_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    create_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

COMMENT ON TABLE bookmazon.password_reset_tokens IS '密碼重置 token 表，用於存儲密碼重置令牌的資訊';

COMMENT ON COLUMN bookmazon.password_reset_tokens.user_id IS '關聯的使用者ID，建立多對一關係，參考 bookmazon.users 表的 id ';
