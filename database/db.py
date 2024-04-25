from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Payment,PaymentText,Chat,ProcessedLead
import mysql.connector
import re

import os
from dotenv import load_dotenv

load_dotenv(override=True)
db_url = os.getenv('DB_URL')


Base = declarative_base()




class Database:
        def __init__(self, db_url):
            self.engine = create_engine(db_url,echo=True)
            self.Session = sessionmaker(bind=self.engine)
            
        def get_session(self):
            return self.Session()
                              
        def create_payment(self,lead_id, date, amount, checking_account,payment_message,chat_id,reply_message,status):
            session = self.get_session()
            
            payment = Payment(lead_id=lead_id, date=date, amount=amount, checking_account=checking_account,payment_message=payment_message,chat_id=chat_id,reply_message=reply_message,status=status)
            
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

      
                
        def get_mapping(self, message, chat_id):
                    try:
                        
                        conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="8121974",
                        database="payemnt_bot"
                    )
                        
                        cursor = conn.cursor(dictionary=True)

                        query = """
                            SELECT *
                            FROM bot_transfer
                            WHERE chat_id = %s
                            AND %s LIKE CONCAT('%', key_phrase, '%')
                            LIMIT 1
                        """
                        cursor.execute(query, (chat_id,message))
                        mapping = cursor.fetchone()

                        if mapping:
                            return {
                                'date_today': mapping['date_today'],
                                'payment_date': mapping['payment_date'],
                                'payment_message': mapping['payment_message'],
                                'reply_message': mapping['reply_message'],
                                'chat_id': mapping['chat_id'],
                                'payment_column': mapping['payment_column'],
                                'paymentmethod': mapping['paymentmethod'],
                                'paymentmethod_name': mapping['paymentmethod_name']
                            }
                        #!Case with unknown mapping
                        else:
                            query = """
                            SELECT *
                            FROM bot_transfer
                            WHERE chat_id = %s
                            AND key_phrase='Неизвестно'
                            LIMIT 1
                        """
                        cursor.execute(query, (chat_id,))
                        mapping = cursor.fetchone()
                        
                        if mapping:
                            return {
                                'date_today': mapping['date_today'],
                                'payment_date': mapping['payment_date'],
                                'payment_message': mapping['payment_message'],
                                'reply_message': mapping['reply_message'],
                                'chat_id': mapping['chat_id'],
                                'payment_column': mapping['payment_column'],
                                'paymentmethod': mapping['paymentmethod'],
                                'paymentmethod_name': mapping['paymentmethod_name']
                            }
                            
                    except Exception as e:
                        print(f"Error determining transfer: {e}")
                        return None
                    finally:
                        if 'cursor' in locals():
                            cursor.close()
                        if 'conn' in locals():
                            conn.close()

        def get_sheet_id(self,chat_id):
            session = self.get_session()
            try:
                sheet_id = session.query(Chat).filter_by(chat_id=chat_id).first()
                if sheet_id:
                        return {
                            'sheet_id': sheet_id.sheet_id, 
                        }
                else:
                        return {}  #
            except Exception as e:
                    print(f"Error")
                    return None  
            finally:
                    session.close()

        def get_avaliable_chats(self):
            # Connect to the database
            session = self.get_session()

            # Query the database to get all lead IDs
            all_chats = []
            for chat in session.query(Chat):
                # Append the lead ID to the list
                all_chats.append(chat.chat_id)

            # Close the session
            session.close()
            
            return all_chats
        
        def get_payed_lead_ids(self):
            # Connect to the database
            session = self.get_session()

            # Query the database to get all lead IDs
            all_lead_ids = []
            for lead in session.query(ProcessedLead).filter(ProcessedLead.partly_payed == 0):
                # Append the lead ID to the list
                all_lead_ids.append(lead.lead_id)

            # Close the session
            session.close()
            
            return all_lead_ids
            
        def process_lead_id(self, lead_id, partly):
            # Connect to the database
            session = self.get_session()

            # Search for an existing record with the given lead_id
            existing_lead = session.query(ProcessedLead).filter_by(lead_id=lead_id).first()

            if existing_lead:
                # If the record exists, update its partly_payed value
                existing_lead.partly_payed = partly
            else:
                # If the record doesn't exist, create a new one
                new_lead = ProcessedLead(lead_id=lead_id, partly_payed=partly)
                session.merge(new_lead)

            # Commit the transaction and close the session
            session.commit()
            session.close()            
            
        
# db=Database(db_url)
# print(db.get_mapping("a","-1002052638653"))
