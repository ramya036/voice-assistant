import datetime as dt

import pytest

from commands import Intent, Services, greeting, parse, respond

NOON = dt.datetime(2026, 11, 5, 12, 30)


def services(**kw):
    defaults = dict(now=lambda: NOON, wiki=lambda t: f"{t.title()} is a topic.",
                    joke=lambda: "Why do programmers prefer dark mode? Because light attracts bugs.",
                    weather=lambda place: f"Weather in {place or 'Atlanta'}: Sunny, +21°C")
    defaults.update(kw)
    return Services(**defaults)


@pytest.mark.parametrize("said, intent", [
    ("Open YouTube", Intent("open_site", "youtube")),
    ("lisa open github", Intent("open_site", "github")),
    ("What's the time?", Intent("time")),
    ("what is the date", Intent("date")),
    ("tell me a joke", Intent("joke")),
    ("search wikipedia for alan turing", Intent("wikipedia", "alan turing")),
    ("who is Ada Lovelace", Intent("wikipedia", "Ada Lovelace")),
    ("where is Georgia State University", Intent("locate", "Georgia State University")),
    ("what's the weather in Seattle", Intent("weather", "Seattle")),
    ("temperature", Intent("weather", "")),
    ("play lo-fi beats", Intent("music", "lo-fi beats")),
    ("search for best pizza near me", Intent("search", "best pizza near me")),
    ("ok bye", Intent("quit")),
    ("hello", Intent("greet")),
    ("blah blah", Intent("unknown", "blah blah")),
])
def test_parse(said, intent):
    assert parse(said) == intent


def test_where_is_wins_over_what_is():
    assert parse("where is the eiffel tower").name == "locate"


def test_open_known_and_unknown_sites():
    assert respond(Intent("open_site", "youtube"), services()).open_url == "https://www.youtube.com"
    assert respond(Intent("open_site", "netflix"), services()).open_url == "https://www.google.com/search?q=netflix"


def test_time_and_date_use_the_clock():
    assert respond(Intent("time"), services()).say == "The time is 12:30 PM."
    assert respond(Intent("date"), services()).say == "Today is Thursday, November 5."


@pytest.mark.parametrize("hour, word", [(8, "morning"), (14, "afternoon"), (21, "evening")])
def test_greeting_by_time_of_day(hour, word):
    assert word in greeting(dt.datetime(2026, 1, 1, hour))


def test_wikipedia_and_failure():
    assert "Alan Turing is a topic." in respond(Intent("wikipedia", "alan turing"), services()).say
    def boom(_):
        raise LookupError
    assert "couldn't find" in respond(Intent("wikipedia", "zzz"), services(wiki=boom)).say


def test_weather_and_failure():
    assert respond(Intent("weather", "Seattle"), services()).say == "Weather in Seattle: Sunny, +21°C"
    def boom(_):
        raise TimeoutError
    assert "couldn't get the weather" in respond(Intent("weather"), services(weather=boom)).say


def test_locate_and_music_build_safe_urls():
    assert respond(Intent("locate", "new york"), services()).open_url == "https://www.google.com/maps/search/new+york"
    assert respond(Intent("music", "a&b"), services()).open_url == "https://music.youtube.com/search?q=a%26b"


def test_quit_and_unknown():
    assert respond(Intent("quit"), services()).quit is True
    assert "didn't catch that" in respond(Intent("unknown", "x"), services()).say
