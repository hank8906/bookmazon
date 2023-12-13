INSERT INTO bookmazon.book
(book_id, book_name, book_author, book_publisher, book_price, book_category, book_image_path, update_datetime, create_datetime)
VALUES('1484226976', 'Beginning Pixlr Editor: Learn to Edit Digital Photos Using this Free Web-Based App', 'Phillip Whitt', 'Apress', 1380.00, 'Fiction', 'assets/img/book/book_2.jpg', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');
INSERT INTO bookmazon.book
(book_id, book_name, book_author, book_publisher, book_price, book_category, book_image_path, update_datetime, create_datetime)
VALUES('9059052471', 'Creating a Photo Book for Seniors', 'Studio Visual Steps', 'Visual Steps Publishing', 360.00, 'Non-Fiction', 'assets/img/book/book_3.jpg', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');
INSERT INTO bookmazon.book
(book_id, book_name, book_author, book_publisher, book_price, book_category, book_image_path, update_datetime, create_datetime)
VALUES('158717149X', 'Out of Sight', 'Seymour Simon', 'Chronicle Books', 24.99, 'Mystery', 'assets/img/book/book_4.jpg', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');
INSERT INTO bookmazon.item
(item_id, book_id, item_status, book_count, provider_account, update_datetime, create_datetime)
VALUES(2, '9059052471', '0', 1, 'Provider2', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');
INSERT INTO bookmazon.item
(item_id, book_id, item_status, book_count, provider_account, update_datetime, create_datetime)
VALUES(3, '158717149X', '1', 3, 'Provider3', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');
INSERT INTO bookmazon.item
(item_id, book_id, item_status, book_count, provider_account, update_datetime, create_datetime)
VALUES(1, '1484226976', '1', 5, 'Provider1', '2023-12-02 21:13:55.512', '2023-12-02 21:13:55.512');