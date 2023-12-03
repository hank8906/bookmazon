from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from model.BaseModel import Base
from datetime import datetime

class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {"schema": "bookmazon"}
    item_id = mapped_column(Integer, primary_key=True)
    book_id = mapped_column(String(13), ForeignKey('bookmazon.book.book_id'))
    item_status = mapped_column(String(1))
    book_count = mapped_column(Integer)
    provider_account = mapped_column(String(20), ForeignKey('bookmazon.user.user_account'))
    update_datetime = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())


# CREATE TABLE bookmazon.item (
#     item_id SERIAL NOT NULL,            -- 品項ID
#     book_id VARCHAR(13) NOT NULL,       -- 書籍ID (外部鍵)
#     item_status VARCHAR(1),             -- 商品狀態 (0: 有販售, 1: 已販售)
#     book_count INTEGER NOT NULL,        -- 庫存數
#     provider_account VARCHAR(20),       -- 提供者帳號 (外部鍵)
#     update_datetime TIMESTAMP,          -- 更新時間
#     create_datetime TIMESTAMP,          -- 建立時間
#     CONSTRAINT pk_item PRIMARY KEY (item_id)
# );