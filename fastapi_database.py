#This file handles the SQL engine connection and session creation.

#It also 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection configuration, defines the db_url variable, which represents the URL for connecting to the PostgreSQL database.
db_url = "postgresql://postgres:apple123@localhost:5432/postgres"

# SQLAlchemy configuration, creates the SQLAlchemy engine and sessionmaker objects using the create_engine and sessionmaker functions from the sqlalchemy module.
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)