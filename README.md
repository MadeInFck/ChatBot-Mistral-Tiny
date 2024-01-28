---
title: ChatBot-Mistral
app_file: run.py
sdk: gradio
sdk_version: 4.14.0
---
[![Python application](https://github.com/MadeInFck/ChatBot-Mistral-Tiny/actions/workflows/python-app.yml/badge.svg)](https://github.com/MadeInFck/ChatBot-Mistral-Tiny/actions/workflows/python-app.yml)

# ChatBot-Mistral-Tiny
 ChatBot based on [Mistral AI model (Mistral Tiny 7B)](mistral.ai) 

 
## Gradio
Interface using [Gradio](gradio.app) for a fast and nice UI development.

## [gTTS](https://gtts.readthedocs.io/en/latest/)
Answer from the bot is transcribed to speech and can be played if needed. Language is automatically detected by the python lib [langDetect](https://pypi.org/project/langdetect/).

![Snapshot of the ChatBot](/ChatBot-MistralAI.png)

## Todos
* Add chat interface type
* Add dropdown to choose language for answer.