from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Payment

Base = declarative_base()





class Database:
        def __init__(self, db_url):
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)

        def get_session(self):
            return self.Session()
                              
        def create_payment(self,lead_id, date, amount, checking_account):
            session = self.get_session()
            
            payment = Payment(lead_id=lead_id, date=date, amount=amount, checking_account=checking_account)
            
            try:
                session.add(payment)
                session.commit()
                print("Payment created successfully!")
            except Exception as e:
                session.rollback()
                print(f"Error creating payment: {e}")
            finally:
                session.close()





