"""
tools.py – The three agentic tools that power the FireReach pipeline.

    1. tool_signal_harvester   – Gathers company signals via web search
    2. tool_research_analyst   – Generates an account brief using the LLM
    3. tool_outreach_automated_sender – Writes and sends the outreach email

LLM backend: Groq API with Llama 3 (llama-3.3-70b-versatile)
"""

import os
import json
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from prompts import RESEARCH_ANALYST_PROMPT, EMAIL_WRITER_PROMPT
from email_service import send_email

load_dotenv()

# ── Configure Groq client ────────────────────────────────────────────────────
# _groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
_groq_client = Groq(api_key=GROQ_API_KEY)
_LLM_MODEL = "llama-3.3-70b-versatile"


def _llm_chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send a single-turn chat to Groq and return the text response."""
    response = _groq_client.chat.completions.create(
        model=_LLM_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content.strip()


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 1 – Signal Harvester
# ═══════════════════════════════════════════════════════════════════════════════

def tool_signal_harvester(company_name: str) -> dict:
    """
    Collect recent signals about *company_name*:
      • Funding rounds
      • Hiring trends
      • Leadership changes
      • Tech stack changes
      • Social media mentions

    Uses SerpAPI Google Search when SERPAPI_KEY is set; otherwise falls back to
    the Groq LLM to generate plausible research signals.

    Returns a structured dict of signal categories.
    """
    serpapi_key = os.getenv("SERPAPI_KEY")

    if serpapi_key:
        return _harvest_via_serpapi(company_name, serpapi_key)
    else:
        return _harvest_via_llm(company_name)


def _harvest_via_serpapi(company_name: str, api_key: str) -> dict:
    """Search Google via SerpAPI and categorise results into signal buckets."""
    categories = {
        "funding_rounds": f"{company_name} funding round investment 2024 2025",
        "hiring_trends": f"{company_name} hiring jobs expansion team growth",
        "leadership_changes": f"{company_name} new CEO CTO VP leadership appointment",
        "tech_stack_changes": f"{company_name} technology stack migration adoption",
        "social_media_mentions": f"{company_name} latest news announcement launch",
    }

    signals: dict[str, list[str]] = {}

    for category, query in categories.items():
        try:
            resp = requests.get(
                "https://serpapi.com/search.json",
                params={"q": query, "api_key": api_key, "num": 3},
                timeout=10,
            )
            data = resp.json()
            results = data.get("organic_results", [])
            signals[category] = [
                f"{r.get('title', '')} – {r.get('snippet', '')}"
                for r in results[:3]
            ]
        except Exception:
            signals[category] = [f"Could not retrieve {category} signals."]

    return signals


def _harvest_via_llm(company_name: str) -> dict:
    """Fallback: ask Groq / Llama 3 to generate realistic company signals."""
    prompt = f"""
For the company "{company_name}", generate realistic and plausible recent
signals in the following categories. Return ONLY valid JSON (no markdown
fences, no extra text) with these keys:
  funding_rounds, hiring_trends, leadership_changes,
  tech_stack_changes, social_media_mentions

Each key should map to a list of 2-3 short signal strings.
"""
    try:
        text = _llm_chat(
            prompt,
            system="You are a market-intelligence researcher. Return only valid JSON.",
        )
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        signals = json.loads(text.strip())
        return signals
    except Exception as exc:
        return {
            "funding_rounds": [f"Unable to retrieve signals: {exc}"],
            "hiring_trends": [],
            "leadership_changes": [],
            "tech_stack_changes": [],
            "social_media_mentions": [],
        }


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 2 – Research Analyst
# ═══════════════════════════════════════════════════════════════════════════════

def tool_research_analyst(signals: dict, icp: str) -> str:
    """
    Analyse harvested *signals* against the *icp* and produce a two-paragraph
    account brief via the Groq LLM.

    Returns the account brief as a plain string.
    """
    signals_text = json.dumps(signals, indent=2)
    prompt = RESEARCH_ANALYST_PROMPT.format(signals=signals_text, icp=icp)

    try:
        return _llm_chat(prompt, system="You are a senior B2B research analyst.")
    except Exception as exc:
        return f"[Research Analyst Error] {exc}"


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 3 – Outreach Automated Sender
# ═══════════════════════════════════════════════════════════════════════════════

def tool_outreach_automated_sender(account_brief: str, email: str, icp: str = "") -> dict:
    """
    Generate a hyper-personalised outreach email using the *account_brief* and
    then send it to *email* via the email service.

    Returns:
        {
            "email_subject": str,
            "email_body": str,
            "send_status": {"success": bool, "message": str}
        }
    """
    # ── Generate the email body ───────────────────────────────────────────
    prompt = EMAIL_WRITER_PROMPT.format(account_brief=account_brief, icp=icp)

    try:
        email_body = _llm_chat(prompt, system="You are an elite cold-email copywriter.")
    except Exception as exc:
        email_body = f"[Email Generation Error] {exc}"

    # ── Build subject line via LLM ────────────────────────────────────────
    try:
        subject_prompt = (
            f"Write a single short email subject line (max 8 words) for this "
            f"cold outreach email. Return ONLY the subject line, nothing else.\n\n"
            f"Email body:\n{email_body}"
        )
        subject = _llm_chat(subject_prompt, system="Return only a subject line.")
        subject = subject.strip('"').strip("'")
    except Exception:
        subject = "Quick question for your team"

    # ── Send the email ────────────────────────────────────────────────────
    send_status = send_email(to=email, subject=subject, body=email_body)

    return {
        "email_subject": subject,
        "email_body": email_body,
        "send_status": send_status,
    }
