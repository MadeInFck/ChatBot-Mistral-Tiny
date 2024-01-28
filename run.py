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

app = gr.mount_gradio_app(app, iface.launch( server_name="0.0.0.0", server_port=5000), path='/chatbot')
#auth=(user, password),