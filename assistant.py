"""Lisa, a voice assistant. Listens on the microphone, or reads typed commands with --text.

    python assistant.py          # talk to it
    python assistant.py --text   # type commands instead (no microphone needed)
    python assistant.py --mute   # print replies instead of speaking them
"""
from __future__ import annotations

import argparse
import webbrowser

from commands import Services, greeting, parse, respond


def wiki_summary(topic: str) -> str:
    import wikipedia

    return wikipedia.summary(topic, sentences=2, auto_suggest=False)


def tell_joke() -> str:
    import pyjokes

    return pyjokes.get_joke()


def weather(place: str = "") -> str:
    """Current conditions from wttr.in, a free weather service with a plain-text API."""
    import requests

    text = requests.get(f"https://wttr.in/{place}", params={"format": "%l: %C, %t"}, timeout=8).text.strip()
    return f"Weather in {text}"


class Voice:
    def __init__(self, mute: bool):
        self.engine = None
        if not mute:
            import pyttsx3  # uses SAPI5 on Windows, NSSpeech on macOS, eSpeak on Linux

            self.engine = pyttsx3.init()

    def say(self, text: str) -> None:
        print(f"Lisa: {text}")
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()


def microphone_listener():
    import speech_recognition as sr

    r = sr.Recognizer()
    r.pause_threshold = 0.6

    def listen() -> str:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            return ""

    return listen


def main() -> None:
    p = argparse.ArgumentParser(description="Lisa, a voice assistant")
    p.add_argument("--text", action="store_true", help="type commands instead of speaking")
    p.add_argument("--mute", action="store_true", help="print replies instead of speaking them")
    args = p.parse_args()

    voice = Voice(args.mute)
    listen = (lambda: input("You: ")) if args.text else microphone_listener()
    services = Services(wiki=wiki_summary, joke=tell_joke, weather=weather)

    voice.say(greeting(services.now()))
    while True:
        try:
            heard = listen()
        except (EOFError, KeyboardInterrupt):
            break
        if not heard.strip():
            continue
        reply = respond(parse(heard), services)
        voice.say(reply.say)
        if reply.open_url:
            webbrowser.open(reply.open_url)
        if reply.quit:
            break


if __name__ == "__main__":
    main()
