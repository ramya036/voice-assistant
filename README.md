# Virtual Web Assistant

A voice-controlled personal assistant for Windows. Speak a command and it answers out loud or acts on it: open websites, search Wikipedia, find places on a map, check the weather, tell the time, tell jokes and more.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Windows](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)

## How it works

1. **Listens** through the microphone with `SpeechRecognition` and PyAudio.
2. **Understands** the command by matching keywords in the recognized text.
3. **Acts:** opens sites with `webbrowser`, searches Wikipedia, opens Google Maps for a place, tells jokes with `pyjokes`, and more.
4. **Speaks** the answer back with `pyttsx3`.

## Demo

| Command | Result |
|---|---|
| Open YouTube | ![Opening YouTube](https://github.com/vyshnavi1402/Virtual-Web-Assistant/assets/108367765/7b38c558-5e8c-433e-a46d-523613cb6bd6) |
| Search Wikipedia | ![Wikipedia search](https://github.com/vyshnavi1402/Virtual-Web-Assistant/assets/108367765/f0a3b861-12e1-4f6d-8092-6f026bbea041) |
| Find a location | ![Map location](https://github.com/vyshnavi1402/Virtual-Web-Assistant/assets/108367765/d8cff31f-da1b-46e1-8bf6-02ae205f817e) |
| Weather forecast | ![Weather](https://github.com/vyshnavi1402/Virtual-Web-Assistant/assets/108367765/11692383-5205-47c0-b92d-536ee97d8479) |
| Current time | ![Time](https://github.com/vyshnavi1402/Virtual-Web-Assistant/assets/108367765/13a65c18-80c4-4b16-b448-d9d8baa3cd83) |

## Run it (Windows)

```bash
pip install -r requirements.txt
python code.py
```

## Tech

Python · SpeechRecognition · PyAudio · pyttsx3 · Wikipedia API · pyjokes · BeautifulSoup · Requests
