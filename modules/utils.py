"""
Utility functions — conversions, formatting, mapping.
"""
from datetime import datetime, timezone, timedelta
from config import WEATHER_EMOJIS, WEATHER_TIPS


def celsius_to_fahrenheit(c: float) -> float:
    return round((c * 9 / 5) + 32, 1)


def get_wind_direction(deg: int) -> str:
    dirs = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
            "S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return dirs[round(deg / 22.5) % 16]


def format_unix_time(ts: int, tz_offset: int) -> str:
    tz = timezone(timedelta(seconds=tz_offset))
    return datetime.fromtimestamp(ts, tz=tz).strftime("%I:%M %p")


def get_local_datetime(tz_offset: int) -> datetime:
    return datetime.now(tz=timezone(timedelta(seconds=tz_offset)))


def get_weather_emoji(condition: str) -> str:
    return WEATHER_EMOJIS.get(condition, "🌤️")


def get_weather_tip(condition: str) -> str:
    return WEATHER_TIPS.get(condition, "sys.status: conditions nominal — carry on")


def country_code_to_flag(code: str) -> str:
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code.upper())


def get_feels_description(t: float) -> str:
    if t >= 40: return "CRITICAL_HOT"
    if t >= 35: return "EXTREME_WARM"
    if t >= 30: return "WARM"
    if t >= 25: return "COMFORTABLE"
    if t >= 20: return "PLEASANT"
    if t >= 15: return "COOL"
    if t >= 10: return "CHILLY"
    if t >= 0:  return "COLD"
    return "FREEZING"


def get_humidity_level(h: int) -> str:
    if h >= 80: return "SATURATED"
    if h >= 60: return "HUMID"
    if h >= 40: return "COMFORTABLE"
    if h >= 20: return "DRY"
    return "ARID"


def get_wind_severity(speed: float) -> str:
    if speed >= 90:  return "HURRICANE"
    if speed >= 62:  return "STORM"
    if speed >= 40:  return "STRONG"
    if speed >= 20:  return "MODERATE"
    if speed >= 10:  return "LIGHT"
    return "CALM"
