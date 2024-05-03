# handlers/chat_handler.py
from typing import List
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import uuid
import nltk
from nltk import Tree
TRAINED = False


from helpers import add_to_order, extract_name_address, extract_order_id, get_order, remove_order
from models import NAME_FLAG, MenuItem, Order, OrderItem
from database import temp_orders, orders_collection, menu_collection



# Initialize ChatBot with MongoDB storage adapter
chatbot = ChatBot('CustomerServiceBot',
                storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
                #             mongodb+srv://mongo:MlnHXEHaSvWNoYVxQFjHTZXhGzJAUxgv@monorail.proxy.rlwy.net/
                database_uri="mongodb://pygod:pygod1234@monorail.proxy.rlwy.net:16429/chatbot_database",
                )


# Global flag
TRAINED = False

def train_chatbot():
    global TRAINED
    if not TRAINED:
        trainer = ChatterBotCorpusTrainer(chatbot)
        trainer.train("chatterbot.corpus.english")
        TRAINED = True



# Function to populate the menu collection with initial data
def populate_menu():
    # List of menu items to add
    menu_items = [
            MenuItem(name="Pizza", price=10.99),
            MenuItem(name="Burger", price=8.99),
            MenuItem(name="Pasta", price=9.99),
            MenuItem(name="Salad", price=7.99),
            MenuItem(name="Sandwich", price=6.99),
            MenuItem(name="Steak", price=15.99),
            MenuItem(name="Chicken Wings", price=8.49),
            MenuItem(name="Sushi", price=12.99),
            MenuItem(name="Tacos", price=7.99),
            MenuItem(name="Fish and Chips", price=11.99),
            MenuItem(name="Soup", price=5.99),
            MenuItem(name="Ramen", price=9.49),
    ]

    # Insert each item into the menu collection
    for item in menu_items:
        # Check if the item already exists in the collection
        if not menu_collection.find_one({"name": item.name}):
            menu_collection.insert_one(item.model_dump())



# to get menu
async def get_menu():
    populate_menu()
    menu = list(menu_collection.find({}, {'_id': False}))  # Exclude '_id' from the result
    return {"menu": menu}




#  a function to extract order details
def extract_order_details(user_input: str) -> Order:
    order_items: List[OrderItem] = []
    grammar = 'OrderItem: {<CD>?<NNP>?<NN>?}'
    parser = nltk.RegexpParser(grammar)

    user_input_pos = nltk.pos_tag(user_input.split())
    parsed_data = parser.parse(user_input_pos)

    for subtree in parsed_data:
        if isinstance(subtree, Tree) and subtree.label() == 'OrderItem':
            quantity = None
            item_name = None
            for token, pos in subtree.leaves():
                if pos == 'CD':  # CD denotes a cardinal number
                    quantity = int(token)
                elif pos in ['NN', 'NNP', 'NNS', 'NNPS']:  # NN/NNS/NNP/NNPS denote a noun or nouns
                    item_name = token
            if quantity and item_name:
                order_items.append(OrderItem(quantity=quantity, item_name=item_name))


    # Generate a unique order ID
    order_id = uuid.uuid4()


    # Create and return the Order instance
    return Order(items=order_items, customer_info=None, paid=False, order_id=order_id)



# Helper function to process menu and order requests
async def process_request(user_input):
    global NAME_FLAG

    # Check if user is entering customer details
    if NAME_FLAG:
        customer_detail = extract_name_address(user_input)
        if customer_detail:
            order = temp_orders[-1]
            order.customer_info = customer_detail
            NAME_FLAG = False
            return await create_new_order(order)

    # Check if user is asking for the menu
    if 'menu' in user_input.lower():
        return await get_menu()
    elif "track" in user_input.lower() or "track order" in user_input.lower():
        order_id = extract_order_id(user_input)
        return get_order(order_id)

    # Check if user wants to place an order
    elif 'order' in user_input.lower():
        # Extract order details from user_input and create an order
        order_details = extract_order_details(user_input)
        return await create_new_order(order_details)

    # Check if user wants to add items to an existing order
    elif 'add' in user_input.lower():
        # Extract order items from user input
        order_items = extract_order_details(user_input)
        # Extract order ID from user input
        order_id = extract_order_id(user_input)
        if order_items and order_id:
            return await add_to_order(order_id, order_items)
        else:
            return {"response": "Invalid input. Please specify order ID and items to add."}
    # Check if user wants to remove an order
    elif 'remove' in user_input.lower():
        # Extract order ID from user input
        order_id = extract_order_id(user_input)
        if order_id:
            return remove_order(order_id)
        else:
            return {"response": "Invalid input. Please specify order ID to remove."}

    else:
        # Proceed with the chatbot response for other queries
        response = chatbot.get_response(user_input)
        return {"response": str(response)}


async def create_new_order(order: Order):
    global NAME_FLAG
    if order.customer_info is None:
        temp_orders.append(order)
        NAME_FLAG = True
        return {"data":{"order_id": order.order_id},"response": "Order has been recieved please enter your name and address to complete order."}
    # Convert the order to a dict so it can be stored in MongoDB
    order_dict = order.model_dump()
    # Insert the order into the 'orders' collection
    result = orders_collection.insert_one(order_dict)
    if result.acknowledged:
        return {"order": order, "response": "Your order has been placed successfully! Keep your code as it serves a s your unique identifier!"}
    else:
        return {"response": "There was an error placing your order. Please try again."}


