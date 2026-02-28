"""
Configuration — Storm Weather Terminal
"""
import os

API_KEY: str = os.environ.get("OPENWEATHER_API_KEY", "")
BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL: str = "https://api.openweathermap.org/data/2.5/forecast"
UNITS: str = "metric"

WEATHER_EMOJIS: dict = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️",
    "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Snow": "❄️",
    "Mist": "🌫️", "Haze": "🌫️", "Fog": "🌫️",
    "Smoke": "💨", "Dust": "💨", "Tornado": "🌪️",
}

WEATHER_TIPS: dict = {
    "Clear": "sys.advisory: UV index high — deploy sunscreen protocol",
    "Clouds": "sys.advisory: overcast conditions — optimal for indoor ops",
    "Rain": "sys.advisory: precipitation active — waterproof gear required",
    "Drizzle": "sys.advisory: light moisture detected — windbreaker sufficient",
    "Thunderstorm": "sys.warning: electrical storm — shelter in place",
    "Snow": "sys.advisory: frozen precipitation — traction control advised",
    "Mist": "sys.advisory: low visibility — reduce transit speed",
    "Haze": "sys.advisory: particulate matter elevated — filtration recommended",
    "Fog": "sys.advisory: dense fog — low-beam protocol active",
}

POPULAR_CITIES: list = [
    "Chennai", "Tokyo", "London", "New York",
    "Berlin", "Sydney", "Dubai", "Mumbai",
]
