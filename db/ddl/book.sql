-- 創建 "book" 表格
CREATE TABLE bookmazon.book (
    book_id varchar(13),
    book_name varchar(255),
    book_author varchar(255),
    book_publisher varchar(255),
    book_price numeric(10, 2),
    book_category varchar(50),
    book_image_path varchar(255),
    update_datetime timestamp,
    create_datetime timestamp,
    CONSTRAINT pk_book PRIMARY KEY (book_id)
);

-- 添加 "book" 表格的註解
COMMENT ON TABLE bookmazon.book IS '書籍資訊表';

-- 添加每個列的註解
COMMENT ON COLUMN bookmazon.book.book_id IS '書籍ID';
COMMENT ON COLUMN bookmazon.book.book_name IS '書名';
COMMENT ON COLUMN bookmazon.book.book_author IS '作者';
COMMENT ON COLUMN bookmazon.book.book_publisher IS '出版社';
COMMENT ON COLUMN bookmazon.book.book_price IS '售價';
COMMENT ON COLUMN bookmazon.book.book_category IS '書籍分類';
COMMENT ON COLUMN bookmazon.book.book_image_path IS '書籍圖片路徑';
COMMENT ON COLUMN bookmazon.book.update_datetime IS '更新時間';
COMMENT ON COLUMN bookmazon.book.create_datetime IS '建立時間';
