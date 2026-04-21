"""
app.py – Streamlit UI for FireReach: Autonomous AI Outreach Agent.

Features:
  • Animated full-screen splash page (5 seconds) with particle effects
  • Premium dark-themed agent workspace with glassmorphism cards
  • Live step-by-step progress indicators
"""

import streamlit as st
import streamlit.components.v1 as components
import time
from dotenv import load_dotenv

load_dotenv()

from agent import generate_leads, process_company, send_approved_emails  # noqa: E402
from database import create_user, authenticate_user

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
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"
# ── V2 Pipeline State ──
if "step" not in st.session_state:
    st.session_state.step = 1
if "leads" not in st.session_state:
    st.session_state.leads = []
if "selected_leads" not in st.session_state:
    st.session_state.selected_leads = []
if "drafts" not in st.session_state:
    st.session_state.drafts = []
if "send_results" not in st.session_state:
    st.session_state.send_results = []
if "trace_log" not in st.session_state:
    st.session_state.trace_log = []

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

    st.components.v1.html(splash_html, height=1000, scrolling=False)

    time.sleep(6)
    st.session_state.splash_done = True
    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  AUTHENTICATION UI
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.splash_done and not st.session_state.logged_in:
    # Inject CSS to hide regular Streamlit elements and show our modal
    st.markdown(
        """
        <style>
        /* Hide everything while auth is active */
        .stApp > header { display: none !important; }
        [data-testid="stHeader"] { display: none !important; }
        
        /* Blur the background content if it's already rendered */
        .main .block-container {
            filter: blur(20px);
            pointer-events: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Use a container for the modal to ensure it's rendered on top
    with st.container():
        # HTML structure for the modal
        st.markdown('<div class="auth-overlay">', unsafe_allow_html=True)
        st.markdown('<div class="auth-modal">', unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<div class="auth-logo">🔥</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Login to your account</div>', unsafe_allow_html=True)
            
            l_email = st.text_input("Email Address", key="modal_l_email")
            l_pass = st.text_input("Password", type="password", key="modal_l_pass")
            
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            if st.button("Sign In →", use_container_width=True, type="primary"):
                if l_email and l_pass:
                    success, user_info = authenticate_user(l_email, l_pass)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_info = user_info
                        st.success(f"Welcome back, {user_info['name']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                else:
                    st.warning("Required fields missing.")
            
            st.markdown('<div class="auth-switch-text">New to FireReach?</div>', unsafe_allow_html=True)
            if st.button("Create an account", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.rerun()

        else:
            st.markdown('<div class="auth-logo">✨</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-title">Get Started</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Join the elite outreach era</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                s_name = st.text_input("Full Name", placeholder="John Doe")
                s_email = st.text_input("Email", placeholder="john@example.com")
            with col2:
                s_company = st.text_input("Company", placeholder="Acme Inc")
                s_role = st.text_input("Role", placeholder="Founder")
            
            s_pass = st.text_input("Create Password", type="password")
            
            st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
            if st.button("Create Account →", use_container_width=True, type="primary"):
                if all([s_name, s_email, s_company, s_role, s_pass]):
                    if len(s_pass) < 6:
                        st.error("Password too short.")
                    else:
                        success, msg = create_user(s_name, s_email, s_company, s_role, s_pass)
                        if success:
                            st.success(f"✨ {msg} Logging you in...")
                            # Auto-login after account creation
                            _, user_info = authenticate_user(s_email, s_pass)
                            st.session_state.logged_in = True
                            st.session_state.user_info = user_info
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(msg)
                else:
                    st.warning("All fields are required.")
            
            st.markdown('<div class="auth-switch-text">Already have an account?</div>', unsafe_allow_html=True)
            if st.button("Sign in instead", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.stop()


# ===============================================================================
#  MAIN AGENT WORKSPACE
# ===============================================================================

# Helper
def add_log(msg):
    st.session_state.trace_log.append(f"{msg}")

# ── CSS ──
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
#MainMenu, footer { display: none !important; }
html, body, [class*="css"], .stMarkdown, p, span, label, div { font-family: 'Inter', sans-serif !important; }
.stApp { background: #0d0d0d !important; }

/* Header */
.fr-hdr { display: flex; align-items: center; gap: 12px; padding: 14px 0 8px; border-bottom: 1px solid #1a1a1a; margin-bottom: 16px; }
.fr-hdr .logo { color: #e8542f; font-size: 1.4rem; }
.fr-hdr .brand { font-size: 1.3rem; font-weight: 700; color: #fff; }
.fr-hdr .sep { color: #333; font-weight: 300; font-size: 1.3rem; margin: 0 4px; }
.fr-hdr .tag { color: #888; font-size: 1rem; font-weight: 400; }

/* Panel cards */
.panel { background: #141414; border: 1px solid #1e1e1e; border-radius: 12px; padding: 20px; margin-bottom: 14px; }
.panel-title { display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 0.95rem; color: #fff; margin-bottom: 14px; }
.panel-title .icon { color: #e8542f; font-size: 1rem; }
.panel-desc { color: #777; font-size: 0.82rem; margin-bottom: 16px; line-height: 1.5; }

/* Company row */
.company-row { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 8px; margin-bottom: 4px; transition: background 0.2s; }
.company-row:hover { background: #1a1a1a; }
.company-name { color: #e0e0e0; font-weight: 600; font-size: 0.9rem; }
.company-domain { color: #555; font-size: 0.75rem; }

/* Trace log */
.trace-log { background: #111; border: 1px solid #1a1a1a; border-radius: 10px; padding: 16px; max-height: 320px; overflow-y: auto; }
.trace-item { display: flex; align-items: flex-start; gap: 8px; padding: 4px 0; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; color: #888; }
.trace-dot { width: 8px; height: 8px; border-radius: 50%; background: #e8542f; margin-top: 4px; flex-shrink: 0; }
.trace-dot.done { background: #22c55e; }

/* Email card */
.email-card { background: #141414; border: 1px solid #1e1e1e; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
.email-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.email-company { font-weight: 700; font-size: 1rem; color: #fff; }
.email-contact { color: #666; font-size: 0.82rem; }
.email-body-box { background: #0d0d0d; border: 1px solid #1e1e1e; border-radius: 10px; padding: 20px; margin-top: 10px; color: #bbb; font-size: 0.88rem; line-height: 1.75; white-space: pre-wrap; }
.email-subject-line { color: #e0e0e0; font-weight: 600; font-size: 0.95rem; margin-bottom: 8px; }

/* Buttons */
.stButton > button { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; border-radius: 10px !important; padding: 0.65rem 0 !important; font-size: 0.9rem !important; transition: all 0.2s !important; }
.primary-btn > button { background: #e8542f !important; color: #fff !important; border: none !important; }
.primary-btn > button:hover { background: #d44520 !important; transform: translateY(-1px) !important; box-shadow: 0 4px 20px rgba(232,84,47,0.3) !important; }
.secondary-btn > button { background: transparent !important; color: #999 !important; border: 1px solid #333 !important; }
.secondary-btn > button:hover { border-color: #555 !important; color: #ccc !important; }

/* Inputs */
input, textarea, .stTextInput input, .stTextArea textarea { background: #141414 !important; color: #e0e0e0 !important; border: 1px solid #2a2a2a !important; border-radius: 10px !important; font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; caret-color: #e8542f !important; -webkit-text-fill-color: #e0e0e0 !important; }
input:focus, textarea:focus { border-color: #e8542f !important; box-shadow: 0 0 0 2px rgba(232,84,47,0.15) !important; }
input::placeholder, textarea::placeholder { color: #555 !important; -webkit-text-fill-color: #555 !important; }
.stTextInput label, .stTextArea label { color: #999 !important; font-weight: 500 !important; font-size: 0.82rem !important; }

/* Metrics */
.metric-box { background: #141414; border: 1px solid #1e1e1e; border-radius: 12px; padding: 16px; text-align: center; }
.metric-val { font-size: 2rem; font-weight: 800; color: #fff; }
.metric-lbl { color: #666; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 4px; }

/* Misc */
hr { border: none; border-top: 1px solid #1a1a1a; margin: 1rem 0; }
div[data-testid="stAlert"] { border-radius: 10px !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stExpander"] { border: 1px solid #1e1e1e !important; border-radius: 10px !important; background: #111 !important; }

/* Auth styles (preserved) */
.auth-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,10,0.7); backdrop-filter: blur(12px); z-index: 99999; display: flex; align-items: center; justify-content: center; }
.auth-modal { width: 100%; max-width: 440px; background: rgba(20,20,20,0.95); backdrop-filter: blur(30px); border: 1px solid #2a2a2a; border-radius: 20px; padding: 40px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); animation: modalIn 0.35s ease; }
@keyframes modalIn { from { opacity: 0; transform: scale(0.95) translateY(15px); } to { opacity: 1; transform: none; } }
.auth-logo { font-size: 2.5rem; margin-bottom: 8px; text-align: center; }
.auth-title { font-size: 1.8rem; font-weight: 800; color: #e8542f; text-align: center; }
.auth-subtitle { color: #666; font-size: 0.8rem; text-align: center; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 2px; }
.auth-switch-text { text-align: center; margin-top: 20px; color: #555; font-size: 0.82rem; }
</style>""", unsafe_allow_html=True)

# ── Header ──
user_name = st.session_state.user_info["name"] if st.session_state.user_info else "User"
st.markdown(f'<div class="fr-hdr"><span class="logo">✦</span><span class="brand">FireReach</span><span class="sep">|</span><span class="tag">HITL Outreach</span></div>', unsafe_allow_html=True)

cs = st.session_state.step

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — ICP INPUT
# ═══════════════════════════════════════════════════════════════════════════════
if cs == 1:
    left, right = st.columns([1, 2])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">🎯</span> Define Your ICP</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-desc">Describe your ideal customer. Our agent will find matching companies automatically.</div>', unsafe_allow_html=True)
        icp = st.text_area("Ideal Customer Profile", placeholder="e.g. We sell AI-powered workflow automation tools to Series A-C SaaS startups with distributed teams. Our ICP includes CTOs, Heads of Ops, and Founders.", height=160, label_visibility="collapsed")
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        launch = st.button("🔍 Generate Leads", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Logout
        st.markdown("")
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">✦</span> How It Works</div>', unsafe_allow_html=True)
        st.markdown("""
<div style="color:#888; font-size:0.85rem; line-height:1.8;">
<b style="color:#e8542f;">1.</b> Enter your ICP → Agent finds matching companies<br/>
<b style="color:#e8542f;">2.</b> Select targets → Agent researches each company<br/>
<b style="color:#e8542f;">3.</b> Review AI-drafted emails → Approve or edit<br/>
<b style="color:#e8542f;">4.</b> Finalize sender details → Send approved emails<br/>
<b style="color:#e8542f;">5.</b> View delivery dashboard with metrics
</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if launch:
        if not icp:
            st.warning("Please describe your ICP first.")
        else:
            with st.spinner("🔍 Finding matching companies …"):
                add_log("Lead Generation Started")
                leads = generate_leads(icp, on_log=add_log)
                st.session_state.leads = leads
                st.session_state.icp = icp
                st.session_state.step = 2
                add_log(f"Generated {len(leads)} companies via LLM Search")
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — SELECT TARGETS
# ═══════════════════════════════════════════════════════════════════════════════
elif cs == 2:
    left, right = st.columns([1, 2])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">☑</span> Select Targets</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-desc">The agent found these companies. Select which ones to draft outreach for:</div>', unsafe_allow_html=True)

        # Custom company input
        cc1, cc2 = st.columns([3, 1])
        with cc1:
            custom_name = st.text_input(
                "Company Name",
                placeholder="Or add a custom company name",
                label_visibility="collapsed",
                key="cn"
            )
        with cc2:
            add_custom = st.button("+ Add")

        leads = list(st.session_state.leads)
        if add_custom and custom_name:
            leads.append({"name": custom_name, "domain": f"{custom_name.lower().replace(' ','')}.com", "reason": "Manually added"})
            st.session_state.leads = leads
            st.rerun()

        sels = {}
        for i, lead in enumerate(leads):
            sels[i] = st.checkbox(lead.get("name", "Unknown"), key=f"lead_{i}", value=False)

        st.markdown("", unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        confirm = st.button("▶ Confirm Targets & Draft", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">✦</span> Agent Reasoning Trace</div>', unsafe_allow_html=True)
        trace_html = '<div class="trace-log">'
        for log in st.session_state.trace_log:
            trace_html += f'<div class="trace-item"><span class="trace-dot done"></span>{log}</div>'
        trace_html += '</div>'
        st.markdown(trace_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if confirm:
        sel = [leads[i] for i, s in sels.items() if s]
        if not sel:
            st.warning("Select at least one company.")
        else:
            st.session_state.selected_leads = sel
            st.session_state.step = 3
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — AGENT PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
elif cs == 3:
    sel = st.session_state.selected_leads
    icp = st.session_state.get("icp", "")
    ui = st.session_state.user_info or {}

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title"><span class="icon">⚡</span> Agent Pipeline Running</div>', unsafe_allow_html=True)
    prog = st.progress(0)
    status = st.empty()
    drafts = []
    for idx, lead in enumerate(sel):
        co = lead.get("name",""); dom = lead.get("domain","")
        status.info(f"Processing **{co}** ({idx+1}/{len(sel)}) …")
        add_log(f"Processing company: {co}")
        try:
            r = process_company(co, dom, icp, ui.get("name","Team"), ui.get("role",""), on_log=add_log)
            drafts.append(r)
        except Exception as e:
            add_log(f"Error processing {co}: {e}")
            drafts.append({"company": co, "error": str(e)})
        prog.progress((idx+1)/len(sel))
    status.success(f"✅ All {len(sel)} companies processed!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.drafts = drafts
    st.session_state.step = 4
    time.sleep(1.5)
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — REVIEW EMAILS
# ═══════════════════════════════════════════════════════════════════════════════
elif cs == 4:
    left, right = st.columns([1, 2])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">👁</span> Approve Drafts</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-desc">Review the agent\'s personalized outreach drafts below. Check the ones you approve for sending.</div>', unsafe_allow_html=True)
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        send_btn = st.button("📤 Send Approved Emails", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Trace
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">✦</span> Agent Reasoning Trace</div>', unsafe_allow_html=True)
        trace_html = '<div class="trace-log">'
        for log in st.session_state.trace_log:
            trace_html += f'<div class="trace-item"><span class="trace-dot done"></span>{log}</div>'
        trace_html += '</div>'
        st.markdown(trace_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel-title" style="margin-bottom:14px;"><span class="icon">📄</span> Generated Emails</div>', unsafe_allow_html=True)
        drafts = st.session_state.drafts
        approvals = {}
        for i, d in enumerate(drafts):
            if "error" in d:
                st.error(f"❌ {d['company']}: {d['error']}")
                continue
            co = d.get("company",""); ct = d.get("contact",{})
            subj = d.get("email_subject",""); body = d.get("email_body","")

            st.markdown(f'<div class="email-card">', unsafe_allow_html=True)
            hdr1, hdr2 = st.columns([3, 1])
            with hdr1:
                st.markdown(f"**{co}** ({ct.get('email','N/A')})")
            with hdr2:
                approvals[i] = st.checkbox("☑ Approve Delivery", key=f"ap_{i}", value=True)

            with st.expander(f"▶ View Strategic Brief"):
                st.markdown(d.get("account_brief","No brief available."))

            st.markdown(f'<div class="email-body-box"><div class="email-subject-line">Subject: {subj}</div>\n{body}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.drafts = drafts

    if send_btn:
        approved = [drafts[i] for i, ok in approvals.items() if ok]
        if not approved:
            st.warning("No emails approved.")
        else:
            st.session_state.approved_drafts = approved
            st.session_state.step = 5
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — FINALIZE & SEND
# ═══════════════════════════════════════════════════════════════════════════════
elif cs == 5:
    left, right = st.columns([1, 2])
    ui = st.session_state.user_info or {}
    approved = st.session_state.get("approved_drafts", [])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">📝</span> Sender Details</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="panel-desc">Please enter your details to replace the placeholder fields in the approved emails before broadcasting.</div>', unsafe_allow_html=True)

        sn = st.text_input("Your Name", value=ui.get("name",""), placeholder="e.g. John Doe", key="fn")
        sd = st.text_input("Designation / Title", value=ui.get("role",""), placeholder="e.g. Founder & CEO", key="fd")
        se = st.text_input("Contact Info", value=ui.get("email",""), placeholder="e.g. john@company.com", key="fe")

        b1, b2 = st.columns(2)
        with b1:
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("Cancel", use_container_width=True): st.session_state.step = 4; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with b2:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            do_send = st.button("Finalize & Send", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        # Show trace
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title"><span class="icon">✦</span> Agent Reasoning Trace</div>', unsafe_allow_html=True)
        trace_html = '<div class="trace-log">'
        for log in st.session_state.trace_log:
            trace_html += f'<div class="trace-item"><span class="trace-dot done"></span>{log}</div>'
        trace_html += '</div>'
        st.markdown(trace_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if do_send:
        if not sn:
            st.warning("Enter your name."); st.stop()
        for d in approved:
            body = d.get("email_body","")
            body = body.replace("[Your Name]", sn).replace("[Name]", sn).replace("Team,", f"{sn},")
            d["email_body"] = body
        add_log("Email delivery started")
        with st.spinner("📤 Sending …"):
            results = send_approved_emails(approved, on_log=add_log)
        st.session_state.send_results = results
        st.session_state.step = 6
        add_log("Delivery completed")
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 6 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
elif cs == 6:
    left, right = st.columns([1, 2])
    res = st.session_state.send_results
    total = len(st.session_state.get("selected_leads",[])); appr = len(st.session_state.get("approved_drafts",[]))
    ok = sum(1 for r in res if r.get("success")); fail = sum(1 for r in res if not r.get("success"))

    with left:
        st.markdown('<div class="panel" style="text-align:center;">', unsafe_allow_html=True)
        icon_color = "#22c55e" if ok > 0 else "#e8542f"
        st.markdown(f'<div style="font-size:3rem; margin-bottom:8px;">{"✅" if ok > 0 else "⚠️"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:1.2rem; font-weight:700; color:#fff; margin-bottom:4px;">Campaign Completed!</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#666; font-size:0.82rem;">Review your delivery metrics below.</div>', unsafe_allow_html=True)

        mc = st.columns(4)
        labels = ["Total Leads", "Approved", "Delivered", "Failed"]
        vals = [total, appr, ok, fail]
        colors = ["#fff", "#fff", "#22c55e", "#ef4444"]
        for c, l, v, clr in zip(mc, labels, vals, colors):
            with c:
                st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:{clr};">{v}</div><div class="metric-lbl">{l}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Start New Campaign", use_container_width=True):
            for k in ["step","leads","selected_leads","drafts","send_results","trace_log","approved_drafts","icp"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel-title" style="margin-bottom:14px;"><span class="icon">📄</span> Generated Emails</div>', unsafe_allow_html=True)
        for d in st.session_state.get("approved_drafts",[]):
            ct = d.get("contact",{})
            st.markdown(f'<div class="email-card">', unsafe_allow_html=True)
            st.markdown(f"**{d.get('company','')}** ({ct.get('email','N/A')})")
            with st.expander("▶ View Strategic Brief"):
                st.markdown(d.get("account_brief",""))
            body = d.get("email_body",""); subj = d.get("email_subject","")
            st.markdown(f'<div class="email-body-box"><div class="email-subject-line">Subject: {subj}</div>\n{body}</div>', unsafe_allow_html=True)

            # Delivery status
            for r in res:
                if r.get("company") == d.get("company"):
                    if r.get("success"):
                        st.success(f"✅ {r.get('message','Sent')}")
                    else:
                        st.error(f"❌ {r.get('message','Failed')}")
            st.markdown('</div>', unsafe_allow_html=True)
