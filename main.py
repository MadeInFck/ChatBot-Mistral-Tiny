import gradio as gr
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from gtts import gTTS
from langdetect import detect


import os
from dotenv import load_dotenv

load_dotenv()


def chat_with_mistral(user_input, model):
    api_key = os.environ.get("mistral_api_key")
    model = model
    client = MistralClient(api_key=api_key)
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(
        model=model,
        messages=messages,
        temperature=0.2,
        # max_tokens=1000
    )

    text = chat_response.choices[0].message.content
    #print(text)
    return text, text_to_speech(text)


def text_to_speech(text):
    if text == "":
        return None
    else:
        language = detectLanguage(text)
        audio = gTTS(text=text, lang=language, slow=False)
        audio.save(f'sample.mp3')
        return f'sample.mp3'


def detectLanguage(text):
    return detect(text)


iface = gr.Interface(
    fn=chat_with_mistral,
    inputs=[gr.components.Textbox(label="Compose your message", placeholder="Prompt here!"),
            gr.components.Dropdown(choices=[("Mistral Tiny", "mistral-tiny"), ("Mistral Small", "mistral-small"), ("Mistral Medium", "mistral-medium")], label="Choose your Mistral AI model", value="mistral-tiny")],
    outputs=[gr.components.Text(label="Chatbot response"),
             gr.components.Audio(autoplay=True, label="Audio transcription of the response", )],
    title="Chatbot powered by Mistral AI models",
    description="Interact with Mistral API via this chatbot.",
    examples=[["Give me a meal plan for the day."]],
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch()
