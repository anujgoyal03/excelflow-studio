"""
theme.py
--------
All visual design tokens (colors) and the global CSS block live here.
Change a color once at the top of this file and it updates everywhere
(buttons, chips, pipeline, log, cards, sidebar) since every CSS rule
below reads from these same constants.

Call apply_theme() once, near the top of app.py, right after
st.set_page_config().
"""

import streamlit as st

# ============================================================
# DESIGN TOKENS
# ============================================================
# Palette: near-black green-charcoal base, Deloitte green as the single
# accent (used only for "active/in-flow" states), semantic colors kept
# strictly for success/error/warning — never decorative.

BG = "#0A0F0A"
SURFACE = "#131A12"
SURFACE_2 = "#1B231A"
SURFACE_3 = "#242E22"
BORDER = "#324333"
BORDER_SOFT = "#1E271D"
WHITE = "#F5FAF2"
TEXT = "#C9D4C5"
MUTED = "#8B9A88"
FAINT = "#5C6B5A"

ACCENT = "#86BC25"         # Deloitte green — primary accent
ACCENT_2 = "#43B02A"       # deeper Deloitte green — gradient partner
ACCENT_SOFT = "rgba(134,188,37,0.16)"
ACCENT_BORDER = "rgba(134,188,37,0.48)"
ACCENT_GRAD = "linear-gradient(135deg, #A6CE39 0%, #86BC25 55%, #43B02A 100%)"

SUCCESS = "#34E7A6"
SUCCESS_SOFT = "rgba(52,231,166,0.10)"
ERROR = "#FB6F84"
ERROR_SOFT = "rgba(251,111,132,0.10)"
WARNING = "#F0B23E"


def apply_theme():
    """Injects fonts + the full CSS stylesheet into the current page."""

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif;
            }}

            .stApp {{
                background: radial-gradient(120% 130% at 12% -12%, #16241A 0%, {BG} 48%),
                            radial-gradient(90% 90% at 100% 10%, rgba(134,188,37,0.06) 0%, transparent 60%);
            }}

            section[data-testid="stSidebar"] {{
                background-color: {SURFACE};
                border-right: 1px solid {BORDER_SOFT};
            }}

            section[data-testid="stSidebar"] > div {{
                padding-top: 1.4rem;
            }}

            h1, h2, h3, h4 {{
                font-family: 'Space Grotesk', sans-serif;
                color: {WHITE};
            }}

            p, span, label, div {{
                color: {TEXT};
            }}

            #MainMenu, footer {{visibility: hidden;}}

            /* ---------- Brand mark ---------- */
            .ef-brand {{
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 0 4px 20px 4px;
            }}
            .ef-deloitte {{
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700; font-size: 21px; color: {WHITE};
                letter-spacing: 0.2px; line-height: 1;
            }}
            .ef-deloitte .dot {{
                color: {ACCENT};
            }}
            .ef-brand-name {{
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 600; font-size: 12.5px; color: {MUTED};
                letter-spacing: 0.3px; line-height: 1.1; margin-top: 4px;
            }}
            .ef-brand-sub {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 9px; color: {FAINT}; letter-spacing: 1.2px;
                margin-top: 2px;
            }}

            /* ---------- Sidebar nav ---------- */
            .ef-nav-label {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px; color: {FAINT}; letter-spacing: 1.5px;
                margin: 4px 4px 8px 4px; font-weight: 600;
            }}

            section[data-testid="stSidebar"] .stButton > button {{
                background-color: transparent !important;
                color: {MUTED} !important;
                border: 1px solid transparent !important;
                border-radius: 9px !important;
                text-align: left !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
                font-size: 13.5px !important;
                padding: 10px 14px !important;
                box-shadow: none !important;
                transition: all .15s ease;
            }}
            section[data-testid="stSidebar"] .stButton > button:hover {{
                background-color: {SURFACE_2} !important;
                color: {TEXT} !important;
            }}
            section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
                background-color: {ACCENT_SOFT} !important;
                color: {ACCENT} !important;
                border: 1px solid {ACCENT_BORDER} !important;
            }}

            .ef-session-card {{
                background-color: {SURFACE_2};
                border: 1px solid {BORDER_SOFT};
                border-radius: 10px;
                padding: 12px 14px;
                margin-top: 6px;
            }}
            .ef-session-row {{
                display: flex; justify-content: space-between; align-items: center;
                font-family: 'JetBrains Mono', monospace; font-size: 11px;
                color: {MUTED}; padding: 3px 0;
            }}
            .ef-session-row b {{ color: {TEXT}; font-weight: 600; }}

            /* ---------- Header ---------- */
            .ef-eyebrow {{
                display: inline-flex; align-items: center; gap: 7px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10.5px; font-weight: 600; letter-spacing: 1.5px;
                color: {ACCENT_2}; background: {ACCENT_SOFT};
                border: 1px solid {ACCENT_BORDER};
                padding: 5px 11px; border-radius: 20px; margin-bottom: 14px;
            }}
            .ef-eyebrow .dot {{
                width: 6px; height: 6px; border-radius: 50%; background: {ACCENT_GRAD};
            }}
            .ef-h1 {{
                font-family: 'Space Grotesk', sans-serif;
                font-weight: 700; font-size: 30px; color: {WHITE};
                letter-spacing: 0.2px; margin: 0;
            }}
            .ef-desc {{
                color: {MUTED}; font-size: 14px; margin-top: 6px; max-width: 620px;
            }}

            /* ---------- Pipeline (signature element) ---------- */
            .ef-pipeline {{
                display: flex; align-items: center;
                background: {SURFACE};
                border: 1px solid {BORDER_SOFT};
                border-radius: 14px;
                padding: 22px 34px;
                margin: 22px 0 26px 0;
            }}
            .pipe-node {{
                display: flex; flex-direction: column; align-items: center; gap: 8px;
                min-width: 92px;
            }}
            .pipe-icon {{
                width: 46px; height: 46px; border-radius: 50%;
                display: flex; align-items: center; justify-content: center;
                font-size: 18px; border: 1.5px solid {BORDER};
                background: {SURFACE_2}; color: {FAINT};
                transition: all .35s ease;
            }}
            .pipe-node.active .pipe-icon {{
                border-color: {ACCENT_2}; color: {ACCENT_2};
                box-shadow: 0 0 0 5px {ACCENT_SOFT};
                animation: pipePulse 1.5s ease-in-out infinite;
            }}
            .pipe-node.done .pipe-icon {{
                border-color: {SUCCESS}; color: {SUCCESS};
                background: {SUCCESS_SOFT};
            }}
            @keyframes pipePulse {{
                0%, 100% {{ box-shadow: 0 0 0 5px {ACCENT_SOFT}; }}
                50% {{ box-shadow: 0 0 0 9px rgba(134,188,37,0.05); }}
            }}
            .pipe-label {{
                font-family: 'JetBrains Mono', monospace; font-size: 10px;
                letter-spacing: 1.3px; color: {FAINT}; font-weight: 600;
                transition: color .3s ease;
            }}
            .pipe-node.active .pipe-label, .pipe-node.done .pipe-label {{ color: {TEXT}; }}
            .pipe-line {{
                flex: 1; height: 2px; background: {BORDER}; margin: 0 4px;
                position: relative; top: -13px; transition: background .4s ease;
                border-radius: 2px;
            }}
            .pipe-line.filled {{ background: {ACCENT_GRAD}; }}

            /* ---------- Step-numbered cards ---------- */
            .ef-step-label {{
                display: flex; align-items: center; gap: 10px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10.5px; letter-spacing: 1.5px; font-weight: 600;
                color: {FAINT}; margin: 22px 0 10px 2px;
            }}
            .ef-step-num {{
                width: 20px; height: 20px; border-radius: 6px;
                background: {SURFACE_2}; border: 1px solid {BORDER};
                display: flex; align-items: center; justify-content: center;
                font-size: 10px; color: {MUTED};
            }}

            /* ---------- File cards ---------- */
            [data-testid="stFileUploaderDropzone"] {{
                background-color: {SURFACE} !important;
                border: 1.5px dashed {BORDER} !important;
                border-radius: 12px !important;
                transition: border-color .2s ease;
            }}
            [data-testid="stFileUploaderDropzone"]:hover {{
                border-color: {ACCENT_BORDER} !important;
            }}
            [data-testid="stFileUploader"] section {{
                background-color: transparent !important;
            }}
            [data-testid="stFileUploaderDropzone"] button {{
                background: {ACCENT_GRAD} !important;
                color: {WHITE} !important;
                font-weight: 700 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 9px 20px !important;
                box-shadow: 0 3px 12px rgba(134,188,37,0.3);
                transition: transform .12s ease, box-shadow .12s ease;
            }}
            [data-testid="stFileUploaderDropzone"] button:hover {{
                box-shadow: 0 5px 18px rgba(134,188,37,0.45);
                transform: translateY(-1px);
            }}
            [data-testid="stFileUploaderDropzone"] button p {{
                color: {WHITE} !important;
                font-weight: 700 !important;
            }}

            /* ---------- Sheet preview chips ---------- */
            .ef-chip-row {{ margin: 10px 0 4px 0; line-height: 2.3; }}
            .ef-chip {{
                display: inline-flex; align-items: center; gap: 6px;
                font-family: 'JetBrains Mono', monospace; font-size: 11px;
                padding: 4px 12px; border-radius: 20px; margin: 0 6px 6px 0;
                border: 1px solid {BORDER};
            }}
            .ef-chip.include {{
                color: {ACCENT_2}; border-color: {ACCENT_BORDER}; background: {ACCENT_SOFT};
            }}
            .ef-chip.exclude {{
                color: {FAINT}; background: transparent; text-decoration: line-through;
                opacity: .7;
            }}
            .ef-preview-caption {{
                font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
                color: {FAINT}; letter-spacing: .5px; margin-top: 8px;
            }}

            /* ---------- Buttons ---------- */
            .stButton > button {{
                background: {ACCENT_GRAD};
                color: {WHITE};
                font-weight: 700;
                font-family: 'Inter', sans-serif;
                border: none;
                border-radius: 9px;
                padding: 12px 26px;
                transition: transform .12s ease, box-shadow .12s ease;
                box-shadow: 0 0 0 0 rgba(134,188,37,0);
                text-shadow: 0 1px 2px rgba(0,0,0,0.25);
            }}
            .stButton > button:hover {{
                box-shadow: 0 6px 20px rgba(134,188,37,0.45);
                transform: translateY(-1px);
            }}
            .stButton > button p {{
                color: {WHITE} !important;
            }}
            .stDownloadButton > button {{
                background: linear-gradient(135deg, {SUCCESS} 0%, #22D3B0 100%);
                color: {WHITE};
                font-weight: 700;
                border: none;
                border-radius: 9px;
                padding: 13px 28px;
                transition: transform .12s ease, box-shadow .12s ease;
                text-shadow: 0 1px 2px rgba(0,0,0,0.25);
            }}
            .stDownloadButton > button:hover {{
                box-shadow: 0 6px 20px rgba(52,231,166,0.4);
                transform: translateY(-1px);
            }}
            .stDownloadButton > button p {{
                color: {WHITE} !important;
            }}

            /* ---------- Stat cards ---------- */
            .ef-stats-row {{ display: flex; gap: 12px; margin-top: 14px; }}
            .ef-stat {{
                flex: 1; background: {SURFACE};
                border: 1px solid {BORDER_SOFT}; border-radius: 12px;
                padding: 14px 16px;
            }}
            .ef-stat-label {{
                font-family: 'JetBrains Mono', monospace; font-size: 9.5px;
                letter-spacing: 1.3px; color: {FAINT}; font-weight: 600;
            }}
            .ef-stat-value {{
                font-family: 'Space Grotesk', sans-serif; font-weight: 700;
                font-size: 24px; margin-top: 4px;
            }}

            /* ---------- Activity log ---------- */
            .ef-log-card {{
                background: {SURFACE};
                border: 1px solid {BORDER_SOFT};
                border-radius: 12px;
                padding: 6px 16px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 12.5px;
                max-height: 360px;
                min-height: 360px;
                overflow-y: auto;
            }}
            .log-line {{ padding: 7px 0; border-bottom: 1px solid {BORDER_SOFT}; }}
            .log-line:last-child {{ border-bottom: none; }}
            .log-active {{ color: {ACCENT_2}; }}
            .log-ok {{ color: {SUCCESS}; }}
            .log-err {{ color: {ERROR}; }}
            .log-meta {{ color: {MUTED}; }}

            /* ---------- Result banner ---------- */
            .ef-result-card {{
                background: {SUCCESS_SOFT};
                border: 1px solid rgba(52,231,166,0.35);
                border-radius: 12px;
                padding: 16px 20px;
                margin-top: 6px;
            }}
            .ef-result-title {{
                color: {SUCCESS}; font-weight: 700; font-size: 14px;
                font-family: 'Space Grotesk', sans-serif;
            }}
            .ef-result-sub {{
                color: {TEXT}; font-size: 12.5px; margin-top: 4px;
                font-family: 'JetBrains Mono', monospace;
            }}

            .ef-footer {{
                color: {FAINT}; font-size: 11px; font-family: 'JetBrains Mono', monospace;
                letter-spacing: .5px; margin-top: 30px; text-align: center;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )