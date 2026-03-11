"""
agent.py – Orchestration layer for the FireReach agentic pipeline.

Runs the three tools in strict sequential order:
    Signal Harvesting  →  Research Analysis  →  Automated Outreach
"""

from tools import (
    tool_signal_harvester,
    tool_research_analyst,
    tool_outreach_automated_sender,
)


def run_agent(icp: str, company_name: str, email: str, on_step=None) -> dict:
    """
    Execute the FireReach three-step pipeline.

    Args:
        icp:          Ideal Customer Profile text.
        company_name: Target company to research.
        email:        Recipient email address.
        on_step:      Optional callback ``fn(step_name: str)`` invoked before
                      each tool call so the UI can show progress.

    Returns:
        {
            "signals":       dict   – raw signal data,
            "account_brief": str    – two-paragraph brief,
            "email_subject": str    – generated subject line,
            "email_body":    str    – generated email body,
            "email_status":  dict   – {"success": bool, "message": str},
        }
    """
    result: dict = {}

    # ── Step 1 – Signal Harvesting ────────────────────────────────────────
    if on_step:
        on_step("🔍 Step 1/3 — Harvesting company signals …")
    signals = tool_signal_harvester(company_name)
    result["signals"] = signals

    # ── Step 2 – Research Analysis ────────────────────────────────────────
    if on_step:
        on_step("🧠 Step 2/3 — Analyzing signals & generating account brief …")
    account_brief = tool_research_analyst(signals, icp)
    result["account_brief"] = account_brief

    # ── Step 3 – Automated Outreach ───────────────────────────────────────
    if on_step:
        on_step("✉️ Step 3/3 — Generating & sending outreach email …")
    outreach = tool_outreach_automated_sender(account_brief, email, icp)
    result["email_subject"] = outreach["email_subject"]
    result["email_body"] = outreach["email_body"]
    result["email_status"] = outreach["send_status"]

    return result
