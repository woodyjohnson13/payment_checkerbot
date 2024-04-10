from sqlalchemy import Column, Integer, String,Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Payment(Base):
    __tablename__ = 'bank'

    id = Column(Integer, primary_key=True)
    lead_id=Column(String)
    date = Column(String)
    amount = Column(String)
    checking_account=Column(String)
    payment_commentary=Column(String)

class Chat(Base):
    __tablename__ = 'bot_chats_and_sheets'

    id = Column(Integer, primary_key=True)
    chat_id=Column(String)
    sheet_id = Column(String)
