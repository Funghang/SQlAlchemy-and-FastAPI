# in this file, the SQLAlchemy model is defined.  
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#creates a subclass of declarative_base() called Base, which serves as the base class for all models in the application.
Base = declarative_base()


# The Customer class is defined as a subclass of Base and represents the customers_details table in the database.
# It has three attributes: id, name, and age, which are mapped to the respective columns in the table.
class Customer(Base):
    __tablename__ = "customers_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)