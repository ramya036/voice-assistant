"""Understand a spoken command and decide what to do, with no audio or browser code.

parse() turns text like "where is Atlanta" into an Intent, and respond() turns an
Intent into a Response: what to say, and optionally a URL to open. Anything that
needs the outside world (clock, Wikipedia, jokes, weather) is passed in, so the
logic is easy to test.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import quote_plus

ASSISTANT_NAME = "Lisa"


@dataclass(frozen=True)
class Intent:
    name: str
    arg: str = ""


@dataclass(frozen=True)
class Response:
    say: str
    open_url: str | None = None
    quit: bool = False


SITES = {"youtube": "https://www.youtube.com", "google": "https://www.google.com",
         "gmail": "https://mail.google.com", "github": "https://github.com",
         "linkedin": "https://www.linkedin.com", "maps": "https://www.google.com/maps"}

NAMES = {"youtube": "YouTube", "github": "GitHub", "linkedin": "LinkedIn", "gmail": "Gmail"}

# Order matters: the first matching rule wins, so specific commands come before
# the general "who is / what is" Wikipedia question.
RULES: list[tuple[str, re.Pattern]] = [
    ("quit",      re.compile(r"\b(ok bye|goodbye|bye|exit|quit|stop listening)\b")),
    ("time",      re.compile(r"\b(what(?:'s| is) the time|the time|what time is it)\b")),
    ("date",      re.compile(r"\b(what(?:'s| is) the date|today's date|what day is it)\b")),
    ("joke",      re.compile(r"\bjoke\b")),
    ("weather",   re.compile(r"\b(weather|temperature)(?: in (?P<arg>.+))?")),
    ("open_site", re.compile(r"\bopen (?P<arg>[a-z]+)")),
    ("locate",    re.compile(r"\bwhere is (?P<arg>.+)")),
    ("wikipedia", re.compile(r"(?:search )?wikipedia (?:for )?(?P<arg>.+)|(?P<arg2>.+?) (?:on|from) wikipedia|(?:who|what) is (?P<arg3>.+)")),
    ("music",     re.compile(r"\bplay (?P<arg>.+)")),
    ("search",    re.compile(r"\b(?:search|google|look up) (?:for )?(?P<arg>.+)")),
    ("greet",     re.compile(r"\b(hello|hi|hey)\b")),
]


def parse(text: str) -> Intent:
    """Match on lowercase text, but keep the speaker's capitalisation in the argument."""
    original = re.sub(r"\s+", " ", text).strip(" .?!")
    original = re.sub(rf"^(hey |ok )?{ASSISTANT_NAME},? ", "", original, flags=re.I)
    query = original.lower()
    for name, pattern in RULES:
        m = pattern.search(query)
        if m:
            group = next((k for k, v in m.groupdict().items() if v), None)
            arg = original[m.start(group):m.end(group)].strip() if group else ""
            if name in ("open_site",):
                arg = arg.lower()
            return Intent(name, arg)
    return Intent("unknown", query)


def greeting(now: dt.datetime) -> str:
    part = "morning" if now.hour < 12 else "afternoon" if now.hour < 18 else "evening"
    return f"Good {part}! I'm {ASSISTANT_NAME}. How can I help?"


@dataclass
class Services:
    now: Callable[[], dt.datetime] = dt.datetime.now
    wiki: Callable[[str], str] | None = None
    joke: Callable[[], str] | None = None
    weather: Callable[[str], str] | None = None
    sites: dict = field(default_factory=lambda: dict(SITES))


def respond(intent: Intent, s: Services) -> Response:
    n, arg = intent.name, intent.arg
    if n == "quit":
        return Response("Thanks for your time. Goodbye!", quit=True)
    if n == "greet":
        return Response(greeting(s.now()))
    if n == "time":
        now = s.now()
        return Response(f"The time is {now.hour % 12 or 12}:{now:%M %p}.")
    if n == "date":
        now = s.now()
        return Response(f"Today is {now:%A, %B} {now.day}.")
    if n == "open_site":
        url = s.sites.get(arg)
        if url:
            return Response(f"Opening {NAMES.get(arg, arg.title())}.", open_url=url)
        return Response(f"Searching for {arg}.", open_url=f"https://www.google.com/search?q={quote_plus(arg)}")
    if n == "wikipedia" and s.wiki:
        try:
            return Response(f"According to Wikipedia: {s.wiki(arg)}")
        except Exception:
            return Response(f"I couldn't find {arg} on Wikipedia.")
    if n == "joke" and s.joke:
        return Response(s.joke())
    if n == "weather" and s.weather:
        try:
            return Response(s.weather(arg))
        except Exception:
            return Response("I couldn't get the weather right now.")
    if n == "locate":
        return Response(f"Here is {arg} on the map.", open_url=f"https://www.google.com/maps/search/{quote_plus(arg)}")
    if n == "music":
        return Response(f"Playing {arg} on YouTube Music.", open_url=f"https://music.youtube.com/search?q={quote_plus(arg)}")
    if n == "search":
        return Response(f"Here are results for {arg}.", open_url=f"https://www.google.com/search?q={quote_plus(arg)}")
    return Response("Sorry, I didn't catch that. Try 'what's the time', 'open YouTube' or 'where is Atlanta'.")
