#This file contains the CRUD (Create, Read, Update, Delete) operations for interacting with the database.

from sqlalchemy.orm import Session
from fastapi_models import Customer
from fastapi_schema import CustomerCreate

#Retrieves a customer from the database based on the provided customer_id.
def get_customer(db: Session, customer_id: int):
    return db.query(Customer).get(customer_id)

#Retrieves all customers from the database.
def get_all_customers(db: Session):
    return db.query(Customer).all()

#Creates a new customer in the database based on the provided customer object.
def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(name=customer.name, age=customer.age)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

#Updates an existing customer in the database based on the provided customer_id and customer object.
def update_customer(db: Session, customer_id: int, customer: CustomerCreate):
    existing_customer = db.query(Customer).get(customer_id)
    if existing_customer:
        existing_customer.name = customer.name
        existing_customer.age = customer.age
        db.commit()
        db.refresh(existing_customer)
        return existing_customer

# Deletes a customer from the database based on the provided customer_id.
def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).get(customer_id)
    if customer:
        db.delete(customer)
        db.commit()
        return {"message": "Customer deleted successfully"}