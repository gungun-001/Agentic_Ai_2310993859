"""
tools.py – Agentic tools for the FireReach V2 pipeline.

    1. tool_lead_generator         – Generates target companies from ICP
    2. tool_signal_harvester       – Gathers company signals via web search
    3. tool_contact_finder         – Finds decision-maker contact info
    4. tool_research_analyst       – Generates a strategic account brief
    5. tool_email_generator        – Writes personalized cold email (no send)
    6. tool_send_email             – Sends a single email via SMTP

LLM backend: Groq API with Llama 3 (llama-3.3-70b-versatile)
"""

import os
import json
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from prompts import (
    LEAD_GENERATION_PROMPT,
    CONTACT_FINDER_PROMPT,
    RESEARCH_ANALYST_PROMPT,
    EMAIL_WRITER_PROMPT,
)
from email_service import send_email

load_dotenv()

# ── Configure Groq client ────────────────────────────────────────────────────
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
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
        max_tokens=2000,
    )
    return response.choices[0].message.content.strip()


def _parse_json(text: str):
    """Strip markdown fences and parse JSON from LLM output."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    return json.loads(text.strip())


def is_valid_email(email: str) -> bool:
    """Basic regex-based email validation."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def _extract_emails_from_text(text: str) -> list:
    """Extract all email addresses from a string."""
    import re
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 1 – Lead Generator
# ═══════════════════════════════════════════════════════════════════════════════

def tool_lead_generator(icp: str) -> list:
    """
    Generate a list of target companies based on the ICP.

    Returns a list of dicts: [{"name": str, "domain": str, "reason": str}, ...]
    """
    prompt = LEAD_GENERATION_PROMPT.format(icp=icp)
    try:
        text = _llm_chat(prompt, system="You are a B2B sales strategist. Return only valid JSON.")
        leads = _parse_json(text)
        if isinstance(leads, list):
            return leads
        return []
    except Exception as exc:
        return [{"name": "Error", "domain": "", "reason": f"Lead generation failed: {exc}"}]


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 2 – Signal Harvester
# ═══════════════════════════════════════════════════════════════════════════════

def tool_signal_harvester(company_name: str) -> dict:
    """
    Collect recent signals about *company_name*.
    Uses SerpAPI when available; otherwise falls back to LLM.
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
    """Fallback: ask LLM to generate realistic company signals."""
    prompt = f"""
For the company "{company_name}", generate realistic and plausible recent
signals in the following categories. Return ONLY valid JSON (no markdown
fences, no extra text) with these keys:
  funding_rounds, hiring_trends, leadership_changes,
  tech_stack_changes, social_media_mentions

Each key should map to a list of 2-3 short signal strings.
"""
    try:
        text = _llm_chat(prompt, system="You are a market-intelligence researcher. Return only valid JSON.")
        signals = _parse_json(text)
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
#  TOOL 3 – Contact Finder
# ═══════════════════════════════════════════════════════════════════════════════

def tool_contact_finder(company_name: str, domain: str, icp: str) -> dict:
    """
    Find the most likely decision-maker contact for a company.
    Uses: Hunter.io (if available) -> SerpAPI search -> LLM guess -> Generic fallback.
    """
    serpapi_key = os.getenv("SERPAPI_KEY")
    hunter_key = os.getenv("HUNTER_API_KEY")
    
    # --- Strategy 1: Hunter.io (Highly Reliable) ---
    if hunter_key:
        try:
            resp = requests.get(
                "https://api.hunter.io/v2/domain-search",
                params={"domain": domain, "api_key": hunter_key, "limit": 3},
                timeout=10
            )
            data = resp.json()
            emails = data.get("data", {}).get("emails", [])
            if emails:
                best = emails[0]
                return {
                    "name": f"{best.get('first_name', 'Team')} {best.get('last_name', '')}".strip(),
                    "role": best.get("position", "Professional"),
                    "email": best.get("value"),
                    "source": "Hunter.io"
                }
        except Exception:
            pass

    # --- Strategy 2: Web Search for actual emails ---
    if serpapi_key:
        try:
            query = f"{company_name} {domain} contact email"
            resp = requests.get(
                "https://serpapi.com/search.json",
                params={"q": query, "api_key": serpapi_key, "num": 5},
                timeout=10,
            )
            data = resp.json()
            snippets = " ".join([r.get("snippet", "") for r in data.get("organic_results", [])])
            found_emails = _extract_emails_from_text(snippets)
            
            # Filter for emails belonging to the domain
            valid_found = [e for e in found_emails if domain in e.lower() and is_valid_email(e)]
            if valid_found:
                return {
                    "name": "Team",
                    "role": "Contact",
                    "email": valid_found[0],
                    "source": "SerpAPI Search"
                }
        except Exception:
            pass

    # --- Strategy 3: LLM attempt ---
    prompt = CONTACT_FINDER_PROMPT.format(
        company_name=company_name, domain=domain, icp=icp
    )
    try:
        text = _llm_chat(prompt, system="You are a B2B contact researcher. Return only valid JSON.")
        contact = _parse_json(text)
        email = contact.get("email", "").lower()
        if is_valid_email(email) and domain in email:
            return contact
    except Exception:
        pass

    # --- Strategy 4: Safe Fallbacks (tried in order) ---
    # contact@ failed for Glassdoor, so let's use a broader list
    fallbacks = [f"info@{domain}", f"hello@{domain}", f"support@{domain}", f"contact@{domain}"]
    
    return {
        "name": "Team",
        "role": "Decision Maker",
        "email": fallbacks[0], 
        "is_fallback": True,
        "source": "Fallback"
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 4 – Research Analyst
# ═══════════════════════════════════════════════════════════════════════════════

def tool_research_analyst(signals: dict, icp: str) -> str:
    """
    Analyse harvested signals against the ICP and produce a strategic brief.
    """
    signals_text = json.dumps(signals, indent=2)
    prompt = RESEARCH_ANALYST_PROMPT.format(signals=signals_text, icp=icp)
    try:
        return _llm_chat(prompt, system="You are a senior B2B research analyst.")
    except Exception as exc:
        return f"[Research Analyst Error] {exc}"


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 5 – Email Generator (draft only, no sending)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_email_generator(
    account_brief: str,
    contact_name: str,
    icp: str,
    sender_name: str = "Team",
    sender_designation: str = "",
) -> dict:
    """
    Generate a personalized cold email. Does NOT send it.

    Returns: {"email_subject": str, "email_body": str}
    """
    prompt = EMAIL_WRITER_PROMPT.format(
        account_brief=account_brief,
        contact_name=contact_name,
        icp=icp,
        sender_name=sender_name,
        sender_designation=sender_designation,
    )

    try:
        raw_output = _llm_chat(
            prompt,
            system="You are a startup founder writing a cold email. Be human, direct, and concise.",
        )
    except Exception as exc:
        raw_output = f"[Email Generation Error] {exc}"

    # ── Parse subject and body ────────────────────────────────────────────
    subject = "Quick question for your team"
    email_body = raw_output

    if "Subject:" in raw_output:
        parts = raw_output.split("Subject:", 1)
        after_subject = parts[1].strip()
        lines = after_subject.split("\n", 1)
        subject = lines[0].strip().strip('"').strip("'")
        email_body = lines[1].strip() if len(lines) > 1 else raw_output

    # Clean up any "Email:" label
    if email_body.startswith("Email:"):
        email_body = email_body[len("Email:"):].strip()

    return {
        "email_subject": subject,
        "email_body": email_body,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  TOOL 6 – Send Email (delivery only)
# ═══════════════════════════════════════════════════════════════════════════════

def tool_send_email(to: str, subject: str, body: str) -> dict:
    """
    Send an email via SMTP. Returns {"success": bool, "message": str}.
    """
    return send_email(to=to, subject=subject, body=body)
