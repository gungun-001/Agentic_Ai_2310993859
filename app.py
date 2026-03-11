"""
app.py – Streamlit UI for FireReach: Autonomous AI Outreach Agent.

Features:
  • Animated full-screen splash page (5 seconds) with particle effects
  • Premium dark-themed agent workspace with glassmorphism cards
  • Live step-by-step progress indicators
"""

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

from agent import run_agent  # noqa: E402

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FireReach – AI Outreach Agent",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False
if "result" not in st.session_state:
    st.session_state.result = None

# ═══════════════════════════════════════════════════════════════════════════════
#  SPLASH PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.splash_done:
    # Hide ALL Streamlit chrome during splash
    st.markdown(
        """
        <style>
        header, #MainMenu, footer,
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        section[data-testid="stSidebar"] { display: none !important; }
        .stApp { background: #0a0a0f !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    splash_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0a0f;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: 'Outfit', sans-serif;
        }
        .splash {
            position: relative;
            width: 100vw; height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .orb { position:absolute; border-radius:50%; filter:blur(80px); animation:orbFloat 6s ease-in-out infinite; }
        .orb-1 { width:400px; height:400px; background:radial-gradient(circle,rgba(255,107,53,0.37),transparent 70%); top:10%; left:15%; }
        .orb-2 { width:350px; height:350px; background:radial-gradient(circle,rgba(247,201,72,0.25),transparent 70%); bottom:15%; right:10%; animation-delay:-2s; }
        .orb-3 { width:300px; height:300px; background:radial-gradient(circle,rgba(232,68,48,0.19),transparent 70%); top:50%; left:60%; animation-delay:-4s; }
        @keyframes orbFloat {
            0%,100% { transform:translate(0,0) scale(1); }
            33% { transform:translate(30px,-40px) scale(1.1); }
            66% { transform:translate(-20px,30px) scale(0.95); }
        }

        .particles {
            position:absolute; width:200%; height:200%; top:-50%; left:-50%;
            background-image: radial-gradient(circle,rgba(255,107,53,0.12) 1px,transparent 1px);
            background-size: 40px 40px;
            animation: particleDrift 20s linear infinite;
        }
        @keyframes particleDrift { from{transform:translate(0,0)} to{transform:translate(-40px,-40px)} }

        .logo {
            font-size:5.5rem; opacity:0; transform:scale(0.5) translateY(30px);
            animation: logoIn 1.2s cubic-bezier(.16,1,.3,1) forwards, logoPulse 2.5s ease-in-out 1.5s infinite;
        }
        @keyframes logoIn { to{opacity:1;transform:scale(1) translateY(0)} }
        @keyframes logoPulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.08)} }

        .title {
            font-size:4.8rem; font-weight:800; letter-spacing:-2px;
            background:linear-gradient(135deg,#FF6B35,#F7C948,#FF6B35);
            background-size:200% 200%;
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            opacity:0; transform:translateY(20px);
            animation: fadeUp 1s cubic-bezier(.16,1,.3,1) .3s forwards, gradShift 3s ease-in-out infinite;
        }
        @keyframes fadeUp { to{opacity:1;transform:translateY(0)} }
        @keyframes gradShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }

        .subtitle {
            color:#777; font-size:1.25rem; font-weight:300; letter-spacing:6px;
            text-transform:uppercase; margin-top:10px;
            opacity:0; transform:translateY(15px); animation:fadeUp .8s ease .8s forwards;
        }
        .pipeline {
            display:flex; align-items:center; gap:12px; margin-top:36px;
            opacity:0; animation:fadeUp .8s ease 1.3s forwards;
        }
        .badge { padding:7px 18px; border-radius:20px; font-size:.85rem; font-weight:600; }
        .b1{background:#1e3a5f;color:#7ec8e3} .b2{background:#2d1b4e;color:#c084fc} .b3{background:#1a3c2a;color:#6ee7b7}
        .arrow{color:#444;font-size:1.1rem}

        .bar-wrap {
            position:absolute; bottom:70px; width:220px; height:3px;
            background:#1a1a2e; border-radius:3px; overflow:hidden;
            opacity:0; animation:fadeUp .5s ease 1.8s forwards;
        }
        .bar-fill {
            height:100%; width:0%; background:linear-gradient(90deg,#FF6B35,#F7C948);
            border-radius:3px; animation:fillBar 3.8s ease-in-out 2s forwards;
        }
        @keyframes fillBar { to{width:100%} }

        .bar-label {
            position:absolute; bottom:44px; color:#444; font-size:.72rem;
            letter-spacing:3px; text-transform:uppercase;
            opacity:0; animation:fadeUp .5s ease 1.8s forwards;
        }
    </style>
    </head>
    <body>
        <div class="splash">
            <div class="particles"></div>
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
            <div class="logo">🔥</div>
            <div class="title">FireReach</div>
            <div class="subtitle">Autonomous AI Outreach</div>
            <div class="pipeline">
                <span class="badge b1">🔍 Signal</span>
                <span class="arrow">→</span>
                <span class="badge b2">🧠 Insight</span>
                <span class="arrow">→</span>
                <span class="badge b3">✉️ Email</span>
            </div>
            <div class="bar-wrap"><div class="bar-fill"></div></div>
            <div class="bar-label">Initializing Agent</div>
        </div>
    </body>
    </html>
    """

    components.html(splash_html, height=700, scrolling=False)

    import time
    time.sleep(6)
    st.session_state.splash_done = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN AGENT WORKSPACE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Hide default chrome */
    #MainMenu, footer { display: none !important; }

    /* Force all text to our font */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Force dark background ──────────────────────── */
    .stApp {
        background: linear-gradient(145deg, #0a0a0f 0%, #0f0f1a 50%, #0a0f14 100%) !important;
    }

    /* ── Header ─────────────────────────────────────── */
    .fr-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem;
    }
    .fr-header h1 {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35, #F7C948);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -1px;
    }
    .fr-header .sub {
        color: #666;
        font-size: 0.95rem;
        font-weight: 300;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* ── Pipeline bar ──────────────────────────────── */
    .pipeline-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin: 1.2rem auto;
        padding: 14px 24px;
        border-radius: 16px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        max-width: 600px;
    }
    .pip-step {
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .pip-step.harvest  { background: #1e3a5f; color: #7ec8e3; }
    .pip-step.research { background: #2d1b4e; color: #c084fc; }
    .pip-step.email    { background: #1a3c2a; color: #6ee7b7; }
    .pip-arrow { color: #444; font-size: 1rem; }

    /* ── FORCE INPUTS VISIBLE ──────────────────────── */
    input, textarea,
    .stTextInput input,
    .stTextArea textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #141420 !important;
        color: #f0f0f0 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        caret-color: #FF6B35 !important;
        -webkit-text-fill-color: #f0f0f0 !important;
    }
    input:focus, textarea:focus,
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #FF6B35 !important;
        box-shadow: 0 0 0 3px rgba(255,107,53,0.2) !important;
        outline: none !important;
    }
    input::placeholder, textarea::placeholder {
        color: #666 !important;
        -webkit-text-fill-color: #666 !important;
        opacity: 1 !important;
    }

    /* Labels */
    .stTextInput label, .stTextArea label,
    [data-testid="stTextInput"] label,
    [data-testid="stTextArea"] label {
        color: #ccc !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* ── Launch button ──────────────────────────────── */
    .stButton > button,
    button[kind="primary"],
    [data-testid="stButton"] > button {
        width: 100% !important;
        padding: 0.85rem 0 !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #FF6B35, #F7C948) !important;
        color: #0a0a0f !important;
        border: none !important;
        cursor: pointer !important;
        letter-spacing: 0.5px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    .stButton > button:hover,
    [data-testid="stButton"] > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 40px rgba(255, 107, 53, 0.35) !important;
        color: #0a0a0f !important;
        background: linear-gradient(135deg, #FF6B35, #F7C948) !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    /* ── Glassmorphism cards ─────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 16px;
        transition: border-color 0.3s, box-shadow 0.3s;
    }
    .glass-card:hover {
        border-color: rgba(255, 107, 53, 0.15);
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.06);
    }
    .card-icon { font-size: 1.5rem; margin-right: 10px; }
    .card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #e0e0e0;
        display: inline;
    }
    .card-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 10px;
        vertical-align: middle;
    }
    .badge-harvest  { background: #1e3a5f; color: #7ec8e3; }
    .badge-research { background: #2d1b4e; color: #c084fc; }
    .badge-email    { background: #1a3c2a; color: #6ee7b7; }
    .badge-status-ok  { background: #064e3b; color: #6ee7b7; }
    .badge-status-err { background: #4c1d1d; color: #fca5a5; }

    .card-body {
        color: #bbb;
        font-size: 0.92rem;
        line-height: 1.7;
        margin-top: 14px;
    }
    .signal-category {
        color: #ddd;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 14px;
        margin-bottom: 4px;
    }
    .signal-item {
        color: #999;
        font-size: 0.85rem;
        padding: 4px 0 4px 14px;
        border-left: 2px solid rgba(255,107,53,0.25);
        margin: 4px 0;
        line-height: 1.5;
    }

    /* ── Email preview ──────────────────────────────── */
    .email-preview {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 20px;
        margin-top: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #bbb;
        line-height: 1.7;
        white-space: pre-wrap;
    }
    .email-subject {
        color: #F7C948;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    /* ── Divider ────────────────────────────────────── */
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 1.5rem 0;
    }

    /* ── Alerts ─────────────────────────────────────── */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* ── Help tooltips ─────────────────────────────── */
    .stTooltipIcon { color: #666 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="fr-header">'
    "<h1>🔥 FireReach</h1>"
    '<div class="sub">Autonomous AI Outreach Agent</div>'
    "</div>",
    unsafe_allow_html=True,
)

# ── Pipeline visual ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="pipeline-bar">'
    '<span class="pip-step harvest">🔍 Signal Harvester</span>'
    '<span class="pip-arrow">→</span>'
    '<span class="pip-step research">🧠 Research Analyst</span>'
    '<span class="pip-arrow">→</span>'
    '<span class="pip-step email">✉️ Outreach Sender</span>'
    "</div>",
    unsafe_allow_html=True,
)

st.markdown("")   # spacer

# ── Input form ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    company_name = st.text_input(
        "🏢  Target Company",
        placeholder="e.g. Stripe",
    )
with col_right:
    target_email = st.text_input(
        "📧  Recipient Email",
        placeholder="e.g. founder@stripe.com",
    )

icp = st.text_area(
    "🎯  Ideal Customer Profile (ICP)",
    placeholder=(
        "e.g. We sell high-end cybersecurity training to Series B startups. "
        "Our ICP includes CISOs and engineering leaders at fast-growing tech companies."
    ),
    height=120,
)

st.markdown("")   # spacer
launch = st.button("🚀  Launch FireReach Agent")

# ═══════════════════════════════════════════════════════════════════════════════
#  EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════
if launch:
    if not company_name or not target_email or not icp:
        st.warning("⚠️  Please fill in all three fields before launching.")
        st.stop()

    status_ph = st.empty()

    def update_status(msg: str):
        status_ph.info(msg)

    with st.spinner("FireReach agent is working …"):
        result = run_agent(
            icp=icp,
            company_name=company_name,
            email=target_email,
            on_step=update_status,
        )

    status_ph.success("✅  Agent pipeline complete — all 3 tools executed!")
    st.session_state.result = result

# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS — Native Streamlit expanders for reliable display
# ═══════════════════════════════════════════════════════════════════════════════
result = st.session_state.result

if result:
    st.markdown("---")

    # ── Step 1: Discovered Signals ────────────────────────────────────────
    with st.expander("🔍  **Step 1 — Discovered Signals**  `TOOL: signal_harvester`", expanded=True):
        signals = result.get("signals", {})
        if signals:
            for category, items in signals.items():
                nice_name = category.replace("_", " ").title()
                st.markdown(f"**📌 {nice_name}**")
                if isinstance(items, list):
                    for item in items:
                        st.markdown(f"- {item}")
                else:
                    st.markdown(f"- {items}")
                st.markdown("")  # spacer between categories
        else:
            st.info("No signals were discovered.")

    # ── Step 2: Account Brief ─────────────────────────────────────────────
    with st.expander("🧠  **Step 2 — Account Brief**  `TOOL: research_analyst`", expanded=True):
        brief = result.get("account_brief", "")
        if brief:
            st.markdown(brief)
        else:
            st.info("No account brief was generated.")

    # ── Step 3: Generated Email ───────────────────────────────────────────
    with st.expander("✉️  **Step 3 — Generated Email**  `TOOL: outreach_automated_sender`", expanded=True):
        email_subject = result.get("email_subject", "N/A")
        email_body = result.get("email_body", "No email generated.")

        st.markdown(f"**Subject:** {email_subject}")
        st.divider()
        st.markdown(email_body)

    # ── Email Status ──────────────────────────────────────────────────────
    with st.expander("📬  **Email Delivery Status**", expanded=True):
        email_status = result.get("email_status", {})
        is_success = email_status.get("success", False)
        status_msg = email_status.get("message", "Unknown status")

        if is_success:
            st.success(f"✅ {status_msg}")
        else:
            st.error(f"⚠️ {status_msg}")
