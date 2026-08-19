"""
app.py
------
ExcelFlow Enterprise Studio — Web Edition
Main entry point. Run with:

    streamlit run app.py

This file only handles PAGE LAYOUT and FLOW — the actual Excel logic
lives in engine.py, the colors/CSS live in theme.py, the workspace
config lives in modes.py, and the small HTML snippets live in
components.py. Keeping this file focused on "what happens on screen,
in what order" is what makes it readable.
"""

from datetime import datetime

import streamlit as st

from engine import ProcessingError, list_source_sheets, process_workbook, select_sheets
from modes import DEFAULT_MODE, MODES
from theme import ERROR, SUCCESS, apply_theme
from components import (
    build_chip_row_html,
    build_log_html,
    build_pipeline_html,
    build_preview_caption_html,
    build_result_card_html,
    build_stats_html,
)

# ============================================================
# PAGE CONFIG + THEME
# ============================================================

st.set_page_config(
    page_title="ExcelFlow Enterprise Studio",
    page_icon="\U0001F5C2",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

# ============================================================
# SESSION STATE
# ============================================================

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = DEFAULT_MODE
if "result" not in st.session_state:
    st.session_state.result = None
if "run_count" not in st.session_state:
    st.session_state.run_count = 0
if "last_mode_run" not in st.session_state:
    st.session_state.last_mode_run = "\u2014"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="ef-brand">
            <div>
                <div class="ef-deloitte">Deloitte<span class="dot">.</span></div>
                <div class="ef-brand-name">ExcelFlow</div>
                <div class="ef-brand-sub">ENTERPRISE STUDIO</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="ef-nav-label">WORKSPACES</div>', unsafe_allow_html=True)

    for name, mode_cfg in MODES.items():
        is_active = st.session_state.selected_mode == name
        label = f"{mode_cfg['icon']}   {name}"
        if st.button(label, key=f"nav_{name}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.selected_mode = name
            st.session_state.result = None
            st.rerun()

    st.markdown(
        f"""
        <div class="ef-session-card">
            <div class="ef-session-row"><span>RUNS THIS SESSION</span><b>{st.session_state.run_count}</b></div>
            <div class="ef-session-row"><span>LAST WORKSPACE</span><b>{st.session_state.last_mode_run}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ef-footer" style="text-align:left; margin-top:18px;">'
        'ExcelFlow \u00b7 Enterprise<br/>Excel Automation</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# MAIN — HEADER
# ============================================================

cfg = MODES[st.session_state.selected_mode]

st.markdown(
    f'<div class="ef-eyebrow"><span class="dot"></span>{st.session_state.selected_mode}</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="ef-h1">{cfg["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ef-desc">{cfg["description"]}</div>', unsafe_allow_html=True)

# ============================================================
# PIPELINE (signature element)
# ============================================================

pipeline_placeholder = st.empty()


def render_pipeline(stage="idle"):
    pipeline_placeholder.markdown(build_pipeline_html(stage), unsafe_allow_html=True)


render_pipeline("idle")

# ============================================================
# MAIN — WORKFLOW
# ============================================================

left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown(
        '<div class="ef-step-label"><span class="ef-step-num">1</span> SOURCE WORKBOOK</div>',
        unsafe_allow_html=True,
    )
    source_file = st.file_uploader(
        "Source Excel — the generated workbook to pull data from",
        type=["xlsx"],
        key=f"source_{st.session_state.selected_mode}",
        label_visibility="collapsed",
    )

    # Live sheet preview once a source file is present
    if source_file is not None:
        sheet_names = list_source_sheets(source_file.getvalue())
        if sheet_names is None:
            st.markdown(
                build_preview_caption_html(
                    "Could not read sheet names \u2014 the file may not be a valid .xlsx.",
                    color=ERROR,
                ),
                unsafe_allow_html=True,
            )
        else:
            included = select_sheets(cfg["mode"], sheet_names)
            excluded = [s for s in sheet_names if s not in included]
            st.markdown(build_chip_row_html(included, excluded), unsafe_allow_html=True)
            st.markdown(
                build_preview_caption_html(
                    f"{len(included)} OF {len(sheet_names)} SHEET(S) WILL BE PROCESSED IN THIS WORKSPACE"
                ),
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="ef-step-label"><span class="ef-step-num">2</span> TEMPLATE WORKBOOK</div>',
        unsafe_allow_html=True,
    )
    target_file = st.file_uploader(
        "Template Excel — the workbook to be updated",
        type=["xlsx"],
        key=f"target_{st.session_state.selected_mode}",
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="ef-step-label"><span class="ef-step-num">3</span> RUN</div>',
        unsafe_allow_html=True,
    )
    process_clicked = st.button("\u26a1  START PROCESSING", type="primary")

    status_placeholder = st.empty()
    status_placeholder.markdown(
        build_preview_caption_html("READY \u2022 SELECT YOUR FILES TO BEGIN"),
        unsafe_allow_html=True,
    )

    progress_bar = st.progress(0)

    stats_placeholder = st.empty()

    def render_stats(processed, total):
        stats_placeholder.markdown(build_stats_html(processed, total), unsafe_allow_html=True)

    render_stats(0, 0)

with right:
    st.markdown(
        '<div class="ef-step-label" style="margin-top:0;"><span class="ef-step-num">\u25CF</span> LIVE ACTIVITY</div>',
        unsafe_allow_html=True,
    )
    activity_placeholder = st.empty()

    def render_log(lines):
        activity_placeholder.markdown(build_log_html(lines), unsafe_allow_html=True)

    render_log([])

# ============================================================
# PROCESSING
# ============================================================

if process_clicked:
    log_lines = []

    if source_file is None:
        st.error("Please select the Source Excel file.")
    elif target_file is None:
        st.error("Please select the Template Excel file.")
    elif source_file.name == target_file.name and source_file.size == target_file.size:
        st.error("Source and Template files should not be the same file.")
    else:
        try:
            source_bytes = source_file.getvalue()
            target_bytes = target_file.getvalue()

            render_pipeline("reading")
            status_placeholder.markdown(
                build_preview_caption_html("LOADING EXCEL WORKBOOKS\u2026"),
                unsafe_allow_html=True,
            )
            log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] Opening source workbook...")
            render_log(log_lines)

            render_pipeline("processing")

            def on_progress(index, total, sheet_name):
                if log_lines and log_lines[-1].startswith("\u2192 Processing"):
                    log_lines[-1] = log_lines[-1].replace("\u2192 Processing", "\u2713 Processed", 1)

                progress_bar.progress(int((index / total) * 100))
                render_stats(index, total)
                status_placeholder.markdown(
                    build_preview_caption_html(f"PROCESSING \u2022 {sheet_name}"),
                    unsafe_allow_html=True,
                )
                log_lines.append(f"\u2192 Processing {sheet_name}")
                render_log(log_lines)

            output_bytes, processed_sheets, engine_log = process_workbook(
                source_bytes, target_bytes, cfg["mode"], progress_callback=on_progress
            )

            if log_lines and log_lines[-1].startswith("\u2192 Processing"):
                log_lines[-1] = log_lines[-1].replace("\u2192 Processing", "\u2713 Processed", 1)

            render_pipeline("writing")
            status_placeholder.markdown(
                build_preview_caption_html("SAVING UPDATED TEMPLATE\u2026"),
                unsafe_allow_html=True,
            )
            render_log(log_lines)

            progress_bar.progress(100)
            render_stats(len(processed_sheets), len(processed_sheets))

            render_pipeline("done")
            status_placeholder.markdown(
                build_preview_caption_html("COMPLETED SUCCESSFULLY \u2713", color=SUCCESS),
                unsafe_allow_html=True,
            )

            log_lines.append(f"[{datetime.now().strftime('%H:%M:%S')}] All sheets processed successfully.")
            render_log(log_lines)

            st.session_state.result = {
                "bytes": output_bytes,
                "filename": target_file.name,
                "sheets": processed_sheets,
            }
            st.session_state.run_count += 1
            st.session_state.last_mode_run = st.session_state.selected_mode

        except ProcessingError as e:
            render_pipeline("idle")
            status_placeholder.markdown(
                build_preview_caption_html("PROCESSING FAILED", color=ERROR),
                unsafe_allow_html=True,
            )
            log_lines.append(f"\u2715 {e}")
            render_log(log_lines)
            st.error(str(e))

        except Exception as e:
            render_pipeline("idle")
            status_placeholder.markdown(
                build_preview_caption_html("PROCESSING FAILED", color=ERROR),
                unsafe_allow_html=True,
            )
            log_lines.append(f"\u2715 Unexpected error: {e}")
            render_log(log_lines)
            st.error(f"Unexpected error: {e}")

# ============================================================
# RESULT / DOWNLOAD
# ============================================================

if st.session_state.result:
    result = st.session_state.result
    st.markdown(
        build_result_card_html(result["filename"], result["sheets"]),
        unsafe_allow_html=True,
    )
    st.write("")
    st.download_button(
        label="\u2b07  DOWNLOAD UPDATED TEMPLATE",
        data=result["bytes"],
        file_name=result["filename"],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.markdown('<div class="ef-footer">EXCELFLOW ENTERPRISE STUDIO</div>', unsafe_allow_html=True)