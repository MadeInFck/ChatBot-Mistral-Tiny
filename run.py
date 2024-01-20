from fastapi import FastAPI
import gradio as gr
import os
from main import iface
from dotenv import load_dotenv

load_dotenv()
user = os.environ.get("user")
password = os.environ.get("password")
app = FastAPI()

@app.get('/')
async def root():
    return 'The chatbot is running at /chatbot', 200

app = gr.mount_gradio_app(app, iface.launch(auth=(user, password)), path='/chatbot')