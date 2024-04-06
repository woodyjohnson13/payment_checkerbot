from sqlalchemy import Column, Integer, String,Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    info = Column(String)
    lead_id = Column(Integer)


class Payment(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    lead_id=Column(String)
    date = Column(String)
    amount = Column(String)
    checking_account=Column(String)
