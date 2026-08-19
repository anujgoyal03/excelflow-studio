"""
components.py
--------------
Small, reusable functions that build an HTML snippet for one piece of the
UI (the pipeline indicator, the activity log, the stat cards, the sheet
preview chips, the result banner). Each function just returns a string —
app.py is the only place that actually calls st.markdown(...) to render
it. That keeps these easy to read/tweak/test in isolation.
"""

from html import escape as esc

from theme import ACCENT, ACCENT_2, ERROR, SUCCESS

# ============================================================
# PIPELINE (Source -> Engine -> Template signature widget)
# ============================================================

_PIPELINE_STATES = {
    "idle":       ("", "", "", "", ""),
    "reading":    ("active", "", "", "", ""),
    "processing": ("done", "filled", "active", "", ""),
    "writing":    ("done", "filled", "done", "filled", "active"),
    "done":       ("done", "filled", "done", "filled", "done"),
}


def build_pipeline_html(stage="idle"):
    """stage: idle | reading | processing | writing | done"""

    src_s, line1_s, eng_s, line2_s, tgt_s = _PIPELINE_STATES.get(stage, _PIPELINE_STATES["idle"])

    return f"""
    <div class="ef-pipeline">
        <div class="pipe-node {src_s}">
            <div class="pipe-icon">\u2b06</div>
            <div class="pipe-label">SOURCE</div>
        </div>
        <div class="pipe-line {line1_s}"></div>
        <div class="pipe-node {eng_s}">
            <div class="pipe-icon">\u2699</div>
            <div class="pipe-label">ENGINE</div>
        </div>
        <div class="pipe-line {line2_s}"></div>
        <div class="pipe-node {tgt_s}">
            <div class="pipe-icon">\u2b07</div>
            <div class="pipe-label">TEMPLATE</div>
        </div>
    </div>
    """


# ============================================================
# ACTIVITY LOG
# ============================================================

def build_log_html(lines):
    """Renders the list of log strings, color-coding by their prefix
    (-> in progress, checkmark done, x error, otherwise neutral)."""

    if not lines:
        return '<div class="ef-log-card"><div class="log-line log-meta">Ready. Waiting for files\u2026</div></div>'

    rows = []
    for line in lines:
        if line.startswith("\u2713"):
            cls = "log-ok"
        elif line.startswith("\u2715"):
            cls = "log-err"
        elif line.startswith("\u2192"):
            cls = "log-active"
        else:
            cls = "log-meta"
        rows.append(f'<div class="log-line {cls}">{esc(line)}</div>')

    return f'<div class="ef-log-card">{"".join(rows)}</div>'


# ============================================================
# STAT CARDS
# ============================================================

def build_stats_html(processed, total):
    return f"""
    <div class="ef-stats-row">
        <div class="ef-stat">
            <div class="ef-stat-label">PROCESSED</div>
            <div class="ef-stat-value" style="color:{SUCCESS};">{processed}</div>
        </div>
        <div class="ef-stat">
            <div class="ef-stat-label">TOTAL</div>
            <div class="ef-stat-value" style="color:{ACCENT_2};">{total}</div>
        </div>
    </div>
    """


# ============================================================
# SHEET PREVIEW CHIPS
# ============================================================

def build_chip_row_html(included, excluded):
    chips = "".join(f'<span class="ef-chip include">{esc(s)}</span>' for s in included)
    chips += "".join(f'<span class="ef-chip exclude">{esc(s)}</span>' for s in excluded)
    return f'<div class="ef-chip-row">{chips}</div>'


def build_preview_caption_html(text, color=None):
    style = f' style="color:{color};"' if color else ""
    return f'<div class="ef-preview-caption"{style}>{esc(text)}</div>'


# ============================================================
# RESULT / DOWNLOAD BANNER
# ============================================================

def build_result_card_html(filename, sheets):
    return f"""
    <div class="ef-result-card">
        <div class="ef-result-title">\u2713 Ready to download</div>
        <div class="ef-result-sub">{esc(filename)} \u2014 {len(sheets)} sheet(s) updated:
        {esc(', '.join(sheets))}</div>
    </div>
    """