# helpers.py

import re
from typing import List, Optional
import uuid

from fastapi import HTTPException, status
from models import CustomerInfo, OrderItem
import  nltk.tag.stanford as st
import pyap
from database import customers_collection, orders_collection

tagger = st.StanfordNERTagger('stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz', 'stanford-ner-2014-08-27/stanford-ner.jar')



# Function to create a new customer and add it to the database
def create_customer(name: str, address: str):
    # Generate a unique customer code
    customer_code = generate_customer_code()
    # Create a CustomerInfo instance
    customer = CustomerInfo(customer_name=name, customer_address=address, customer_code=customer_code)
    # Convert the CustomerInfo instance to a dict and store it in the database
    customers_collection.insert_one(customer.dict())
    return customer


# function to get an order
def get_order(order_id: str) -> Optional[dict]:
    order = orders_collection.find_one({"order_id": order_id}, {'_id': False})
    print(order)
    return order

#  a function to add items to an existing order
def add_to_order(order_id: str, order_items: List[OrderItem]) -> dict:
    order = orders_collection.find_one({"order_id": order_id})
    if order:
        orders_collection.update_one(
            {"order_id": order_id},
            {"$push": {"items": {"$each": [item.model_dump() for item in order_items]}}}
        )
        return {"response": "Items added to the order successfully!"}
    else:
        return {"response": "Order not found!"}

#  a function to remove an order
def remove_order(order_id: str) -> dict:
    result = orders_collection.delete_one({"order_id": order_id})
    if result.deleted_count > 0:
        return {"response": "Order removed successfully!"}
    else:
        return {"response": "Order not found!"}


# function to extract order_id
def extract_order_id(user_input: str) -> str:
    # Regular expression pattern to match UUID
    uuid_pattern = r"\b[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}\b"
    # Search for UUID pattern in user input
    match = re.search(uuid_pattern, user_input)
    if match:
        print(uuid.UUID(match.group()))
        return uuid.UUID(match.group())
    else:
        return None



def extract_name_address(user_input) -> CustomerInfo | None:
    addresses = pyap.parse(user_input, country="US")
    if addresses:
        addy = addresses[-1]

        tagged_words = tagger.tag(user_input.split())
        # Extract words with the 'PERSON' tag
        person_words = [word for word, tag in tagged_words if tag == 'PERSON']

        # Join the words into a string
        person= ' '.join(person_words)

        customer = CustomerInfo(customer_name=person, customer_address=str(addy), customer_code=generate_customer_code())

        customers_collection.insert_one(customer.model_dump())
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"response": "Addresses are only supported for "})




# Function to generate a unique customer code
def generate_customer_code() -> int:
    # random number generation
    return uuid.uuid4().int & (1 << 32) - 1