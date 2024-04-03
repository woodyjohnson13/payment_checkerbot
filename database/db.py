from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Order,Payment

Base = declarative_base()





class Database:
        def __init__(self, db_url):
            self.engine = create_engine(db_url)
            self.Session = sessionmaker(bind=self.engine)

        def get_session(self):
            return self.Session()
        
        def get_order_by_lead_id(self, lead_ids):
            session = self.get_session()
            try:
                orders = session.query(Order).filter(Order.lead_id.in_(lead_ids)).all()
                return orders
            finally:
                session.close()

                
        def get_all_orders(self):
            session = self.get_session()
            try:
                orders = session.query(Order).all()
                return orders
            finally:
                session.close()



        def check (self):
            print("Connected")





