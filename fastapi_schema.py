#The CustomerCreate class is a subclass of BaseModel and represents the schema for the request body when creating a new customer.

from pydantic import BaseModel


# Pydantic model for creating a customer
class CustomerCreate(BaseModel):
    name: str
    age: int