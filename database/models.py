from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Payment(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    lead_id=Column(String)
    date = Column(String)
    amount = Column(String)
    checking_account=Column(String)
    payment_message=Column(String)
    reply_message=Column(String)
    chat_id=Column(String)
    status=Column(Integer)


