"""
API Handler — OpenWeatherMap requests.
"""
import logging
from datetime import datetime
from typing import Optional
import requests
from config import API_KEY, BASE_URL, FORECAST_URL, UNITS

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
_TIMEOUT = 10


def fetch_current_weather(city: str) -> Optional[dict]:
    """Fetch current weather for a city."""
    try:
        params = {"q": city, "appid": API_KEY, "units": UNITS}
        resp = requests.get(BASE_URL, params=params, timeout=_TIMEOUT)
        if resp.status_code == 404:
            logger.warning("City not found: %s", city)
            return None
        if resp.status_code == 401:
            logger.error("Invalid API key")
            return None
        resp.raise_for_status()
        d = resp.json()
        logger.info("Fetched: %s (%s)", d["name"], d["sys"]["country"])
        return {
            "city": d["name"],
            "country": d["sys"]["country"],
            "temp": round(d["main"]["temp"]),
            "feels_like": round(d["main"]["feels_like"]),
            "temp_min": round(d["main"]["temp_min"]),
            "temp_max": round(d["main"]["temp_max"]),
            "humidity": d["main"]["humidity"],
            "pressure": d["main"]["pressure"],
            "wind_speed": round(d["wind"]["speed"] * 3.6, 1),
            "wind_deg": d["wind"].get("deg", 0),
            "visibility": round(d.get("visibility", 0) / 1000, 1),
            "clouds": d["clouds"]["all"],
            "condition": d["weather"][0]["main"],
            "description": d["weather"][0]["description"].title(),
            "icon_code": d["weather"][0]["icon"],
            "sunrise": d["sys"]["sunrise"],
            "sunset": d["sys"]["sunset"],
            "timezone": d["timezone"],
            "dt": d["dt"],
        }
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
    except Exception as exc:
        logger.error("Error: %s", exc)
    return None


def fetch_forecast(city: str) -> Optional[list]:
    """Fetch 5-day forecast aggregated by day."""
    try:
        params = {"q": city, "appid": API_KEY, "units": UNITS}
        resp = requests.get(FORECAST_URL, params=params, timeout=_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        daily: dict = {}
        for item in data["list"]:
            dk = datetime.utcfromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            b = daily.setdefault(dk, {
                "temps": [], "conditions": [], "descriptions": [],
                "humidity": [], "wind": [],
            })
            b["temps"].append(item["main"]["temp"])
            b["conditions"].append(item["weather"][0]["main"])
            b["descriptions"].append(item["weather"][0]["description"])
            b["humidity"].append(item["main"]["humidity"])
            b["wind"].append(item["wind"]["speed"])
        forecast = []
        for ds, v in list(daily.items())[:5]:
            do = datetime.strptime(ds, "%Y-%m-%d")
            cond = max(set(v["conditions"]), key=v["conditions"].count)
            desc = max(set(v["descriptions"]), key=v["descriptions"].count)
            forecast.append({
                "date": do,
                "day_name": do.strftime("%a").upper(),
                "date_formatted": do.strftime("%b %d"),
                "temp_max": round(max(v["temps"])),
                "temp_min": round(min(v["temps"])),
                "condition": cond,
                "description": desc.title(),
                "humidity": round(sum(v["humidity"]) / len(v["humidity"])),
                "wind": round(sum(v["wind"]) / len(v["wind"]) * 3.6, 1),
            })
        return forecast
    except Exception as exc:
        logger.error("Forecast error: %s", exc)
        return None
