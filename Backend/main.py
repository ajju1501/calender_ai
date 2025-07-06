from fastapi import FastAPI, Request
from pydantic import BaseModel
from agent import handle_user_input

app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    response = handle_user_input(msg.text)
    return {"response": response}
