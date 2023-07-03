#This is the main file that imports the necessary modules and defines the FastAPI application (app) using the FastAPI() class.
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi_database import SessionLocal, engine
from fastapi_schema import CustomerCreate
from fastapi_crud import get_all_customers, get_customer, create_customer, update_customer, delete_customer

from fastapi_models import Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get a database session for each request
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# GET operation to fetch all customers using fast api decorator
@app.get("/customers")
def read_customers(db: Session = Depends(get_db)):
    customers = get_all_customers(db)
    return customers


# GET operation to fetch a customer by ID
@app.get("/customers/{customer_id}")
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if customer:
        return customer
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# POST operation to create a new customer
@app.post("/customers")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = create_customer(db, customer)
    return new_customer


# PUT operation to update an existing customer on the basis of customer_id
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    existing_customer = update_customer(db, customer_id, customer)
    if existing_customer:
        return existing_customer
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


# DELETE operation to delete a customer by ID
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    response = delete_customer(db, customer_id)
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Customer not found")

#application is run using the uvicorn.run() function, specifying the host and port to listen on.

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)