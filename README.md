# 🔥 FireReach V2 — Autonomous AI Outreach Agent

**Lead Generation → Signal Harvesting → Contact Discovery → Research Analysis → Email Drafting → Automated Outreach**

FireReach V2 is a powerful agentic AI platform that automates the entire sales outreach funnel. It identifies target companies based on your ICP, researches recent business signals, finds key decision-makers, and generates hyper-personalized outreach — all powered by Llama 3.3.

---

## ✨ Features

- **End-to-End Agentic Pipeline** — 6 specialized tools working in orchestration.
- **Lead Generation** — Automatically identifies high-potential target companies matching your Ideal Customer Profile (ICP).
- **Signal Harvesting** — Monitors funding rounds, hiring trends, leadership changes, and tech stack moves via SerpAPI.
- **Contact Discovery** — Locates relevant decision-makers and their contact information.
- **Strategic Research** — LLM-powered account briefs linking company signals to your specific value proposition.
- **Hyper-Personalized Outreach** — Generates human-like, direct cold emails that reference real-time signals.
- **Premium Streamlit UI** — Dark-themed workspace with real-time pipeline status and human-in-the-loop review.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **UI** | Streamlit |
| **LLM** | Groq API (Llama 3.3 70B Versatile) |
| **Signal Source** | SerpAPI (Google Search) / LLM Fallback |
| **Email** | Python `smtplib` (SMTP) |
| **Orchestration** | Custom Agentic Workflow (Python) |

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI & Human-in-the-loop Workspace
├── agent.py            # Agent orchestration (FireReach V2 Pipeline)
├── tools.py            # Implementation of the 6 agentic tools
├── email_service.py    # SMTP email delivery service
├── prompts.py          # Structured system prompts for LLM
├── database.py         # Lead and signal persistence
├── DOCS.md             # Detailed architecture documentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── .streamlit/
    └── config.toml     # Streamlit theme configuration
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/gungun-001/Agentic_Ai_2310993859.git
cd Agentic_Ai_2310993859
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
GROQ_API_KEY=your-groq-api-key      # Required
SERPAPI_KEY=your-serpapi-key          # Optional (falls back to LLM)
SMTP_HOST=smtp.gmail.com             # Optional (for actual sending)
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🔄 Agent Pipeline (V2)

```
       [ User Input: ICP ]
               │
               ▼
    ┌──────────────────────┐
    │ 1. Lead Generator    │──▶ List of target companies
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 2. Signal Harvester  │──▶ Company-specific signals
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 3. Contact Finder    │──▶ Decision-maker info
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 4. Research Analyst  │──▶ Strategic account brief
    └──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ 5. Email Generator   │──▶ Personalized draft
    └──────────────────────┘
               │
      [ Human Review ] ── (Optional)
               │
               ▼
    ┌──────────────────────┐
    │ 6. Outreach Sender   │──▶ Sent status
    └──────────────────────┘
```

---

## 📄 License

This project is for educational and demonstration purposes.

