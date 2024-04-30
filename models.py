# bot_models.py

from pydantic import BaseModel
from typing import List, Optional
import uuid

NAME_FLAG = False
TRACK_ORDER_FLAG = False
ADD_TO_ORDER_FLAG = False


#  models for menu items and orders
class MenuItem(BaseModel):
    name: str
    price: float

class OrderItem(BaseModel):
    item_name: str
    quantity: int

class CustomerInfo(BaseModel):
    customer_name: str
    customer_address: str
    customer_code: int

class Order(BaseModel):
    items: List[OrderItem]
    customer_info: Optional[CustomerInfo]
    paid: bool
    order_id: uuid.UUID



class ChatInput(BaseModel):
    user_input: str