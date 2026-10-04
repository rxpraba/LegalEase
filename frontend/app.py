"""LegalEase - AI Legal Document Studio
Modern, high-performance UI with rich aesthetics, glassmorphism, and color accents.
"""
import base64
import html
import inspect
import sys
import time
from datetime import date
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

import requests
import streamlit as st

# Clean cross-version button width kwargs without deprecation warnings
BTN_KWARGS = (
    {"width": "stretch"}
    if "width" in inspect.signature(st.button).parameters
    else {"use_container_width": True}
)


from ai_core.generator import (
    format_docx,
    format_html_preview,
    format_pdf,
    sanitize_text,
)
from config import BACKEND_URL, WEB_LOGO_PATH

# -----------------------------------------------------------------------------
# Helper: Safe HTML Renderer (prevents markdown 4-space code block glitch)
# -----------------------------------------------------------------------------
def render_html(html_str: str):
    """Strip leading/trailing space from each line to prevent CommonMark code-block parsing."""
    clean_lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LegalEase Studio | AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Custom Modern CSS (Luxury Dark Glassmorphism & Neon Legal Tech Gradients)
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #090D16;
    --bg-secondary: #0F172A;
    --bg-card: rgba(15, 23, 42, 0.75);
    --border-color: rgba(255, 255, 255, 0.08);
    --accent-indigo: #6366F1;
    --accent-cyan: #06B6D4;
    --accent-purple: #8B5CF6;
    --accent-amber: #F59E0B;
    --accent-emerald: #10B981;
    --text-primary: #F8FAFC;
    --text-muted: #94A3B8;
}

/* Base resets & typography */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 90% 10%, rgba(6, 182, 212, 0.10) 0%, transparent 35%),
                radial-gradient(circle at 50% 90%, rgba(139, 92, 246, 0.10) 0%, transparent 45%),
                #080C14;
    background-attachment: fixed;
}

/* Block padding */
.main .block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Style native Streamlit bordered containers with Glassmorphism */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-color) !important;
    border-radius: 18px !important;
    padding: 8px 12px;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(99, 102, 241, 0.35) !important;
}

/* Header Banner */
.brand-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 28px;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.85));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 9999px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(6, 182, 212, 0.2));
    border: 1px solid rgba(99, 102, 241, 0.4);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #A5B4FC;
}

.status-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
}

/* Gradient Titles */
.gradient-title {
    background: linear-gradient(135deg, #FFFFFF 20%, #A5B4FC 60%, #38BDF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 1.85rem;
    letter-spacing: -0.02em;
    margin: 0;
}

.gradient-subtitle {
    color: var(--text-muted);
    font-size: 0.92rem;
    margin-top: 4px;
}

/* Form Section Labels */
.section-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #38BDF8;
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

/* Button Stylings */
div.stButton > button:first-child {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #06B6D4 100%);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 1rem;
    padding: 0.75rem 1.5rem;
    border-radius: 12px;
    border: none;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.5);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.02em;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 35px -5px rgba(79, 70, 229, 0.7);
    color: #FFFFFF;
}

div.stButton > button:first-child:active {
    transform: translateY(0);
}

/* Download Buttons */
div[data-testid="stDownloadButton"] > button {
    background: rgba(30, 41, 59, 0.85);
    color: #F1F5F9;
    border: 1px solid rgba(255, 255, 255, 0.12);
    font-weight: 600;
    font-size: 0.85rem;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(51, 65, 85, 0.95);
    border-color: #38BDF8;
    color: #FFFFFF;
    transform: translateY(-1px);
}

/* Text Inputs and Text Areas */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}

/* Legal Document Parchment Paper View */
.legal-parchment {
    background: #0B1120;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 36px 42px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.4), 0 20px 40px rgba(0, 0, 0, 0.6);
    font-family: 'Playfair Display', Georgia, serif;
    color: #E2E8F0;
    line-height: 1.85;
    max-height: 550px;
    overflow-y: auto;
}

.legal-parchment h4 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #67E8F9;
    letter-spacing: 0.04em;
    border-bottom: 1px solid rgba(103, 232, 249, 0.2);
    padding-bottom: 6px;
    margin-top: 24px;
    font-size: 1.05rem;
    font-weight: 700;
}

.legal-parchment p {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.98rem;
    color: #CBD5E1;
    margin: 8px 0;
    text-align: justify;
}

.legal-parchment li {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #E2E8F0;
    margin: 4px 0 4px 18px;
    font-size: 0.92rem;
}

/* Metric Cards */
.metrics-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}

.metric-pill {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 14px;
    text-align: center;
}

.metric-val {
    font-weight: 800;
    font-size: 1.15rem;
    color: #F8FAFC;
    background: linear-gradient(135deg, #FFFFFF, #93C5FD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-lbl {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94A3B8;
    margin-top: 2px;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.5);
}
::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.4);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.7);
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Template Library for 1-Click Fast Fill
# -----------------------------------------------------------------------------
TEMPLATES = {
    "Select a pre-built template...": {
        "doc_type": "",
        "parties": "",
        "terms": "",
        "dates": "",
    },
    "🔒 Non-Disclosure Agreement (Mutual NDA)": {
        "doc_type": "Mutual Non-Disclosure Agreement",
        "parties": "Nexus Technologies Inc. (Disclosing Party) and Apex Labs LLC (Receiving Party)",
        "terms": (
            "Definition of Confidential Information includes source code, proprietary algorithms, and business plans; "
            "Confidentiality obligations survive for a duration of 3 years from Effective Date; "
            "Exclusions include publicly available knowledge and independently developed items; "
            "Standard remedies including immediate injunctive relief without bond; "
            "Governing Law and exclusive jurisdiction shall be the State of California"
        ),
        "dates": date.today().strftime("%B %d, %Y"),
    },
    "💼 Independent Contractor / Master Services": {
        "doc_type": "Independent Contractor Agreement",
        "parties": "Acme Innovations Ltd (Client) and Sarah Jenkins (Contractor)",
        "terms": (
            "Scope covers full-stack web and cloud architecture consulting; "
            "Fixed compensation rate of $150.00 USD per hour billed bi-weekly; "
            "Work-for-hire assignment vesting all Intellectual Property rights in Client; "
            "Termination upon 14 days written notice by either party; "
            "Mutual indemnification and limitation of liability capped at aggregate fees paid"
        ),
        "dates": date.today().strftime("%B %d, %Y"),
    },
    "🤝 Employment Offer & Key Terms Agreement": {
        "doc_type": "Executive Employment Agreement",
        "parties": "Vanguard Enterprises Inc. (Employer) and Marcus Sterling (Employee)",
        "terms": (
            "Position of Principal AI Engineer reporting to VP of Technology; "
            "Base annual salary of $185,000 USD plus performance bonus eligibility; "
            "Comprehensive health, retirement 401(k) with 4% match, and 20 days paid PTO; "
            "At-will employment relationship subject to 30-day transition notice; "
            "Non-solicitation of clients and staff for 12 months post-departure"
        ),
        "dates": date.today().strftime("%B %d, %Y"),
    },
    "⚡ SaaS Terms of Service & Data SLA": {
        "doc_type": "Software-as-a-Service (SaaS) Agreement",
        "parties": "CloudScale Cloud Inc. (Vendor) and Enterprise Subscriber (Customer)",
        "terms": (
            "Service level availability guarantee of 99.9% uptime with service credits for downtime; "
            "Customer retains sole ownership of all customer uploaded data; "
            "Vendor maintains SOC-2 Type II, GDPR, and CCPA data privacy compliance; "
            "Annual subscription tier with net-30 automatic renewal invoicing; "
            "Total aggregate liability limited to twelve months preceding subscription fees"
        ),
        "dates": date.today().strftime("%B %d, %Y"),
    },
    "📜 Power of Attorney (Limited Business Representation)": {
        "doc_type": "Limited Power of Attorney",
        "parties": "Jonathan Reed (Principal) and Elena Rostova, Esq. (Attorney-in-Fact)",
        "terms": (
            "Specific authorization to sign real estate deed transfer documents; "
            "Power to negotiate escrow settlement terms not exceeding $750,000 USD; "
            "No authority for general banking, credit line creation, or personal loan guarantees; "
            "Power automatically expires 60 days following execution; "
            "Governing law established under the statutes of New York State"
        ),
        "dates": date.today().strftime("%B %d, %Y"),
    },
}

# -----------------------------------------------------------------------------
# Header Bar
# -----------------------------------------------------------------------------
logo_html = ""
if WEB_LOGO_PATH.exists():
    with open(WEB_LOGO_PATH, "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode()
        logo_html = f"<img src='data:image/png;base64,{encoded_logo}' style='height:44px; margin-right:16px; vertical-align:middle; filter:drop-shadow(0 2px 8px rgba(0,0,0,0.4));' />"

render_html(
    f"""
<div class="brand-header">
    <div style="display:flex; align-items:center;">
        {logo_html}
        <div>
            <h1 class="gradient-title">LegalEase Studio</h1>
            <div class="gradient-subtitle">Enterprise AI Legal Document Drafting & Export Suite</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:10px;">
        <span class="brand-badge">⚡ Gemini Intelligence</span>
        <span class="status-chip">● API Live</span>
    </div>
</div>
"""
)

# -----------------------------------------------------------------------------
# Main Studio Layout (Columns: Left for Input Studio / Right for Preview)
# -----------------------------------------------------------------------------
left_col, right_col = st.columns([1, 1.25], gap="large")

# Manage input fields in session state for fast template populating
if "input_doc_type" not in st.session_state:
    st.session_state.input_doc_type = "Mutual Non-Disclosure Agreement"
if "input_parties" not in st.session_state:
    st.session_state.input_parties = "Alpha Tech Corp and Beta Systems LLC"
if "input_terms" not in st.session_state:
    st.session_state.input_terms = (
        "Confidentiality for 2 years; Non-circumvention; Standard arbitration in Delaware"
    )
if "input_dates" not in st.session_state:
    st.session_state.input_dates = date.today().strftime("%B %d, %Y")

# -----------------------------------------------------------------------------
# LEFT COLUMN: Document Drafting Studio
# -----------------------------------------------------------------------------
with left_col:
    with st.container(border=True):
        render_html(
            '<div class="section-tag">✨ Step 1 &bull; Instant Template Accelerator</div>'
        )

        selected_tpl = st.selectbox(
            "Choose an agreement blueprint to auto-fill:",
            list(TEMPLATES.keys()),
            index=0,
            label_visibility="collapsed",
        )

        if (
            selected_tpl != "Select a pre-built template..."
            and TEMPLATES[selected_tpl]["doc_type"]
        ):
            tpl_data = TEMPLATES[selected_tpl]
            if st.session_state.get("_last_tpl") != selected_tpl:
                st.session_state.input_doc_type = tpl_data["doc_type"]
                st.session_state.input_parties = tpl_data["parties"]
                st.session_state.input_terms = tpl_data["terms"]
                st.session_state.input_dates = tpl_data["dates"]
                st.session_state._last_tpl = selected_tpl
                st.rerun()

        render_html(
            '<div class="section-tag" style="margin-top:14px;">📋 Step 2 &bull; Contract Parameters</div>'
        )

        doc_type = st.text_input(
            "Document Type / Title",
            value=st.session_state.input_doc_type,
            placeholder="e.g. Non-Disclosure Agreement, Master Services Agreement",
        )

        parties = st.text_area(
            "Parties Involved",
            value=st.session_state.input_parties,
            placeholder="e.g. Party A (Disclosing Party) and Party B (Receiving Party)",
            height=80,
        )

        col_date, col_juris = st.columns([1, 1])
        with col_date:
            dates = st.text_input(
                "Effective Date",
                value=st.session_state.input_dates,
                placeholder="e.g. October 04, 2026",
            )
        with col_juris:
            governing_law = st.text_input(
                "Governing Jurisdiction",
                value="State of Delaware, USA",
                placeholder="e.g. California, UK, New York",
            )

        render_html(
            '<div class="section-tag" style="margin-top:10px;">⚖️ Step 3 &bull; Specific Terms & Clauses</div>'
        )
        st.caption("Separate specific terms or clauses using semicolons ( ; ).")

        terms = st.text_area(
            "Terms and Conditions",
            value=st.session_state.input_terms,
            placeholder="e.g. 2-year term; Net 30 payment; Severability; Non-compete within 50 miles",
            height=110,
        )

        # Quick clause adder pills
        st.markdown(
            "<div style='font-size:0.78rem; font-weight:600; color:#94A3B8; margin-bottom:6px;'>Quick Add Legal Clauses:</div>",
            unsafe_allow_html=True,
        )
        chip_col1, chip_col2, chip_col3 = st.columns(3)
        with chip_col1:
            if st.button("+ Indemnity Cap", key="c_indemn"):
                st.session_state.input_terms = (
                    terms.strip().rstrip(";") + "; Aggregate liability capped at total fees paid"
                )
                st.rerun()
        with chip_col2:
            if st.button("+ Non-Solicit", key="c_nonsol"):
                st.session_state.input_terms = (
                    terms.strip().rstrip(";")
                    + "; Non-solicitation of employees and clients for 12 months"
                )
                st.rerun()
        with chip_col3:
            if st.button("+ Force Majeure", key="c_force"):
                st.session_state.input_terms = (
                    terms.strip().rstrip(";")
                    + "; Standard force majeure excluding payment obligations"
                )
                st.rerun()

        st.markdown('<div style="margin-top:14px;"></div>', unsafe_allow_html=True)
        generate_btn = st.button(
            "✨ Generate Legal Document Now",
            **BTN_KWARGS,
        )

# -----------------------------------------------------------------------------
# Trigger Generation
# -----------------------------------------------------------------------------
if generate_btn:
    if not doc_type.strip() or not parties.strip():
        st.warning("⚠️ Please provide at least a Document Type and the Parties involved.")
    else:
        full_terms = terms
        if governing_law.strip() and "governing law" not in terms.lower():
            full_terms = (
                f"{full_terms.strip().rstrip(';')}; Governing law shall be {governing_law.strip()}"
            )

        with st.spinner("🤖 Consulting Gemini AI & constructing structured legal agreement..."):
            start_gen = time.time()
            try:
                r = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": doc_type,
                        "parties": parties,
                        "terms": full_terms,
                        "dates": dates,
                    },
                    timeout=120,
                )
                r.raise_for_status()
                st.session_state.generated_text = sanitize_text(r.json()["document"])
                st.session_state.doc_type = doc_type
                st.session_state.terms = full_terms
                st.session_state.dates = dates
                st.session_state.parties = parties
                st.session_state.show_edit = False
                st.session_state.gen_time = f"{round(time.time() - start_gen, 1)}s"
                st.toast("Document generated successfully!", icon="✅")
            except requests.HTTPError:
                err_detail = r.json().get("detail", r.text) if r else "Unknown error"
                st.error(f"❌ Backend error: {err_detail}")
            except requests.RequestException as e:
                st.error(f"❌ Could not reach backend at {BACKEND_URL}: {e}")

# -----------------------------------------------------------------------------
# RIGHT COLUMN: Live Interactive Document Studio & Multi-Format Exporter
# -----------------------------------------------------------------------------
with right_col:
    if "generated_text" in st.session_state and st.session_state.generated_text:
        text = st.session_state.generated_text
        doc_title = st.session_state.get("doc_type", "Legal Agreement")
        active_terms = st.session_state.get("terms", "")
        slug = doc_title.strip().replace(" ", "_").lower() or "legal_document"

        # Compute Document Statistics
        word_count = len(text.split())
        reading_time = max(1, round(word_count / 200))
        est_pages = max(1, round(word_count / 450))
        gen_speed = st.session_state.get("gen_time", "Instant")

        with st.container(border=True):
            # Top Action Strip
            top_c1, top_c2 = st.columns([3, 1])
            with top_c1:
                render_html(
                    f"""
<div class="metrics-strip">
    <div class="metric-pill">
        <div class="metric-val">{word_count:,}</div>
        <div class="metric-lbl">Words</div>
    </div>
    <div class="metric-pill">
        <div class="metric-val">{est_pages}</div>
        <div class="metric-lbl">Est. Pages</div>
    </div>
    <div class="metric-pill">
        <div class="metric-val">{reading_time} min</div>
        <div class="metric-lbl">Read Time</div>
    </div>
    <div class="metric-pill">
        <div class="metric-val" style="color:#10B981;">{gen_speed}</div>
        <div class="metric-lbl">Draft Time</div>
    </div>
</div>
"""
                )
            with top_c2:
                if st.button("🔄 New Draft", key="btn_reset_draft", **BTN_KWARGS):
                    st.session_state.generated_text = ""
                    st.rerun()

            # Tabs for Studio View, Live Editor, and Raw Content
            tab_preview, tab_edit, tab_raw = st.tabs(
                ["📑 Formatted Legal Preview", "✏️ Edit Draft", "📋 Raw Text"]
            )

            with tab_preview:
                render_html(
                    f"""
<div class="legal-parchment">
    <div style="text-align:center; margin-bottom:20px; border-bottom:1px double rgba(255,255,255,0.15); padding-bottom:12px;">
        <span style="font-family:'Plus Jakarta Sans',sans-serif; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.15em; color:#94A3B8;">CONFIDENTIAL LEGAL DRAFT</span>
        <h2 style="font-family:'Playfair Display',serif; color:#F8FAFC; margin:8px 0; font-size:1.6rem; letter-spacing:0.02em;">{html.escape(doc_title.upper())}</h2>
        <span style="font-size:0.85rem; color:#A5B4FC;">Effective: {html.escape(st.session_state.get('dates', ''))}</span>
    </div>
    {format_html_preview(text)}
</div>
"""
                )

            with tab_edit:
                st.caption(
                    "You can refine, append clauses, or customize names below. Changes update the download files automatically."
                )
                updated_text = st.text_area(
                    "Document Editor",
                    value=text,
                    height=450,
                    label_visibility="collapsed",
                    key="editor_text_area",
                )
                if updated_text != text:
                    st.session_state.generated_text = updated_text
                    text = updated_text

            with tab_raw:
                st.code(text, language="text")

            # Multi-Format Export Station
            render_html(
                '<div class="section-tag" style="margin-top:18px;">📥 Export Station &bull; Multi-Format Downloads</div>'
            )

            d_col1, d_col2, d_col3 = st.columns(3)
            with d_col1:
                try:
                    docx_bytes = format_docx(text, doc_title, active_terms)
                    st.download_button(
                        "📄 Download .DOCX",
                        data=docx_bytes,
                        file_name=f"{slug}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        **BTN_KWARGS,
                    )
                except Exception as e:
                    st.error(f"DOCX error: {e}")

            with d_col2:
                try:
                    pdf_bytes = format_pdf(text, doc_title, active_terms)
                    st.download_button(
                        "📕 Download .PDF",
                        data=pdf_bytes,
                        file_name=f"{slug}.pdf",
                        mime="application/pdf",
                        **BTN_KWARGS,
                    )
                except Exception as e:
                    st.error(f"PDF error: {e}")

            with d_col3:
                st.download_button(
                    "📝 Download .TXT",
                    data=text,
                    file_name=f"{slug}.txt",
                    mime="text/plain",
                    **BTN_KWARGS,
                )


    else:
        # High-Impact Hero Placeholder rendered cleanly without raw HTML leakage
        with st.container(border=True):
            render_html(
                """
<div style="min-height:500px; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:36px 20px;">
    <div style="width:72px; height:72px; border-radius:20px; background:linear-gradient(135deg, rgba(99,102,241,0.25), rgba(6,182,212,0.25)); border:1px solid rgba(99,102,241,0.5); display:flex; align-items:center; justify-content:center; font-size:2rem; margin:0 auto 18px;">
        ⚖️
    </div>
    <h3 style="font-family:'Playfair Display',serif; font-size:1.6rem; margin:0 0 10px 0; color:#F8FAFC;">
        Legal Document Studio is Ready
    </h3>
    <p style="color:#94A3B8; max-width:440px; font-size:0.95rem; line-height:1.6; margin:0 auto 26px;">
        Select an enterprise contract blueprint on the left or customize your own terms, then click 
        <span style="color:#67E8F9; font-weight:600;">"Generate Legal Document Now"</span> to draft an authoritative, clause-complete agreement in seconds.
    </p>
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; width:100%; max-width:540px; text-align:left;">
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:14px;">
            <div style="color:#818CF8; font-size:1.1rem; margin-bottom:4px;">🛡️</div>
            <div style="font-weight:700; font-size:0.85rem; color:#E2E8F0;">Legally Structured</div>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">Governing law, severability & execution blocks.</div>
        </div>
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:14px;">
            <div style="color:#38BDF8; font-size:1.1rem; margin-bottom:4px;">✏️</div>
            <div style="font-weight:700; font-size:0.85rem; color:#E2E8F0;">Live In-App Editor</div>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">Instantly tweak or append clauses on the fly.</div>
        </div>
        <div style="background:rgba(30,41,59,0.5); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:14px;">
            <div style="color:#34D399; font-size:1.1rem; margin-bottom:4px;">📦</div>
            <div style="font-weight:700; font-size:0.85rem; color:#E2E8F0;">Multi-Format Export</div>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">Instant professional DOCX, PDF, and clean TXT.</div>
        </div>
    </div>
</div>
"""
            )

# -----------------------------------------------------------------------------
# Footer Notice
# -----------------------------------------------------------------------------
render_html(
    """
<div style="text-align:center; margin-top:36px; padding:16px; color:#64748B; font-size:0.78rem; border-top:1px solid rgba(255,255,255,0.06);">
    ⚠️ <strong>Legal Disclaimer:</strong> Documents generated by LegalEase AI are draft templates intended for informational purposes and operational convenience. 
    Always have drafts reviewed by a qualified legal professional before signature and execution.
</div>
"""
)
