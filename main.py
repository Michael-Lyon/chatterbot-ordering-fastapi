from fastapi import FastAPI
from handlers import chat_handlers
from models import ChatInput

app = FastAPI()

@app.post("/chat")
async def chat_with_bot(chat_input: ChatInput):
    return await chat_handlers.process_request(chat_input.user_input)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
