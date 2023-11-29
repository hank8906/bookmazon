-- 移除 "book" 表格
DROP TABLE bookmazon.book;
-- 創建 "book" 表格
CREATE TABLE bookmazon.book (
    book_id VARCHAR(13) NOT NULL,       --書籍ID
    book_name VARCHAR(255) NOT NULL,    --書名
    book_author VARCHAR(255),           --作者
    book_publisher VARCHAR(255),        --出版社
    book_price NUMERIC(10, 2) NOT NULL, --售價
    book_category VARCHAR(50),          --書籍分類
    book_image_path VARCHAR(255),       --書籍圖片路徑
    update_datetime TIMESTAMP,          --更新時間
    create_datetime TIMESTAMP,          --建立時間
    CONSTRAINT pk_book PRIMARY KEY (book_id)
);

-- 添加 "book" 表格的註解
COMMENT ON TABLE bookmazon.book IS '書籍資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.book.book_id         IS '書籍ID';
COMMENT ON COLUMN bookmazon.book.book_name       IS '書名';
COMMENT ON COLUMN bookmazon.book.book_author     IS '作者';
COMMENT ON COLUMN bookmazon.book.book_publisher  IS '出版社';
COMMENT ON COLUMN bookmazon.book.book_price      IS '售價';
COMMENT ON COLUMN bookmazon.book.book_category   IS '書籍分類';
COMMENT ON COLUMN bookmazon.book.book_image_path IS '書籍圖片路徑';
COMMENT ON COLUMN bookmazon.book.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.book.create_datetime IS '建立時間';
