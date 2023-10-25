-- 創建 user 表格
CREATE TABLE bookmazon.user (
    user_account varchar(20),
    user_password varchar(16),
    user_identification varchar(1),
    user_email varchar(255),
    user_birthday varchar(255),
    update_datetime timestamp,
    create_datetime timestamp,
    CONSTRAINT pk_user PRIMARY KEY (user_Account)
);

-- 給表格加上註解
COMMENT ON TABLE bookmazon.user IS '使用者資訊表';

-- 給每個列加上註解
COMMENT ON COLUMN bookmazon.user.user_account IS '使用者帳號';
COMMENT ON COLUMN bookmazon.user.user_password IS '使用者密碼';
COMMENT ON COLUMN bookmazon.user.user_identification IS '使用者身分識別';
COMMENT ON COLUMN bookmazon.user.user_email IS '使用者電子郵件';
COMMENT ON COLUMN bookmazon.user.user_birthday IS '使用者生日';
COMMENT ON COLUMN bookmazon.user.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.user.create_datetime IS '建立時間';
