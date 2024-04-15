from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Payment,PaymentText




Base = declarative_base()



class Database:
        def __init__(self, db_url):
            self.engine = create_engine(db_url,echo=True)
            self.Session = sessionmaker(bind=self.engine)
            
        def get_session(self):
            return self.Session()
                              
        def create_payment(self,lead_id, date, amount, checking_account,payment_message,chat_id,reply_message):
            session = self.get_session()
            
            payment = Payment(lead_id=lead_id, date=date, amount=amount, checking_account=checking_account,payment_message=payment_message,chat_id=chat_id,reply_message=reply_message,status=0)
            
            try:
                session.add(payment)
                session.commit()
                print("Payment created successfully!")
            except Exception as e:
                session.rollback()
                print(f"Error creating payment: {e}")
            finally:
                session.close()
                
                
                
        def create_payment_text(self, text):
            session = self.get_session()
            payment_id = None
            
            try:
                payment_text = PaymentText(text=text)
                session.add(payment_text)
                session.commit()
                payment_id = payment_text.id
                print("Payment text created successfully!")
            except Exception as e:
                session.rollback()
                print(f"Error creating payment text: {e}")
            finally:
                session.close()
                
            return payment_id



        def get_payment_text(self, payment_id):
            session = self.get_session()
            payment_text = None
            
            try:
                # Query the PaymentText object based on the provided payment_id
                payment_text = session.query(PaymentText).filter_by(id=payment_id).first()
            except Exception as e:
                print(f"Error getting payment text: {e}")
            finally:
                session.close()
                
            return payment_text



        def delete_payment_text(self, payment_id):
            session = self.get_session()
            
            try:
                # Query the PaymentText object based on the provided payment_id
                payment_text = session.query(PaymentText).filter_by(id=payment_id).first()
                
                if payment_text:
                    session.delete(payment_text)
                    session.commit()
                    print("Payment text deleted successfully.")
                else:
                    print("Payment text not found.")
            except Exception as e:
                # Rollback the transaction in case of an error
                session.rollback()
                print(f"Error deleting payment text: {e}")
            finally:
                session.close()






