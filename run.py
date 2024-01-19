from fastapi import FastAPI
import gradio as gr

from main import iface

app = FastAPI()

@app.get('/')
async def root():
    return 'The chatbot is running at /chatbot', 200

app = gr.mount_gradio_app(app, iface, path='/chatbot')