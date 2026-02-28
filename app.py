"""
╔═══════════════════════════════════════════════╗
║  > STORM.WX — Weather Intelligence Terminal   ║
║  Real-time atmospheric data. Terminal-grade.   ║
╚═══════════════════════════════════════════════╝
"""
import streamlit as st
from config import POPULAR_CITIES
from modules.api_handler import fetch_current_weather, fetch_forecast
from modules.ui_components import (
    _html, inject_custom_css,
    render_header, render_welcome, render_current_weather,
    render_weather_tip, render_metric_cards, render_sun_card,
    render_forecast, render_error, render_footer,
)

# ── Page Config ──
st.set_page_config(
    page_title="Storm · Weather Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS ──
inject_custom_css()

# ── Header ──
render_header()

# ── Divider line ──
_html('<div style="height:1px;background:rgba(255,255,255,0.05);margin-bottom:1.2rem;"></div>')

# ── Search Bar ──
col_input, col_btn = st.columns([5, 1])
with col_input:
    city_input = st.text_input(
        "Search",
        placeholder="> query city name...",
        label_visibility="collapsed",
    )
with col_btn:
    search_clicked = st.button("[ QUERY ]", use_container_width=True)

# ── Quick City Chips ──
chip_cols = st.columns(len(POPULAR_CITIES))
chip_city = None
for i, c in enumerate(POPULAR_CITIES):
    with chip_cols[i]:
        if st.button(c, key=f"chip_{c}", use_container_width=True):
            chip_city = c

city = chip_city or city_input.strip()

# ── Spacer ──
_html('<div style="height:0.5rem;"></div>')

# ── Main Content ──
if city:
    with st.spinner(""):
        weather = fetch_current_weather(city)

    if weather:
        render_current_weather(weather)
        render_weather_tip(weather["condition"])
        render_metric_cards(weather)
        render_sun_card(weather)

        with st.spinner(""):
            forecast = fetch_forecast(city)
        if forecast:
            render_forecast(forecast)
    else:
        render_error("City not found")
else:
    render_welcome()

# ── Footer ──
render_footer()
