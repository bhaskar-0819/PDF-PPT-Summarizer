import streamlit as st
import requests
import os
import json
from datetime import datetime
import streamlit.components.v1 as components
from fpdf import FPDF
from fpdf.enums import XPos, YPos
 

st.set_page_config(
    page_title="DocSummarize AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html { scroll-behavior: smooth; }
*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
}
.main .block-container, [data-testid="stAppViewContainer"] > section:last-child {
    scroll-behavior: smooth;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
}
.stApp {
    background: linear-gradient(135deg, #c8f0e8 0%, #b8d4f8 45%, #a0b8f5 100%) !important;
    min-height: 100vh;
    overflow-x: hidden;
}
#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebar"] > div:first-child > div > div > div > button {
    display: none !important;
    pointer-events: none !important;
}
.css-1rs6os, .css-17ziqus, .css-fblp2m, .css-1lcbmhc, .css-1outpf7, .css-qrbaxs {
    display: none !important;
}
[data-testid="stSidebar"] {
    transform: none !important;
    visibility: visible !important;
    left: 0 !important;
    transition: none !important;
}
section[data-testid="stSidebar"][aria-expanded="false"] {
    display: block !important;
    transform: none !important;
    margin-left: 0 !important;
    width: 260px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2e4a 0%, #0f4c75 60%, #1b6ca8 100%) !important;
    border-right: none !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }

.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 0.5rem;
}
.s-icon {
    width: 36px; height: 36px; border-radius: 10px;
    background: rgba(255,255,255,0.15);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.s-title { font-size: 1rem; font-weight: 700; color: white !important; line-height: 1.2; }
.s-sub   { font-size: 0.7rem; color: rgba(255,255,255,0.5) !important; }

.sidebar-section {
    padding: 0.6rem 1.2rem 0.3rem;
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: rgba(255,255,255,0.38) !important;
}

.stat-card {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 10px; padding: 0.75rem 1rem;
    margin: 0.3rem 1rem;
    display: flex; align-items: center; gap: 10px;
}
.sc-val { font-size: 1.3rem; font-weight: 700; color: white !important; line-height: 1; }
.sc-lbl { font-size: 0.72rem; color: rgba(255,255,255,0.55) !important; margin-top: 2px; }

.hist-item {
    display: flex; align-items: center; gap: 8px;
    padding: 0.55rem 1rem; border-radius: 8px;
    margin: 0.15rem 0.8rem;
}
.hist-item:hover { background: rgba(255,255,255,0.1); }
.hi-icon {
    width: 28px; height: 28px; border-radius: 6px;
    background: rgba(255,255,255,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; flex-shrink: 0;
}
.hi-name {
    font-size: 0.8rem; color: rgba(255,255,255,0.82) !important;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 160px;
}
.hi-time { font-size: 0.68rem; color: rgba(255,255,255,0.4) !important; margin-top: 1px; }
.hist-empty {
    text-align: center; padding: 0.8rem 1rem;
    font-size: 0.78rem; color: rgba(255,255,255,0.35) !important;
    line-height: 1.7;
}

.ch-item {
    padding: 0.5rem 1rem; border-radius: 8px;
    margin: 0.12rem 0.8rem;
    border-left: 2px solid transparent;
}
.ch-item:hover { background: rgba(255,255,255,0.08); }
.ch-item.pinned {
    border-left: 2px solid #fbbf24;
    background: rgba(251,191,36,0.08);
}
.ch-q {
    font-size: 0.78rem; color: rgba(255,255,255,0.85) !important;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 170px; font-weight: 500;
}
.ch-a {
    font-size: 0.7rem; color: rgba(255,255,255,0.4) !important;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 170px; margin-top: 1px;
}
.ch-meta { display: flex; align-items: center; gap: 5px; margin-top: 2px; }
.ch-time { font-size: 0.65rem; color: rgba(255,255,255,0.3) !important; }

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.12) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: white !important; border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: white !important; }

[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.1) !important;
    color: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 6px !important;
    font-size: 0.72rem !important;
    padding: 0.2rem 0.5rem !important;
    width: auto !important;
    margin-top: 0 !important;
    box-shadow: none !important;
    min-height: unset !important;
    height: 24px !important;
    line-height: 1 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.2) !important;
    transform: none !important;
    opacity: 1 !important;
}

.block-container { padding-top: 78px !important; padding-bottom: 3rem; max-width: 860px; }
.top-banner {
    background: linear-gradient(90deg, #0f4c75 0%, #1b6ca8 100%);
    padding: 0 2rem; height: 58px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 16px rgba(15,76,117,0.35);
    position: fixed; top: 0; left: 260px; right: 0;
    width: calc(100vw - 260px); z-index: 9998; margin: 0;
}
.nav-left  { display: flex; align-items: center; gap: 10px; }
.nav-icon  {
    width: 32px; height: 32px; border-radius: 8px;
    background: rgba(255,255,255,0.18);
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
}
.nav-title { font-size: 1rem; font-weight: 700; color: white; }
.nav-right { display: flex; align-items: center; gap: 12px; }
.nav-pill  {
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 20px; padding: 4px 13px;
    font-size: 0.74rem; color: rgba(255,255,255,0.88);
}
.nav-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #4ade80; box-shadow: 0 0 6px #4ade80;
    display: inline-block; margin-right: 5px;
}

.type-badges { display: flex; gap: 8px; margin-bottom: 1rem; flex-wrap: wrap; }
.tbadge { padding: 3px 11px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; }
.tbadge-pdf  { background:#fef2f2; border:1px solid #fca5a5; color:#dc2626; }
.tbadge-pptx { background:#fff7ed; border:1px solid #fdba74; color:#ea580c; }

[data-testid="stFileUploader"]   { background: transparent !important; }
[data-testid="stFileDropzone"] {
    background: rgba(255,255,255,0.65) !important;
    border: 1.5px dashed rgba(27,108,168,0.35) !important;
    border-radius: 12px !important;
}
[data-testid="stFileDropzone"] * { color: #1e3a5f !important; font-size: 0.9rem !important; }
[data-testid="stFileUploader"] label   { display: none !important; }
[data-testid="stFileUploader"] section { background: transparent !important; }

.stButton > button {
    background: linear-gradient(90deg, #0f4c75, #1b6ca8) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important; font-size: 1rem !important;
    padding: 0.7rem 2rem !important; width: 100% !important;
    margin-top: 0.75rem;
    box-shadow: 0 4px 14px rgba(15,76,117,0.3) !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0px) !important; }

.result-header { display: flex; align-items: center; gap: 10px; margin: 1.75rem 0 0.75rem; }
.rh-bar {
    width: 4px; height: 22px; border-radius: 2px;
    background: linear-gradient(180deg,#0f4c75,#1b6ca8);
}
.rh-title { font-size: 1rem; font-weight: 700; color: #0f4c75; }
.rh-badge {
    background: #e0f2fe; border: 1px solid #7dd3fc;
    color: #0369a1; font-size: 0.7rem; font-weight: 600;
    padding: 2px 9px; border-radius: 20px; margin-left: auto;
}
.summary-card {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 14px; padding: 1.5rem 1.75rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(15,76,117,0.08);
}
.sc-text { font-size: 0.95rem; color: #1e3a5f; line-height: 1.9; }
.meta-row {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin-top: 1rem; padding-top: 1rem;
    border-top: 1px solid rgba(15,76,117,0.1);
}
.meta-chip {
    background: rgba(15,76,117,0.07);
    border: 1px solid rgba(15,76,117,0.15);
    border-radius: 8px; padding: 4px 11px;
    font-size: 0.75rem; color: #0f4c75; font-weight: 500;
}
.meta-chip span { color: #1b6ca8; font-weight: 700; }

.detail-hint {
    background: rgba(255, 247, 237, 0.85);
    border: 1px solid rgba(253, 186, 116, 0.6);
    border-radius: 10px; padding: 0.6rem 1rem;
    font-size: 0.82rem; color: #92400e;
    margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 8px;
}

/* ── SharePoint section ── */
.sp-section-wrap {
    background: rgba(255,255,255,0.60);
    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 24px rgba(15,76,117,0.07);
    margin: 1.25rem 0;
}
.sp-header-row {
    display: flex; align-items: center; gap: 12px; margin-bottom: 1.2rem;
}
.sp-icon-box {
    width: 38px; height: 38px; border-radius: 10px;
    background: rgba(24,95,165,0.1);
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.sp-head-title { font-size: 1rem; font-weight: 700; color: #0f4c75; }
.sp-head-sub   { font-size: 0.74rem; color: #5a7fa8; margin-top: 1px; }

/* ── Simple file list rows (replaces glitchy card grid) ── */
.sp-files-label {
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.09em; color: #5a7fa8; margin-bottom: 0.6rem;
}
.sp-file-row {
    display: flex; align-items: center; gap: 10px;
    padding: 0.5rem 0.75rem; border-radius: 8px;
    margin-bottom: 4px;
    background: rgba(255,255,255,0.5);
    border: 1px solid rgba(15,76,117,0.08);
}
.sp-file-row-icon { font-size: 1rem; flex-shrink: 0; }
.sp-file-row-name {
    font-size: 0.84rem; color: #1e3a5f; font-weight: 500;
    flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.sp-file-row-ext {
    font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #7a9abf;
    background: rgba(15,76,117,0.07); border-radius: 5px;
    padding: 1px 7px; flex-shrink: 0;
}

.chat-header { display: flex; align-items: center; gap: 10px; margin: 2rem 0 1rem; }
.chat-header-bar {
    width: 4px; height: 22px; border-radius: 2px;
    background: linear-gradient(180deg,#0f4c75,#1b6ca8);
}
.chat-header-title { font-size: 1rem; font-weight: 700; color: #0f4c75; }
.chat-header-badge {
    background: #f0fdf4; border: 1px solid #86efac;
    color: #16a34a; font-size: 0.7rem; font-weight: 600;
    padding: 2px 9px; border-radius: 20px; margin-left: auto;
}

.pinned-banner {
    background: rgba(251,191,36,0.12);
    border: 1px solid rgba(251,191,36,0.35);
    border-radius: 10px; padding: 0.6rem 1rem;
    margin-bottom: 0.4rem;
    display: flex; align-items: flex-start; gap: 8px;
}
.pinned-banner-icon { font-size: 0.85rem; margin-top: 1px; flex-shrink: 0; }
.pinned-banner-text { font-size: 0.82rem; color: #78350f; line-height: 1.5; }
.pinned-banner-q { font-weight: 700; }
.pinned-section-label {
    font-size: 0.72rem; font-weight: 600; color: #92400e;
    text-transform: uppercase; letter-spacing: 0.08em;
    margin: 1.2rem 0 0.4rem;
    display: flex; align-items: center; gap: 6px;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
    margin-bottom: 0.6rem !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stChatMessage"] p {
    color: #1e3a5f !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
}
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.75) !important;
    border: 1.5px solid rgba(27,108,168,0.3) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}
[data-testid="stChatInput"] textarea { color: #1e3a5f !important; font-size: 0.92rem !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(90deg, #0f4c75, #1b6ca8) !important;
    border-radius: 8px !important;
}

.streamlit-expanderHeader {
    background: rgba(255,255,255,0.5) !important;
    border-radius: 8px !important; color: #0f4c75 !important; font-size: 0.85rem !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.4) !important;
    border-radius: 0 0 8px 8px !important;
    font-size: 0.82rem !important; color: #1e3a5f !important;
}

[data-testid="stDownloadButton"] > button {
    background: rgba(255,255,255,0.6) !important;
    color: #0f4c75 !important;
    border: 1px solid rgba(15,76,117,0.25) !important;
    border-radius: 10px !important; font-size: 0.85rem !important;
    font-weight: 600 !important; padding: 0.55rem 1rem !important;
    width: 100% !important; transition: background 0.2s !important;
    box-shadow: none !important; margin-top: 0 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,255,255,0.85) !important;
    transform: translateY(-1px) !important; opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
BASE_URL     = "http://127.0.0.1:8000"
USER_ID      = "1"
COUNTER_FILE = "/tmp/docsummarize_counter.json"

def load_counts():
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE) as f:
                data = json.load(f)
                return data.get("doc_count", 0), data.get("chat_count", 0)
        except Exception:
            return 0, 0
    return 0, 0

def save_counts(doc_n, chat_n):
    try:
        with open(COUNTER_FILE, "w") as f:
            json.dump({"doc_count": doc_n, "chat_count": chat_n}, f)
    except Exception:
        pass

def generate_pdf(summary_html, fname, ext2, detail_level):
    try:
        from fpdf import FPDF
        plain = (summary_html
                 .replace("<strong>", "").replace("</strong>", "")
                 .replace("<br>", "\n").replace("<br/>", "\n"))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(20, 20, 20)
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(15, 76, 117)
        pdf.cell(0, 12, "Document Summary", ln=True)
        pdf.ln(2)
        pdf.set_draw_color(15, 76, 117)
        pdf.set_line_width(0.5)
        pdf.line(20, pdf.get_y(), 190, pdf.get_y())
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 6, f"File: {fname}   |   Format: {ext2}   |   Detail: {detail_level}", ln=True)
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(30, 58, 95)
        pdf.multi_cell(0, 7, plain)
        return bytes(pdf.output()), True
    except ImportError:
        return None, False
    except Exception:
        return None, False

# ── Session state ──────────────────────────────────────────────────────
if "summary"          not in st.session_state: st.session_state.summary        = None
if "messages"         not in st.session_state: st.session_state.messages       = []
if "history"          not in st.session_state: st.session_state.history        = []
if "summary_detail"   not in st.session_state: st.session_state.summary_detail = None
if "show_files"       not in st.session_state: st.session_state.show_files     = False
if "synced_files"     not in st.session_state: st.session_state.synced_files   = []
if "selected_sp_file" not in st.session_state: st.session_state.selected_sp_file = None
if "chat_history"     not in st.session_state: st.session_state.chat_history   = []

_doc_count, _chat_count = load_counts()
if "doc_count"  not in st.session_state: st.session_state.doc_count  = _doc_count
if "chat_count" not in st.session_state: st.session_state.chat_count = _chat_count

def current_doc_name():
    return st.session_state.history[0]["name"] if st.session_state.history else "Unknown doc"

def add_to_chat_history(question, answer):
    entry = {
        "id":       len(st.session_state.chat_history),
        "question": question,
        "answer":   answer,
        "time":     datetime.now().strftime("%H:%M"),
        "pinned":   False,
        "doc":      current_doc_name(),
    }
    st.session_state.chat_history.insert(0, entry)
    unpinned = [e for e in st.session_state.chat_history if not e["pinned"]]
    if len(unpinned) > 50:
        oldest_unpinned = unpinned[-1]
        st.session_state.chat_history = [
            e for e in st.session_state.chat_history
            if e["id"] != oldest_unpinned["id"]
        ]

def toggle_pin(entry_id):
    for entry in st.session_state.chat_history:
        if entry["id"] == entry_id:
            entry["pinned"] = not entry["pinned"]
            break

def clean_name(f):
    return f.replace(".enc", "")

def get_ext_icon(name):
    n = name.lower()
    if n.endswith(".pptx") or n.endswith(".pptm"):
        return "📊", "PPTX"
    return "📄", "PDF"

def short_name(name, max_len=42):
    return name[:max_len] + "…" if len(name) > max_len else name

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="s-icon">📄</div>
        <div>
            <div class="s-title">DocSummarize</div>
            <div class="s-sub">AI-powered · Multimodal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Your stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size:1.4rem">📂</div>
        <div>
            <div class="sc-val">{st.session_state.doc_count}</div>
            <div class="sc-lbl">Docs summarized</div>
        </div>
    </div>
    <div class="stat-card">
        <div style="font-size:1.4rem">💬</div>
        <div>
            <div class="sc-val">{st.session_state.chat_count}</div>
            <div class="sc-lbl">Chat messages</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Summary settings</div>', unsafe_allow_html=True)
    detail_level = st.select_slider(
        "📊 Detail level",
        options=["Brief", "Standard", "Thorough"],
        value=st.session_state.get("detail_level", "Standard"),
        key="detail_level",
    )
    detail_changed = (
        st.session_state.summary is not None
        and st.session_state.summary_detail != detail_level
    )
    if detail_changed:
        st.markdown(
            '<div class="detail-hint">⚠️ Detail level changed — click <strong>Summarize</strong> to regenerate.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Recent documents</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown("""
        <div class="hist-empty">🗂️<br/>No documents yet.<br/>Upload one to get started.</div>
        """, unsafe_allow_html=True)
    else:
        for item in st.session_state.history:
            st.markdown(f"""
            <div class="hist-item">
                <div class="hi-icon">{item['icon']}</div>
                <div style="overflow:hidden">
                    <div class="hi-name">{item['name']}</div>
                    <div class="hi-time">{item['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Chat history</div>', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="hist-empty">💬<br/>No chats yet.<br/>Ask a question after uploading.</div>
        """, unsafe_allow_html=True)
    else:
        pinned_entries   = [e for e in st.session_state.chat_history if e["pinned"]]
        unpinned_entries = [e for e in st.session_state.chat_history if not e["pinned"]]

        if pinned_entries:
            st.markdown('<div style="padding:0 1rem 0.2rem;font-size:0.65rem;color:rgba(251,191,36,0.7)!important;font-weight:600;letter-spacing:0.06em;">📌 PINNED</div>', unsafe_allow_html=True)
            for entry in pinned_entries:
                q_short = entry["question"][:32] + "…" if len(entry["question"]) > 32 else entry["question"]
                a_short = entry["answer"][:38] + "…"   if len(entry["answer"])   > 38 else entry["answer"]
                col_txt, col_btn = st.columns([5, 1])
                with col_txt:
                    st.markdown(f"""
                    <div class="ch-item pinned">
                        <div class="ch-q">📌 {q_short}</div>
                        <div class="ch-a">{a_short}</div>
                        <div class="ch-meta">
                            <span class="ch-time">{entry['time']} · {entry['doc'][:18]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.button("✕", key=f"unpin_{entry['id']}", help="Unpin"):
                        toggle_pin(entry["id"])
                        st.rerun()

        if unpinned_entries:
            if pinned_entries:
                st.markdown('<div style="padding:0 1rem 0.2rem;font-size:0.65rem;color:rgba(255,255,255,0.3)!important;font-weight:600;letter-spacing:0.06em;">RECENT</div>', unsafe_allow_html=True)
            for entry in unpinned_entries[:8]:
                q_short = entry["question"][:32] + "…" if len(entry["question"]) > 32 else entry["question"]
                a_short = entry["answer"][:38] + "…"   if len(entry["answer"])   > 38 else entry["answer"]
                col_txt, col_btn = st.columns([5, 1])
                with col_txt:
                    st.markdown(f"""
                    <div class="ch-item">
                        <div class="ch-q">{q_short}</div>
                        <div class="ch-a">{a_short}</div>
                        <div class="ch-meta">
                            <span class="ch-time">{entry['time']} · {entry['doc'][:18]}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    if st.button("📌", key=f"pin_{entry['id']}", help="Pin this chat"):
                        toggle_pin(entry["id"])
                        st.rerun()

        if unpinned_entries:
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
            if st.button("🗑 Clear unpinned", key="clear_unpinned"):
                st.session_state.chat_history = [
                    e for e in st.session_state.chat_history if e["pinned"]
                ]
                st.rerun()

    st.markdown("""
    <div style='text-align:center;padding:1.5rem 0 0.5rem;
         font-size:0.68rem;color:rgba(255,255,255,0.25)'>
        v2.2.0 · DocSummarize AI
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# MAIN — NAVBAR
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="top-banner">
    <div class="nav-left">
        <div class="nav-icon">📄</div>
        <span class="nav-title">Multimodal Document Summarization App</span>
    </div>
    <div class="nav-right">
        <span class="nav-pill"><span class="nav-dot"></span>AI Ready</span>
        <span class="nav-pill">PDF · PPTX</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="type-badges">
    <span class="tbadge tbadge-pdf">📄 PDF</span>
    <span class="tbadge tbadge-pptx">📊 PPTX</span>
</div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "upload",
    type=["pdf", "pptx", "pptm"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

# ══════════════════════════════════════════════════════════════════════
# SHAREPOINT SECTION
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="sp-section-wrap">
    <div class="sp-header-row">
        <div class="sp-icon-box">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                 stroke="#185FA5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
            </svg>
        </div>
        <div>
            <div class="sp-head-title">SharePoint files</div>
            <div class="sp-head-sub">Sync from OneDrive and select a document to summarize</div>
        </div>
    </div>
""", unsafe_allow_html=True)

sync_col, hint_col = st.columns([1, 3])
with sync_col:
    sync_clicked = st.button("🔄  Sync files", key="sp_sync_btn")
with hint_col:
    st.markdown(
        "<div style='padding-top:0.9rem;font-size:0.78rem;color:#7a9abf;'>Fetch latest files from SharePoint</div>",
        unsafe_allow_html=True,
    )

if sync_clicked:
    with st.spinner("Connecting to SharePoint…"):
        try:
            res = requests.get(f"{BASE_URL}/sync-sharepoint")
            if res.status_code == 200:
                count = res.json().get("files_synced_count", 0)
                st.session_state.show_files = True
                files_res = requests.get(f"{BASE_URL}/user-files")
                st.session_state.synced_files = files_res.json().get("files", [])
                st.session_state.selected_sp_file = None
                st.success(f"✅ {count} file{'s' if count != 1 else ''} synced successfully")
            else:
                st.error("Sync failed — could not reach SharePoint.")
        except Exception as e:
            st.error(f"Connection error: {e}")

# ── File list (shown after sync) — NO JS, NO card grid ───────────────
if st.session_state.show_files:
    synced_files = st.session_state.synced_files

    if not synced_files:
        st.markdown("""
        <div style="text-align:center;padding:2rem 1rem;font-size:0.85rem;color:#7a9abf;
             border:1.5px dashed rgba(15,76,117,0.18);border-radius:12px;margin:0.5rem 0;">
            No files found in SharePoint.<br/>
            <span style="font-size:0.78rem;">Make sure your OneDrive sync is active.</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="sp-files-label">{len(synced_files)} document{"s" if len(synced_files) != 1 else ""} available</div>',
            unsafe_allow_html=True,
        )

        # Simple styled file list — pure HTML, no JS
        rows_html = ""
        for f in synced_files:
            display = clean_name(f)
            icon, ext_badge = get_ext_icon(display)
            rows_html += f"""<div class="sp-file-row">
                <span class="sp-file-row-icon">{icon}</span>
                <span class="sp-file-row-name">{short_name(display, 60)}</span>
                <span class="sp-file-row-ext">{ext_badge}</span>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        # Selectbox is the only interactive element
        st.markdown(
            "<div style='font-size:0.8rem;color:#5a7fa8;font-weight:500;margin-bottom:4px;'>Select document to summarize:</div>",
            unsafe_allow_html=True,
        )
        file_options = ["— choose a file —"] + [clean_name(f) for f in synced_files]
        chosen = st.selectbox(
            "file_selector",
            options=file_options,
            index=0,
            label_visibility="collapsed",
            key="sp_file_selector",
        )
        if chosen != "— choose a file —":
            idx = [clean_name(f) for f in synced_files].index(chosen)
            st.session_state.selected_sp_file = synced_files[idx]
        else:
            st.session_state.selected_sp_file = None

        if st.session_state.selected_sp_file:
            sel_file = st.session_state.selected_sp_file
            st.markdown(
                f"""<div style="display:flex;align-items:center;gap:10px;
                    background:rgba(24,95,165,0.07);border:1.5px solid rgba(24,95,165,0.18);
                    border-radius:11px;padding:12px 16px;margin-top:8px;">
                    <div style="flex:1;font-size:0.84rem;color:#2a5080;font-weight:500;">
                        Ready to summarize: <strong style="color:#0f4c75;">{short_name(clean_name(sel_file), 45)}</strong>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button("✦  Summarize selected document", key="sp_summarize_btn"):
                st.session_state.selected_file = sel_file

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PROCESS SELECTED SHAREPOINT FILE
# ══════════════════════════════════════════════════════════════════════
if "selected_file" in st.session_state:
    file = st.session_state.selected_file
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.6);border:1px solid rgba(255,255,255,0.85);
         border-radius:12px;padding:1rem 1.25rem;margin:1rem 0;
         font-size:0.88rem;color:#0f4c75;font-weight:600;">
        ⚙️ Processing: <span style="font-weight:400;color:#2a5080;">{clean_name(file)}</span>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Analyzing document with AI…"):
        try:
            res = requests.post(
                f"{BASE_URL}/upload",
                params={"user_id": USER_ID},
                data={"file_name": file},
            )
            if res.status_code == 200:
                data = res.json()
                st.session_state.summary = data.get("summary", "No summary returned")
                st.session_state.summary_detail = st.session_state.detail_level
                icon_map = {"pdf": "📄", "pptx": "📊", "pptm": "📊"}
                ext = clean_name(file).rsplit(".", 1)[-1].lower() if "." in file else "pdf"
                st.session_state.history.insert(0, {
                    "name": clean_name(file),
                    "time": "Just now",
                    "icon": icon_map.get(ext, "📄"),
                })
                st.session_state.history = st.session_state.history[:5]
                st.session_state.doc_count += 1
                st.session_state.messages = []
                save_counts(st.session_state.doc_count, st.session_state.chat_count)
                del st.session_state.selected_file
                st.session_state.selected_sp_file = None
                st.rerun()
            else:
                st.error(f"Failed to summarize: {res.text}")
                del st.session_state.selected_file
        except Exception as e:
            st.error(f"Connection error: {e}")
            del st.session_state.selected_file

# ── Summarize uploaded files ──────────────────────────────────────────
if uploaded_files:
    if st.button("✦  Summarize Document"):
        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        with st.spinner("Analyzing your document with AI…"):
            response = requests.post(
                f"{BASE_URL}/upload-multiple",
                files=files,
                params={"user_id": USER_ID, "detail_level": st.session_state.detail_level},
            )
        if response.status_code == 200:
            data = response.json()
            file_summaries = data.get("file_summaries", {})
            if len(file_summaries) == 1:
                st.session_state.summary = list(file_summaries.values())[0]
            else:
                combined = ""
                for file_name, summary in file_summaries.items():
                    combined += f"<strong>{file_name}</strong><br>{summary}<br><br>"
                st.session_state.summary = combined

            st.session_state.summary_detail = st.session_state.detail_level
            icon_map = {"pdf": "📄", "pptx": "📊", "pptm": "📊"}
            for f in uploaded_files:
                ext = f.name.rsplit(".", 1)[-1].lower()
                st.session_state.history.insert(0, {
                    "name": f.name, "time": "Just now",
                    "icon": icon_map.get(ext, "📄"),
                })
            st.session_state.history = st.session_state.history[:5]
            st.session_state.doc_count += 1
            st.session_state.messages = []
            save_counts(st.session_state.doc_count, st.session_state.chat_count)
            st.rerun()
        else:
            st.error(response.text)

# ── Summary output ────────────────────────────────────────────────────
if st.session_state.summary:
    st.markdown("""
    <div class="result-header">
        <div class="rh-bar"></div>
        <div class="rh-title">Summarization</div>
        <div class="rh-badge">✓ Complete</div>
    </div>
    """, unsafe_allow_html=True)

    fname        = st.session_state.history[0]["name"] if st.session_state.history else "document"
    ext2         = fname.rsplit(".", 1)[-1].upper() if "." in fname else "FILE"
    shown_detail = st.session_state.summary_detail or st.session_state.detail_level

    st.markdown(f"""
    <div class="summary-card">
        <div class="sc-text">{st.session_state.summary}</div>
        <div class="meta-row">
            <div class="meta-chip">📁 Format: <span>{ext2}</span></div>
            <div class="meta-chip">📊 Detail: <span>{shown_detail}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    raw      = st.session_state.summary.replace("<strong>","").replace("</strong>","").replace("<br>","\n")
    md       = st.session_state.summary.replace("<strong>","**").replace("</strong>","**").replace("<br>","\n")
    pdf_bytes, pdf_ok = generate_pdf(st.session_state.summary, fname, ext2, shown_detail)

    dl1, dl2, dl3, dl4 = st.columns(4)
    with dl1:
        st.download_button("⬇  Download .txt", data=raw, file_name="summary.txt",
                           mime="text/plain", use_container_width=True)
    with dl2:
        st.download_button("⬇  Download .md", data=f"# Summary\n\n{md}",
                           file_name="summary.md", mime="text/markdown", use_container_width=True)
    with dl3:
        if pdf_ok and pdf_bytes:
            st.download_button("⬇  Download .pdf", data=pdf_bytes, file_name="summary.pdf",
                               mime="application/pdf", use_container_width=True)
        else:
            st.button("⬇  .pdf — run: pip install fpdf2", disabled=True,
                      use_container_width=True, help="pip install fpdf2")
    with dl4:
        if st.button("🔄  New Document", use_container_width=True):
            st.session_state.summary        = None
            st.session_state.summary_detail = None
            st.session_state.messages       = []
            st.rerun()

    pinned = [e for e in st.session_state.chat_history if e["pinned"]]
    if pinned:
        st.markdown('<div class="pinned-section-label">📌 Pinned exchanges</div>', unsafe_allow_html=True)
        for entry in pinned:
            st.markdown(f"""
            <div class="pinned-banner">
                <div class="pinned-banner-icon">📌</div>
                <div class="pinned-banner-text">
                    <span class="pinned-banner-q">Q: {entry['question']}</span><br>
                    A: {entry['answer'][:180]}{'…' if len(entry['answer']) > 180 else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-bar"></div>
        <div class="chat-header-title">💬 Chat with your document</div>
        <div class="chat-header-badge">● Live</div>
    </div>
    """, unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                user_q = ""
                if i > 0 and st.session_state.messages[i-1]["role"] == "user":
                    user_q = st.session_state.messages[i-1]["content"]
                match = next(
                    (e for e in st.session_state.chat_history
                     if e["question"] == user_q and e["answer"] == msg["content"]),
                    None
                )
                if match:
                    pin_label = "📌 Unpin" if match["pinned"] else "📌 Pin"
                    if st.button(pin_label, key=f"msgpin_{match['id']}_{i}"):
                        toggle_pin(match["id"])
                        st.rerun()

    if prompt := st.chat_input("Ask anything about your document…"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                res = requests.post(f"{BASE_URL}/chat", json={"user_id": USER_ID, "query": prompt})
                if res.status_code == 200:
                    data   = res.json()
                    answer = data.get("answer", "No answer returned.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    add_to_chat_history(prompt, answer)
                    st.session_state.chat_count += 1
                    save_counts(st.session_state.doc_count, st.session_state.chat_count)

                    if "sources" in data:
                        with st.expander("📚 Sources"):
                            for i, src in enumerate(data["sources"]):
                                st.write(f"{i+1}. ({src.get('file','unknown')}) {src['content']}…")

                    match = next(
                        (e for e in st.session_state.chat_history if e["question"] == prompt),
                        None
                    )
                    if match:
                        if st.button("📌 Pin this answer", key=f"newpin_{match['id']}"):
                            toggle_pin(match["id"])
                            st.rerun()
                else:
                    st.error(res.text)

    if st.session_state.messages:
        if st.button("🧹  Clear Chat"):
            st.session_state.messages = []
            st.rerun()