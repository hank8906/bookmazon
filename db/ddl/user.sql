-- 移除 "user" 表格
DROP TABLE bookmazon.user;
-- 創建 user 表格
CREATE TABLE bookmazon.user (
    user_account varchar(20) NOT NULL,  --使用者帳號
    user_password varchar(16) NOT NULL, --使用者密碼
    user_name VARCHAR(50) NOT NULL,     --使用者姓名
    user_gender varchar(1),             --性別
    user_email varchar(255),            --使用者電子郵件
    user_birthday date,                 --使用者生日
    user_identification varchar(1),     --使用者身分識別
    update_datetime timestamp,          --更新時間
    create_datetime timestamp,          --建立時間
    CONSTRAINT pk_user PRIMARY KEY (user_account)
);

-- 給表格加上註解
COMMENT ON TABLE bookmazon.user IS '使用者資訊表';

-- 給每個列加上註解
COMMENT ON COLUMN bookmazon.user.user_account IS '使用者帳號';
COMMENT ON COLUMN bookmazon.user.user_password IS '使用者密碼';
COMMENT ON COLUMN bookmazon.user.user_name IS '使用者姓名';
COMMENT ON COLUMN bookmazon.user.user_gender IS '性別';
COMMENT ON COLUMN bookmazon.user.user_email IS '使用者電子郵件';
COMMENT ON COLUMN bookmazon.user.user_birthday IS '使用者生日';
COMMENT ON COLUMN bookmazon.user.user_identification IS '使用者身分識別';
COMMENT ON COLUMN bookmazon.user.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.user.create_datetime IS '建立時間';