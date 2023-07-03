#FastAPI CRUD Operations with SQLAlchemy and PostgreSQL
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# Database connection configuration
db_url = "postgresql://postgres:apple123@localhost:5432/postgres"

# SQLAlchemy configuration
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Model for the data to be stored/retrieved (corresponds to the "customers_details" table)
# Customer, a subclass of Base, is mapped to a customers_details table in the database, Attributes in the Customer class correspond to the data types of the columns in the target table.
class Customer(Base):
    __tablename__ = "customers_details"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)


# Create the database tables
Base.metadata.create_all(bind=engine)


# Declare a Pydantic model that corresponds to the declarative base subclass (Customer class defined above).
class CustomerCreate(BaseModel):
    name: str
    age: int

# GET operation to fetch all customers
@app.get("/customers")
def get_all_customers():
    db = SessionLocal()

    try:
        customers = db.query(Customer).all()
        return customers
    finally:
        db.close()

# GET operation to fetch a customer by ID
@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    db = SessionLocal()

    try:
        customer = db.query(Customer).get(customer_id)
        if customer:
            return customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    finally:
        db.close()


# POST operation to create a new customer
@app.post("/customers")
def create_customer(customer: CustomerCreate):
    db = SessionLocal()

    try:
        new_customer = Customer(name=customer.name, age=customer.age)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    finally:
        db.close()


# PUT operation to update an existing customer on the basis of customer_id
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerCreate):
    db = SessionLocal()

    try:
        existing_customer = db.query(Customer).get(customer_id)
        if existing_customer:
            existing_customer.name = customer.name
            existing_customer.age = customer.age
            db.commit()
            db.refresh(existing_customer)
            return existing_customer
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    finally:
        db.close()


# DELETE operation to delete a customer by ID
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    db = SessionLocal()

    try:
        customer = db.query(Customer).get(customer_id)
        if customer:
            db.delete(customer)
            db.commit()
            return {"message": "Customer deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Customer not found")
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)