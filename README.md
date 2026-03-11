# 🔥 FireReach — Autonomous AI Outreach Agent

**Signal Harvesting → Research Analysis → Automated Outreach**

FireReach is a lightweight agentic AI prototype that researches target companies, generates personalized insights, and sends cold outreach emails — all autonomously using a three-tool function-calling pipeline.

---

## ✨ Features

- **Agentic AI Architecture** — Three tools called in strict sequential order
- **Signal Harvesting** — Discovers funding rounds, hiring trends, leadership changes, tech stack moves, and social mentions
- **Research Analysis** — LLM-powered account brief linking company signals to your ICP
- **Automated Outreach** — Generates and sends hyper-personalized cold emails via SMTP
- **Animated Splash Page** — Premium dark-themed UI with particle effects and gradient animations
- **Live Pipeline Status** — Real-time progress indicators as each tool executes

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **UI** | Streamlit |
| **LLM** | Groq API (Llama 3.3 70B) |
| **Signal Source** | SerpAPI (Google Search) / LLM fallback |
| **Email** | Python smtplib (SMTP) |
| **Language** | Python 3.10+ |

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI (splash page + workspace)
├── agent.py            # Agent orchestration (sequential tool calls)
├── tools.py            # Three agentic tools
├── email_service.py    # SMTP email sending service
├── prompts.py          # System prompts for LLM
├── DOCS.md             # Architecture documentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── .streamlit/
    └── config.toml     # Streamlit dark theme config
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
SMTP_HOST=smtp.gmail.com             # Optional (for sending emails)
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

## 🔄 Agent Pipeline

```
User inputs: ICP + Company Name + Email
                    │
                    ▼
     ┌──────────────────────────┐
     │  🔍 tool_signal_harvester │ → Signals dict
     └──────────────────────────┘
                    │
                    ▼
     ┌──────────────────────────┐
     │  🧠 tool_research_analyst │ → Account brief
     └──────────────────────────┘
                    │
                    ▼
     ┌──────────────────────────────────┐
     │  ✉️ tool_outreach_automated_sender │ → Email + send status
     └──────────────────────────────────┘
                    │
                    ▼
          UI displays all results
```

---

## 🧰 Tool Schemas

### `tool_signal_harvester(company_name)`
Collects signals via SerpAPI or LLM fallback. Returns a dict with keys: `funding_rounds`, `hiring_trends`, `leadership_changes`, `tech_stack_changes`, `social_media_mentions`.

### `tool_research_analyst(signals, icp)`
Analyzes signals against the ICP using the LLM. Returns a two-paragraph account brief.

### `tool_outreach_automated_sender(account_brief, email, icp)`
Generates a personalized outreach email and sends it via SMTP. Returns subject, body, and send status.

---

## 📸 Screenshots

### Splash Page
Animated dark-themed splash with gradient orbs, particle grid, and loading bar.

### Agent Workspace
Premium dark UI with pipeline visualization, styled inputs, and gradient launch button.

### Pipeline Results
Expandable sections showing signals, account brief, generated email, and delivery status.

---

## 📄 License

This project is for educational and demonstration purposes.
