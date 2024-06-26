from fastapi import FastAPI
from handlers import chat_handlers
from models import ChatInput
from database import menu_collection, orders_collection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Train the chatbot


@app.get("/")
async def root():
    chat_handlers.train_chatbot()
    return {"A simple chat bot"}

@app.post("/chat")
async def chat_with_bot(chat_input: ChatInput):
    chat_handlers.train_chatbot()
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


