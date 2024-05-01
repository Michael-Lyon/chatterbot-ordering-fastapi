from fastapi import FastAPI
from .handlers import chat_handlers
from .models import ChatInput
from .database import menu_collection, orders_collection

app = FastAPI()

@app.post("/chat")
async def chat_with_bot(chat_input: ChatInput):
    print(chat_input)
    return await chat_handlers.process_request(chat_input.user_input)



# Endpoint to get menu
@app.get("/menu")
async def get_menu():
    chat_handlers.populate_menu()
    menu = list(menu_collection.find({}, {'_id': False}))  # Exclude '_id' from the result
    return {"menu": menu}




@app.get("/orders")
async def get_orders():
    orders = list(orders_collection.find({}, {'_id': False}))  # Exclude '_id' from the result
    return {"orders": orders}