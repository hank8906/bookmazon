from datetime import datetime

from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import mapped_column

from model.BaseModel import Base

class Order(Base):
    __tablename__ = 'order'
    __table_args__ = {"schema": "bookmazon"}

    order_id = mapped_column(Integer, primary_key=True)
    user_account = mapped_column(String(20), nullable=False)
    recipient_name = mapped_column(String(50))
    order_total_price = mapped_column(Numeric(10, 2))
    order_status = mapped_column(String(1))
    payment_status = mapped_column(String(1))
    shipping_status = mapped_column(String(1))
    shipping_address = mapped_column(String(255))
    update_datetime = mapped_column(DateTime, default=datetime.now())
    create_datetime = mapped_column(DateTime, default=datetime.now())
