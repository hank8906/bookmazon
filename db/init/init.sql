-- 建立 bookmazon schema
CREATE SCHEMA bookmazon;

-- 可以選資料表內容的角色
CREATE ROLE rl_sel;
-- 可以刪除資料表內容的角色
CREATE ROLE rl_del;
-- 可以更新資料表內容的角色
CREATE ROLE rl_upd;
-- 可以新增資料表內容的角色
CREATE ROLE rl_ins;

-- 程式開發人員操作 db 的角色
CREATE ROLE user_001 WITH LOGIN CREATEDB CREATEROLE PASSWORD 'user_001';
GRANT rl_sel, rl_del, rl_upd, rl_ins to user_001;
-- 賦予 bookmazon schema 的使用權限
GRANT USAGE ON SCHEMA bookmazon to user_001;
-- 賦予可以 bookmazon schema 建立物件（trigger、function、procedure）的權限
GRANT CREATE ON SCHEMA bookmazon to user_001;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA bookmazon TO user_001;

-- 後端系統操作 db 的角色
CREATE ROLE app_001 WITH LOGIN PASSWORD 'app_001';
GRANT rl_sel, rl_del, rl_upd, rl_ins to app_001;
-- 賦予 bookmazon schema 的使用權限
GRANT USAGE ON SCHEMA bookmazon to app_001;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA bookmazon TO app_001;
