from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import *

Base = declarative_base()

class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.Session()

    def check (self):
        print("Connected")






# Example usage:
# db_url = 'mysql+mysqlconnector://username:password@localhost/mydatabase'
# db_connection = DBConnection(db_url)
# db_connection.create_tables()

# session = db_connection.get_session()

# Add a new user
# new_user = User(name='John', age=30)
# session.add(new_user)
# session.commit()

# Query users
# users = session.query(User).all()
# for user in users:
#     print(user.id, user.name, user.age)

# session.close()
