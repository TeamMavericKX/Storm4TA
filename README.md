# ⚡ Storm — Weather Intelligence Terminal
### A Mini Project by Tiger Analytics @Mini Project

Storm is a terminal-grade, real-time weather application that fetches atmospheric data from the OpenWeatherMap API and presents it in a modular, highly-performant Streamlit interface.

![Tiger Analytics](https://img.shields.io/badge/Tiger--Analytics-Mini--Project-orange)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-ff4b4b)

## 1. Project Overview
The API-Based Weather App is a real-time weather application that fetches weather data from an external API and presents it in a user-friendly Streamlit interface. The app allows users to search for weather details of any city and provides information such as temperature, humidity, weather conditions, and wind speed.

## 2. Use Case & Problem Statement
### Use Case:
- Many users require instant access to accurate weather information before making travel or work-related decisions.
- Traditional weather apps may be cluttered with ads, slow, or lack customization.

### Problem Statement:
How can we build a simple, responsive, and modular web application that fetches real-time weather data and presents it efficiently to users?

## 3. Solution Approach
- **Python Backend:** Core logic and data processing handled by Python.
- **Streamlit Frontend:** Lightweight and interactive UI for real-time visualization.
- **API Integration:** Fetches global weather data via the OpenWeatherMap API.
- **Best Practices:** Implementation of code modularization, PEP 8 compliance, and robust error handling.

## 4. Tech Stack
- **Language:** Python
- **Frontend:** Streamlit
- **Backend:** Python (Requests library)
- **API Provider:** OpenWeatherMap API
- **Version Control:** Git

## 5. Folder Structure
```bash
weather_app/
├── app.py             # Main Streamlit application
├── config.py          # Stores API key and config variables
├── requirements.txt   # Project dependencies
├── README.md          # Project Documentation
├── .gitignore         # Git ignore file
├── modules/
│   ├── __init__.py    # Module initialization
│   ├── api_handler.py # Handles API requests
│   ├── ui_components.py # UI elements (buttons, forms, etc.)
│   └── utils.py       # Helper functions (unit conversion, etc.)
└── assets/
    └── weather_icons/ # Icons for different weather conditions
```

## 6. Code Documentation & Best Practices
- **PEP 8 Compliance:** Code follows Python's official style guide.
- **Docstrings:** All functions and modules include descriptive docstrings.
- **Error Handling:** Graceful handling of API failures, timeouts, and invalid inputs.
- **Logging:** Implemented logging for monitoring API responses and debugging.
- **Security:** API keys are managed via environment variables/config files.

## 7. Installation & Setup
```bash
# 1. Clone & navigate
git clone <repo-url> && cd TA-WeatherApp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```
