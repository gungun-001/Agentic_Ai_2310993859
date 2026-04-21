"""
agent.py – Orchestration layer for the FireReach V2 agentic pipeline.

New flow:
    Lead Generation → Signal Harvesting → Contact Discovery →
    Research Analysis → Email Drafting → (Human Review) → Send
"""

from tools import (
    tool_lead_generator,
    tool_signal_harvester,
    tool_contact_finder,
    tool_research_analyst,
    tool_email_generator,
    tool_send_email,
)


def generate_leads(icp: str, on_log=None) -> list:
    """
    Step 1: Generate target companies from ICP.

    Returns list of dicts: [{"name", "domain", "reason"}, ...]
    """
    if on_log:
        on_log("🔍 Generating target companies from your ICP …")
    leads = tool_lead_generator(icp)
    if on_log:
        on_log(f"✅ Found {len(leads)} potential targets")
    return leads


def process_company(
    company_name: str,
    domain: str,
    icp: str,
    sender_name: str = "Team",
    sender_designation: str = "",
    on_log=None,
) -> dict:
    """
    Run the full pipeline for a single company (no sending).

    Returns:
        {
            "company":       str,
            "signals":       dict,
            "contact":       {"name", "role", "email"},
            "account_brief": str,
            "email_subject": str,
            "email_body":    str,
        }
    """
    result = {"company": company_name}

    # ── Step 1: Signal Harvesting ─────────────────────────────────────────
    if on_log:
        on_log(f"🔍 [{company_name}] Harvesting signals …")
    signals = tool_signal_harvester(company_name)
    result["signals"] = signals

    # ── Step 2: Contact Discovery ─────────────────────────────────────────
    if on_log:
        on_log(f"👤 [{company_name}] Finding decision-maker …")
    contact = tool_contact_finder(company_name, domain, icp)
    result["contact"] = contact
    
    source = contact.get("source", "LLM")
    email = contact.get("email")
    if on_log:
        if contact.get("is_fallback"):
            on_log(f"⚠️ [{company_name}] Using fallback email: {email} (No specific contact found)")
        else:
            on_log(f"✅ [{company_name}] Found email via {source}: {email}")

    # ── Step 3: Research Analysis ─────────────────────────────────────────
    if on_log:
        on_log(f"🧠 [{company_name}] Generating strategic brief …")
    brief = tool_research_analyst(signals, icp)
    result["account_brief"] = brief

    # ── Step 4: Email Generation ──────────────────────────────────────────
    if on_log:
        on_log(f"✉️ [{company_name}] Drafting personalized email …")
    email_data = tool_email_generator(
        account_brief=brief,
        contact_name=contact.get("name", "there"),
        icp=icp,
        sender_name=sender_name,
        sender_designation=sender_designation,
    )
    result["email_subject"] = email_data["email_subject"]
    result["email_body"] = email_data["email_body"]

    if on_log:
        on_log(f"✅ [{company_name}] Draft ready for review")

    return result


def send_approved_emails(approved_leads: list, on_log=None) -> list:
    """
    Send emails for all approved leads.

    Args:
        approved_leads: list of dicts, each with keys:
            "contact" (dict with "email"), "email_subject", "email_body"

    Returns:
        list of dicts: [{"company", "email", "success", "message"}, ...]
    """
    results = []
    for lead in approved_leads:
        to_email = lead["contact"]["email"]
        subject = lead["email_subject"]
        body = lead["email_body"]
        company = lead.get("company", "Unknown")

        if on_log:
            on_log(f"📤 Sending to {to_email} ({company}) …")

        status = tool_send_email(to=to_email, subject=subject, body=body)
        results.append({
            "company": company,
            "email": to_email,
            "success": status.get("success", False),
            "message": status.get("message", "Unknown error"),
        })

        if on_log:
            icon = "✅" if status.get("success") else "❌"
            on_log(f"{icon} [{company}] {status.get('message', '')}")

    return results
