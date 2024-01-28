import gradio as gr
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from gtts import gTTS
from langdetect import detect

import os
from dotenv import load_dotenv

load_dotenv()

history = []
languages = [("French", "fr"), ("English", "en"), ("Afrikaans", "af"), ("Arabic", "ar"), ("Bulgarian", "bg"),
             ("Bengali", "bn"), ("Catalan", "ca"), ("Czech", "cs"), ("Welsh", "cy"), ("Danish", "da"), ("German", "de"),
             ("Greek", "el"), ("Spanish", "es"), ("Estonian", "et"), ("Persian", "fa"), ("Finnish", "fi"),
             ("Gujarati", "gu"), ("Hebrew", "he"),
             ("Hindi", "hi"), ("Croatian", "hr"), ("Hungarian", "hu"), ("Indonesian", "id"), ("Italian", "it"),
             ("Japanese", "ja"), ("Kannada", "kn"), ("Korean", "ko"), ("Lithuanian", "lt"), ("Latvian", "lv"),
             ("Macedonian", "mk"), ("Malayalam", "ml"), ("Marathi", "mr"), ("Nepali", "ne"), ("Dutch", "nl"),
             ("Norwegian", "no"), ("Punjabi", "pa"), ("Polish", "pl"),
             ("Portuguese", "pt"), ("Romanian", "ro"), ("Russian", "ru"), ("Slovak", "sk"), ("Slovenian", "sl"),
             ("Somali", "so"), ("Albanian", "sq"), ("Swedish", "sv"), ("Swahili", "sw"), ("Tamil", "ta"),
             ("Telugu", "te"), ("Thai", "th"), ("Tagalog", "tl"), ("Turkish", "tr"), ("Ukrainian", "uk"),
             ("Urdu", "ur"), ("Vietnamese", "vi"),
             ("Chinese", "zh")]


def chat_with_mistral(user_input, model, language, maxtoken, temperature):
    history.append(user_input)
    history_input = "\n".join(history)
    print(history_input)
    # Ask to answer in selected language
    lang = getLanguage(language)

    # Mistral API
    api_key = os.environ.get("mistral_api_key")
    model = model
    client = MistralClient(api_key=api_key)
    messages = [ChatMessage(role="user", content=history_input + ". Your answer must only use " + lang + "words.")]

    chat_response = client.chat(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=maxtoken
    )

    text = chat_response.choices[0].message.content
    # print(text)
    return text, text_to_speech(text)


def text_to_speech(text):
    if text == "":
        return None
    else:
        language = detectLanguageForAudio(text)
        audio = gTTS(text=text, lang=language, slow=False)
        audio.save(f'sample.mp3')
        return f'sample.mp3'


def detectLanguageForAudio(text):
    return detect(text)


def reset():
    global history
    history = []


def getLanguage(lang):
    for l in languages:
        if lang in l:
            return l[0]


with gr.Blocks(theme="base", title="Mistral Chatbot") as iface:
    # Markdown
    gr.Markdown("# Chatbot powered by Mistral AI models")
    gr.Markdown("## Interact with Mistral API via this chatbot.")

    with gr.Row():
        # Chatbot
        with gr.Column(scale=4):
            # Inputs
            textbox = gr.components.Textbox(label="Compose your message", placeholder="Prompt here!", scale=2)
            with gr.Row(equal_height=True):
                clearBtn = gr.components.ClearButton(value="Clear", variant="stop")
                submitBtn = gr.components.Button(value="Submit", variant="primary")

            # Outputs
            outputs = [gr.components.Text(label="Chatbot response"),
                       gr.components.Audio(autoplay=True, label="Audio transcription of the response", )]

        # Settings
        with gr.Column(scale=1):
            with gr.Row(equal_height=True):
                modelDropdown = gr.components.Dropdown(scale=1,
                                                       choices=[("Mistral Tiny", "mistral-tiny"),
                                                                ("Mistral Small", "mistral-small"),
                                                                ("Mistral Medium", "mistral-medium")],
                                                       label="Choose your Mistral AI model",
                                                       value="mistral-tiny")
                langDropdown = gr.components.Dropdown(scale=1,
                                                      choices=languages, label="Choose the language of the answer",
                                                      value="fr")
            with gr.Row(equal_height=True):
                token = gr.components.Number(value=1000, scale=1, label="Number of maximum tokens", step=10,
                                             minimum=100,
                                             maximum=10000, precision=0, info="Choose between 100 and 10000")
                slider = gr.Slider(0, 1.0, value=0.2, step=0.1, scale=1, label="Température",
                                   info="Choose between 0 and 1, more accuracy close from 0")





    # Submit button
    submitBtn.click(chat_with_mistral, inputs=[textbox, modelDropdown, langDropdown, token, slider], outputs=outputs)
    clearBtn.add(textbox)
    clearBtn.click(reset)
    # Reset button

    # Examples
    # def chat_with_mistral(user_input, model, language, token, temperature)
    gr.Examples([["Give me a meal plan for the day."]], textbox, outputs,
                chat_with_mistral, cache_examples=False)

# if __name__ == "__main__":
#   iface.launch()
