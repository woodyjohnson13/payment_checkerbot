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


class PaymentText(Base):
    __tablename__ = 'payment_text'

    id = Column(Integer, primary_key=True)
    text=Column(String)
    

class Chat(Base):
    __tablename__ = 'bot_chats_and_sheets'

    id = Column(Integer, primary_key=True)
    chat_id=Column(String)
    sheet_id = Column(String)


class ProcessedLead(Base):
    __tablename__ = 'processed_lead_ids'

    id = Column(Integer, primary_key=True)
    lead_id=Column(String)
    partly_payed = Column(Integer)
