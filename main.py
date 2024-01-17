import gradio as gr
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from gtts import gTTS
from langdetect import detect
from uuid import uuid4

def chat_with_mistral(user_input):
    api_key = "f6jzkpIaRIqc93Xa7sxSc73A10TjRZUQ"
    model = "mistral-tiny"  # Use "Mistral-7B-v0.2" for "mistral-tiny"

    client = MistralClient(api_key=api_key)
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(
        model=model,
        messages=messages,
        temperature=0.2,
        # max_tokens=1000
    )

    text = chat_response.choices[0].message.content
    print(text)
    return text, text_to_speech(text)


def text_to_speech(text):
    language = detectLanguage(text)
    print(language)
    audio = gTTS(text=text, lang=language, slow=False)
    nameFile = f'{uuid4()}' + '.mp3'
    print(nameFile, type(nameFile))
    audio.save(nameFile)
    return nameFile


def detectLanguage(text):
    return detect(text)


iface = gr.Interface(
    fn=chat_with_mistral,
    inputs=gr.components.Textbox(label="Entrer un message", placeholder="Donne-moi un menu pour la journée!"),
    outputs=[gr.components.Text(label="Réponse du Chatbot"),
             gr.components.Audio(autoplay=True, label="Transcription de la réponse",)],
    title="Mistral AI Chatbot (mistral-tiny)",
    description="Interagissez avec l'API Mistral via ce chatbot.",
    examples=[["Donne-moi un menu pour la journée."]],
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch()
