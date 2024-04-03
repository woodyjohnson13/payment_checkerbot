from sqlalchemy import Column, Integer, String,Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    info = Column(String)
    lead_id = Column(Integer)


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    payment_amount = Column(Numeric(precision=10, scale=2))
    lead_id = Column(Integer)