"""
UI Components — Storm v2
Terminal-grade aesthetic. No gradients. Pure darkness + lime accent.
Matching the portfolio's design DNA exactly.
"""
import streamlit as st
from modules.utils import (
    country_code_to_flag, format_unix_time, get_local_datetime,
    get_weather_emoji, get_weather_tip, get_wind_direction,
    get_feels_description, get_humidity_level, get_wind_severity,
    celsius_to_fahrenheit,
)


def _html(content: str) -> None:
    """Render HTML, stripping blank lines to prevent Streamlit parser breakage."""
    cleaned = "\n".join(line for line in content.split("\n") if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


# ════════════════════════════════════════════
#  CSS INJECTION
# ════════════════════════════════════════════

def inject_custom_css() -> None:
    """Inject the full terminal-grade stylesheet."""
    css = """
    <style>
    /* ═══ FONTS ═══ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;700&display=swap');
    /* ═══ VARIABLES ═══ */
    :root {
        --accent: #bef264;
        --accent-rgb: 190,242,100;
        --accent-dim: rgba(190,242,100,0.15);
        --accent-glow: rgba(190,242,100,0.25);
        --bg: #050505;
        --bg-card: rgba(255,255,255,0.02);
        --bg-card-hover: rgba(255,255,255,0.05);
        --border: rgba(255,255,255,0.08);
        --border-hover: rgba(190,242,100,0.3);
        --text-primary: #fafafa;
        --text-secondary: #a3a3a3;
        --text-muted: #525252;
        --text-dim: #404040;
        --radius: 1rem;
        --font-sans: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
        --font-display: 'Space Grotesk', sans-serif;
        --ease-expo: cubic-bezier(0.16, 1, 0.3, 1);
    }
    /* ═══ BASE ═══ */
    .stApp {
        background-color: var(--bg) !important;
        font-family: var(--font-sans);
    }
    /* ═══ NOISE OVERLAY ═══ */
    .stApp::before {
        content: '';
        position: fixed; inset: 0;
        pointer-events: none; z-index: 9999;
        opacity: 0.035;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    }
    /* ═══ SCANLINES ═══ */
    .stApp::after {
        content: '';
        position: fixed; inset: 0;
        background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.08) 50%);
        background-size: 100% 4px;
        pointer-events: none; z-index: 9998;
        opacity: 0.25;
    }
    /* ═══ HIDE STREAMLIT CHROME ═══ */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden !important; height: 0 !important; }
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px !important;
    }
    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }
    ::selection { background: var(--accent); color: #000; }
    /* ═══ INPUT ═══ */
    .stTextInput > div > div > input {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0.5rem !important;
        color: var(--text-primary) !important;
        font-family: var(--font-mono) !important;
        font-size: 0.9rem !important;
        padding: 0.85rem 1.2rem !important;
        transition: all 0.3s ease !important;
        caret-color: var(--accent) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent), 0 0 20px rgba(var(--accent-rgb), 0.1) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: var(--text-dim) !important;
        font-family: var(--font-mono) !important;
    }
    .stTextInput label { display: none !important; }
    /* ═══ BUTTONS ═══ */
    .stButton > button {
        background: transparent !important;
        color: var(--accent) !important;
        border: 1px solid rgba(var(--accent-rgb), 0.3) !important;
        border-radius: 0.5rem !important;
        padding: 0.85rem 1.5rem !important;
        font-family: var(--font-mono) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase !important;
    }
    .stButton > button:hover {
        background: rgba(var(--accent-rgb), 0.1) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 20px rgba(var(--accent-rgb), 0.15) !important;
        transform: translateY(-2px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    /* ═══ CHIP BUTTONS (quick cities) ═══ */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        font-size: 0.7rem !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: 0.25rem !important;
        letter-spacing: 0.08em !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: var(--text-muted) !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        color: var(--accent) !important;
        border-color: var(--accent) !important;
        background: rgba(var(--accent-rgb), 0.05) !important;
        box-shadow: none !important;
    }
    /* ═══ SPINNER ═══ */
    .stSpinner > div { border-top-color: var(--accent) !important; }
    /* ═══ KEYFRAMES ═══ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    @keyframes scanline {
        0% { top: 0%; opacity: 0; }
        10% { opacity: 0.6; }
        90% { opacity: 0.6; }
        100% { top: 100%; opacity: 0; }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(var(--accent-rgb), 0.2); }
        50% { border-color: rgba(var(--accent-rgb), 0.5); }
    }
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    /* ═══ HEADER ═══ */
    .app-header {
        text-align: left;
        padding: 0 0 1.5rem;
        animation: fadeInDown 0.6s var(--ease-expo);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .app-logo {
        font-family: var(--font-mono);
        font-weight: 700;
        font-size: 1.2rem;
        color: var(--text-primary);
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .app-logo .caret {
        color: var(--accent);
        animation: blink 1s infinite;
    }
    .app-logo .dim { color: var(--text-muted); }
    .header-status {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .status-dot {
        width: 6px; height: 6px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulse 2s infinite;
        display: inline-block;
    }
    /* ═══ SECTION LABEL ═══ */
    .section-label {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 1rem;
        animation: slideInLeft 0.5s var(--ease-expo);
    }
    /* ═══ HERO CARD ═══ */
    .weather-hero {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 2.5rem;
        margin: 0.8rem 0;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s var(--ease-expo);
        transition: all 0.4s ease;
    }
    .weather-hero:hover {
        border-color: var(--border-hover);
        box-shadow: 0 20px 40px -20px rgba(var(--accent-rgb), 0.1);
    }
    .weather-hero::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(var(--accent-rgb), 0.3), transparent);
        transform: scaleX(0);
        transition: transform 0.6s var(--ease-expo);
    }
    .weather-hero:hover::before { transform: scaleX(1); }
    .weather-hero .scan {
        position: absolute; top: 0; left: 0; width: 100%; height: 2px;
        background: rgba(var(--accent-rgb), 0.4);
        box-shadow: 0 0 8px var(--accent);
        animation: scanline 4s linear infinite;
        pointer-events: none;
    }
    .hero-grid {
        display: flex; align-items: center; justify-content: space-between;
        flex-wrap: wrap; gap: 2rem; position: relative; z-index: 1;
    }
    .hero-left { flex: 1; min-width: 250px; }
    .hero-right { text-align: center; min-width: 160px; }
    .city-name {
        font-family: var(--font-display);
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.1;
        margin-bottom: 0.25rem;
    }
    .city-country {
        font-family: var(--font-mono);
        font-size: 0.75rem;
        color: var(--accent);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .city-country .dot {
        width: 6px; height: 6px;
        background: var(--accent);
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    .temp-display {
        font-family: var(--font-display);
        font-size: 5rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .temp-unit {
        font-size: 1.8rem;
        font-weight: 500;
        color: var(--text-muted);
    }
    .temp-range {
        display: flex;
        gap: 1.2rem;
        margin-top: 0.5rem;
        font-family: var(--font-mono);
        font-size: 0.8rem;
    }
    .temp-high { color: #f87171; font-weight: 500; }
    .temp-low { color: #67e8f9; font-weight: 500; }
    .weather-emoji {
        font-size: 5.5rem;
        line-height: 1;
        filter: drop-shadow(0 8px 20px rgba(0,0,0,0.4));
        display: block;
        margin-bottom: 0.5rem;
    }
    .weather-desc {
        font-family: var(--font-display);
        font-size: 1.1rem;
        font-weight: 500;
        color: var(--text-primary);
    }
    .weather-date {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--text-dim);
        margin-top: 0.3rem;
        letter-spacing: 0.05em;
    }
    /* ═══ METRICS GRID ═══ */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.75rem;
        margin: 0.8rem 0;
    }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem 1.2rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        animation: fadeInUp 0.5s var(--ease-expo) backwards;
    }
    .metric-card:nth-child(1) { animation-delay: 0.05s; }
    .metric-card:nth-child(2) { animation-delay: 0.10s; }
    .metric-card:nth-child(3) { animation-delay: 0.15s; }
    .metric-card:nth-child(4) { animation-delay: 0.20s; }
    .metric-card:nth-child(5) { animation-delay: 0.25s; }
    .metric-card:nth-child(6) { animation-delay: 0.30s; }
    .metric-card::after {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
        transform: scaleX(0);
        transition: transform 0.6s var(--ease-expo);
    }
    .metric-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-hover);
        transform: translateY(-4px);
        box-shadow: 0 15px 30px -15px rgba(var(--accent-rgb), 0.1);
    }
    .metric-card:hover::after { transform: scaleX(1); }
    .metric-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }
    .metric-label {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .metric-icon {
        font-size: 1rem;
        opacity: 0.6;
    }
    .metric-value {
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .metric-sub {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-bar {
        margin-top: 0.8rem;
        height: 3px;
        background: rgba(255,255,255,0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .metric-bar-fill {
        height: 100%;
        background: var(--accent);
        border-radius: 2px;
        transition: width 1s var(--ease-expo);
        box-shadow: 0 0 8px rgba(var(--accent-rgb), 0.4);
    }
    /* ═══ SUN CARD ═══ */
    .sun-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 2rem;
        margin: 0.8rem 0;
        transition: all 0.4s ease;
        animation: fadeInUp 0.6s var(--ease-expo) 0.2s backwards;
    }
    .sun-card:hover {
        border-color: var(--border-hover);
    }
    .sun-timeline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        padding: 1.5rem 0 0.5rem;
    }
    .sun-timeline::before {
        content: '';
        position: absolute;
        left: 15%; right: 15%; top: calc(50% + 0.5rem);
        height: 2px;
        background: linear-gradient(90deg, var(--accent), rgba(var(--accent-rgb), 0.3), var(--accent));
        border-radius: 1px;
    }
    .sun-point {
        text-align: center;
        position: relative; z-index: 1;
    }
    .sun-icon {
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    .sun-time {
        font-family: var(--font-display);
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    .sun-tag {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }
    /* ═══ TIP CARD ═══ */
    .tip-card {
        background: rgba(var(--accent-rgb), 0.03);
        border: 1px solid rgba(var(--accent-rgb), 0.12);
        border-radius: var(--radius);
        padding: 1rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 0.8rem 0;
        font-family: var(--font-mono);
        animation: fadeInUp 0.5s var(--ease-expo) 0.1s backwards;
    }
    .tip-prefix {
        color: var(--accent);
        font-size: 0.75rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .tip-text {
        color: var(--text-secondary);
        font-size: 0.8rem;
        line-height: 1.5;
    }
    /* ═══ FORECAST ═══ */
    .forecast-section {
        margin-top: 1rem;
        animation: fadeInUp 0.6s var(--ease-expo) 0.3s backwards;
    }
    .forecast-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 0.75rem;
    }
    .forecast-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem 1rem;
        text-align: center;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.5s var(--ease-expo) backwards;
    }
    .forecast-card:nth-child(1) { animation-delay: 0.05s; }
    .forecast-card:nth-child(2) { animation-delay: 0.10s; }
    .forecast-card:nth-child(3) { animation-delay: 0.15s; }
    .forecast-card:nth-child(4) { animation-delay: 0.20s; }
    .forecast-card:nth-child(5) { animation-delay: 0.25s; }
    .forecast-card:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-hover);
        transform: translateY(-4px);
        box-shadow: 0 15px 30px -15px rgba(var(--accent-rgb), 0.1);
    }
    .forecast-day {
        font-family: var(--font-mono);
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 0.15rem;
    }
    .forecast-date {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        color: var(--text-dim);
        margin-bottom: 0.8rem;
        letter-spacing: 0.05em;
    }
    .forecast-emoji {
        font-size: 2rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    .forecast-temps {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        font-family: var(--font-display);
        font-size: 1rem;
    }
    .forecast-hi { color: #f87171; font-weight: 700; }
    .forecast-lo { color: #67e8f9; font-weight: 500; }
    .forecast-cond {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* ═══ WELCOME ═══ */
    .welcome-container {
        text-align: center;
        padding: 5rem 2rem;
        animation: fadeInUp 0.8s var(--ease-expo);
    }
    .welcome-icon {
        font-size: 3rem;
        margin-bottom: 2rem;
        display: block;
        animation: pulse 2s infinite;
    }
    .welcome-title {
        font-family: var(--font-display);
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    .welcome-text {
        color: var(--text-muted);
        font-size: 0.95rem;
        max-width: 440px;
        margin: 0 auto;
        line-height: 1.7;
    }
    .welcome-hint {
        font-family: var(--font-mono);
        font-size: 0.7rem;
        color: var(--text-dim);
        margin-top: 2rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .welcome-hint .accent { color: var(--accent); }
    /* ═══ ERROR ═══ */
    .error-card {
        background: rgba(239,68,68,0.05);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: var(--radius);
        padding: 3rem;
        text-align: center;
        animation: fadeInUp 0.5s var(--ease-expo);
    }
    .error-icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .error-title {
        font-family: var(--font-display);
        font-size: 1.2rem;
        font-weight: 700;
        color: #f87171;
        margin-bottom: 0.5rem;
    }
    .error-msg {
        font-family: var(--font-mono);
        color: var(--text-muted);
        font-size: 0.8rem;
    }
    /* ═══ FOOTER ═══ */
    .app-footer {
        text-align: center;
        padding: 2rem 0 0.5rem;
        margin-top: 2rem;
        border-top: 1px solid var(--border);
        font-family: var(--font-mono);
        font-size: 0.6rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .app-footer .accent { color: var(--accent); }
    .footer-status {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 0.5rem;
        color: var(--text-dim);
    }
    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 640px) {
        .hero-grid { flex-direction: column; text-align: center; }
        .hero-left { text-align: center; }
        .city-country { justify-content: center; }
        .temp-display { font-size: 4rem; }
        .temp-range { justify-content: center; }
        .weather-emoji { font-size: 4rem; }
        .city-name { font-size: 1.6rem; }
    }
    </style>
    """
    _html(css)


# ════════════════════════════════════════════
#  RENDER FUNCTIONS
# ════════════════════════════════════════════

def render_header() -> None:
    _html(
        '<div class="app-header">'
        '<div class="app-logo">'
        '<span class="caret">&gt;</span>STORM'
        '<span class="dim">.WX</span>'
        '</div>'
        '<div class="header-status">'
        '<span class="status-dot"></span>'
        '<span>SYS.ONLINE</span>'
        '<span style="color:#404040;">|</span>'
        '<span>ENCRYPTION: ACTIVE</span>'
        '</div>'
        '</div>'
    )


def render_welcome() -> None:
    _html(
        '<div class="welcome-container">'
        '<span class="welcome-icon">&#9729;&#65039;</span>'
        '<div class="welcome-title">Weather Intelligence Terminal</div>'
        '<p class="welcome-text">'
        'Enter a city name above to query real-time atmospheric data '
        'from the OpenWeatherMap network.'
        '</p>'
        '<div class="welcome-hint">'
        '[ <span class="accent">type a city</span> &mdash; press enter ]'
        '</div>'
        '</div>'
    )


def render_current_weather(data: dict) -> None:
    emoji = get_weather_emoji(data["condition"])
    flag = country_code_to_flag(data["country"])
    local_dt = get_local_datetime(data["timezone"])
    date_str = local_dt.strftime("%A, %b %d &middot; %I:%M %p")
    f_temp = celsius_to_fahrenheit(data["temp"])

    _html(
        '<div class="section-label">01 / Current Conditions</div>'
        '<div class="weather-hero">'
        '<div class="scan"></div>'
        '<div class="hero-grid">'
        # Left
        '<div class="hero-left">'
        f'<div class="city-name">{data["city"]}</div>'
        '<div class="city-country">'
        f'<span class="dot"></span>'
        f'{flag}&ensp;{data["country"]}'
        '</div>'
        f'<div class="temp-display">{data["temp"]}<span class="temp-unit">&deg;C</span></div>'
        '<div class="temp-range">'
        f'<span class="temp-high">&#9650; {data["temp_max"]}&deg;</span>'
        f'<span class="temp-low">&#9660; {data["temp_min"]}&deg;</span>'
        f'<span style="color:#525252;font-family:var(--font-mono);font-size:0.75rem;">'
        f'/ {f_temp}&deg;F</span>'
        '</div>'
        '</div>'
        # Right
        '<div class="hero-right">'
        f'<span class="weather-emoji">{emoji}</span>'
        f'<div class="weather-desc">{data["description"]}</div>'
        f'<div class="weather-date">{date_str}</div>'
        '</div>'
        '</div>'
        '</div>'
    )


def render_weather_tip(condition: str) -> None:
    tip = get_weather_tip(condition)
    _html(
        '<div class="tip-card">'
        '<div class="tip-prefix">&gt;_</div>'
        f'<div class="tip-text">{tip}</div>'
        '</div>'
    )


def render_metric_cards(data: dict) -> None:
    wind_dir = get_wind_direction(data["wind_deg"])
    feels_desc = get_feels_description(data["feels_like"])
    hum_level = get_humidity_level(data["humidity"])
    wind_sev = get_wind_severity(data["wind_speed"])

    cards = [
        ("FEELS LIKE",  "&#x1F321;&#xFE0F;", f'{data["feels_like"]}&deg;',
         feels_desc, None),
        ("HUMIDITY",     "&#x1F4A7;",          f'{data["humidity"]}%',
         hum_level, data["humidity"]),
        ("WIND",         "&#x1F4A8;",          f'{data["wind_speed"]}',
         f"{wind_dir} &middot; {wind_sev}", min(data["wind_speed"] / 100 * 100, 100)),
        ("PRESSURE",     "&#x1F4CA;",          f'{data["pressure"]}',
         "HPA", None),
        ("VISIBILITY",   "&#x1F441;&#xFE0F;", f'{data["visibility"]}',
         "KM", min(data["visibility"] / 20 * 100, 100)),
        ("CLOUD COVER",  "&#9729;&#65039;",    f'{data["clouds"]}%',
         "COVERAGE", data["clouds"]),
    ]

    inner = ""
    for label, icon, value, sub, bar_pct in cards:
        bar_html = ""
        if bar_pct is not None:
            bar_html = (
                '<div class="metric-bar">'
                f'<div class="metric-bar-fill" style="width:{bar_pct}%"></div>'
                '</div>'
            )
        inner += (
            '<div class="metric-card">'
            '<div class="metric-header">'
            f'<span class="metric-label">{label}</span>'
            f'<span class="metric-icon">{icon}</span>'
            '</div>'
            f'<div class="metric-value">{value}</div>'
            f'<div class="metric-sub">{sub}</div>'
            f'{bar_html}'
            '</div>'
        )

    _html(
        '<div class="section-label">02 / Atmospheric Data</div>'
        f'<div class="metrics-grid">{inner}</div>'
    )


def render_sun_card(data: dict) -> None:
    sunrise = format_unix_time(data["sunrise"], data["timezone"])
    sunset = format_unix_time(data["sunset"], data["timezone"])

    _html(
        '<div class="section-label">03 / Solar Cycle</div>'
        '<div class="sun-card">'
        '<div class="sun-timeline">'
        '<div class="sun-point">'
        '<span class="sun-icon">&#127749;</span>'
        f'<div class="sun-time">{sunrise}</div>'
        '<div class="sun-tag">Sunrise</div>'
        '</div>'
        '<div class="sun-point">'
        '<span class="sun-icon">&#9728;&#65039;</span>'
        '<div class="sun-time">12:00 PM</div>'
        '<div class="sun-tag">Solar Peak</div>'
        '</div>'
        '<div class="sun-point">'
        '<span class="sun-icon">&#127751;</span>'
        f'<div class="sun-time">{sunset}</div>'
        '<div class="sun-tag">Sunset</div>'
        '</div>'
        '</div>'
        '</div>'
    )


def render_forecast(forecast: list) -> None:
    inner = ""
    for day in forecast:
        emoji = get_weather_emoji(day["condition"])
        inner += (
            '<div class="forecast-card">'
            f'<div class="forecast-day">{day["day_name"]}</div>'
            f'<div class="forecast-date">{day["date_formatted"]}</div>'
            f'<span class="forecast-emoji">{emoji}</span>'
            '<div class="forecast-temps">'
            f'<span class="forecast-hi">{day["temp_max"]}&deg;</span>'
            f'<span class="forecast-lo">{day["temp_min"]}&deg;</span>'
            '</div>'
            f'<div class="forecast-cond">{day["description"]}</div>'
            '</div>'
        )

    _html(
        '<div class="forecast-section">'
        '<div class="section-label">04 / 5-Day Forecast</div>'
        f'<div class="forecast-grid">{inner}</div>'
        '</div>'
    )


def render_error(message: str = "City not found") -> None:
    _html(
        '<div class="error-card">'
        '<div class="error-icon">&#128683;</div>'
        f'<div class="error-title">ERR: {message.upper()}</div>'
        '<div class="error-msg">'
        'query failed &mdash; verify city name and retry'
        '</div>'
        '</div>'
    )


def render_footer() -> None:
    _html(
        '<div class="app-footer">'
        '<div class="footer-status">'
        '<span>sys.status: normal</span>'
        '<span>&bull;</span>'
        '<span>encryption: enabled</span>'
        '<span>&bull;</span>'
        '<span>uptime: 99.9%</span>'
        '</div>'
        '&copy; 2025 <span class="accent">Storm</span>'
        ' &middot; powered by openweathermap'
        '</div>'
    )
