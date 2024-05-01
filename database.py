# database.py

from typing import List
from pymongo import MongoClient

from models import Order

client = MongoClient('mongodb://mongo:MlnHXEHaSvWNoYVxQFjHTZXhGzJAUxgv@monorail.proxy.rlwy.net:16429')
db = client["chatbot_database"]
orders_collection = db.orders
menu_collection = db.menu
customers_collection = db.customers

temp_orders:List[Order] = []