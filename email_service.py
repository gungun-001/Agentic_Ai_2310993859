"""
email_service.py – Thin wrapper around Python's smtplib for sending outreach
emails.  Reads SMTP credentials from environment variables.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send a plain-text email via SMTP.

    Required env vars:
        SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL

    Returns:
        {"success": True/False, "message": "..."}
    """
    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("SMTP_FROM_EMAIL")

    # ── Validate configuration ────────────────────────────────────────────
    missing = [
        name
        for name, val in [
            ("SMTP_HOST", host),
            ("SMTP_PORT", port),
            ("SMTP_USER", user),
            ("SMTP_PASSWORD", password),
            ("SMTP_FROM_EMAIL", from_email),
        ]
        if not val
    ]
    if missing:
        return {
            "success": False,
            "message": f"SMTP not configured – missing env var(s): {', '.join(missing)}. "
                       "Email was generated but not sent.",
        }

    # ── Build the message ─────────────────────────────────────────────────
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # ── Send ──────────────────────────────────────────────────────────────
    try:
        with smtplib.SMTP(host, int(port)) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(from_email, to, msg.as_string())
        return {"success": True, "message": f"Email sent successfully to {to}"}
    except Exception as exc:
        return {"success": False, "message": f"SMTP error: {exc}"}
