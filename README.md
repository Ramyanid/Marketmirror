# 🪞 MarketMirror

> **AI-powered competitive intelligence — from company name to prescriptive briefing in minutes.**

MarketMirror is a three-phase AI agent system built on [n8n](https://n8n.io) and surfaced through a Streamlit UI. Enter any company name and get back a full competitive landscape: who your rivals are, how they score across key dimensions, where the gaps are, and what to do about them.

---

## How it works

```
User Input
    │
    ▼
┌─────────────────────────────┐
│  Phase 1 · Discovery        │  Identifies the company, infers its industry,
│  (Webhook v2)               │  and finds up to 4 direct competitors via web search
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Phase 2 · Research         │  Deep-dives each competitor — pricing, features,
│                             │  digital presence, recent news, threat level
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│  Phase 3 · Synthesis        │  Scores each competitor across 6 dimensions,
│                             │  identifies gaps, and writes actionable recommendations
└────────────┬────────────────┘
             │
             ▼
     Streamlit UI (MarketMirror)
     — Radar chart  · Heatmap  · Competitor cards
     — Gaps & Recommendations  · Digital/Ecommerce gaps
```

---

## Features

| Feature | Description |
|---|---|
| 🔍 **Competitor Discovery** | Web-searched, not hallucinated — agent confirms what the company does before finding rivals |
| 📊 **Feature Heatmap** | 6-dimension scorecard (Pricing, Product Breadth, Innovation, Digital, Positioning, Support) |
| 🕸️ **Radar Chart** | Visual landscape showing relative strengths at a glance |
| 🃏 **Competitor Cards** | Threat level badge, positioning, pricing, digital presence per competitor |
| 🎯 **Gaps & Recommendations** | Prioritised (High / Medium / Low) with evidence and the competitor driving each gap |
| 🌐 **Digital / Ecommerce Gaps** | Separate section focused on online channel weaknesses |
| ✨ **Sample preview** | Landing page shows a live radar chart with sample data before you run anything |

---

## Project structure

```
MarketMirror/
├── discover_miagent_ui.py                              # Streamlit front-end
├── requirements.txt                                    # Python dependencies
├── .gitignore
│
├── Discover MIagent RN-version1 - Discovery Phase (Webhook v2).json
├── Discover MIagent-version1RN - Research Phase.json
└── Discover MIagent-version1 - Synthesis PhaseRN.json
```

---

## Quickstart

### 1. Clone & install

```bash
git clone https://github.com/Ramyanid/Marketmirror.git
cd Marketmirror
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up n8n

1. Import the three workflow JSON files into your n8n instance
2. Attach credentials to:
   - **Nebius Chat Model** node — OpenAI-compatible API key pointed at `https://api.studio.nebius.com/v1`
   - **Tavily Search** node — [Tavily API key](https://tavily.com)
3. Click **Publish** on all three workflows
4. Copy the **production webhook URL** from the Discovery Phase webhook node

### 3. Configure the webhook URL

Open `discover_miagent_ui.py` and update line 89:

```python
N8N_WEBHOOK = "https://your-n8n-instance.app.n8n.cloud/webhook/discover-miagent"
```

### 4. Run

```bash
streamlit run discover_miagent_ui.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## n8n Workflows

| File | Phase | Description |
|---|---|---|
| `Discovery Phase (Webhook v2)` | 1 — Discovery | Receives POST from UI, identifies company + industry, returns up to 4 competitors |
| `Research Phase` | 2 — Research | Deep-researches each competitor using Tavily web search |
| `Synthesis Phase` | 3 — Synthesis | Scores competitors, identifies gaps, writes structured briefing JSON |

The three workflows are chained — Discovery triggers Research, Research triggers Synthesis, and Synthesis responds to the original webhook call with the final briefing.

---

## Tech stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Charts | [Plotly](https://plotly.com/python/) |
| Orchestration | [n8n](https://n8n.io) |
| LLM | Qwen3-30B via [Nebius AI Studio](https://studio.nebius.com) |
| Web search | [Tavily](https://tavily.com) |

---

## Development vs production

| | Development | Production |
|---|---|---|
| Webhook URL | `…/webhook-test/discover-miagent` | `…/webhook/discover-miagent` |
| n8n trigger | Click **Listen for test event** before each submit | Workflows published and always-on |
| Timeout | 120 s | 300 s |

---

## Roadmap

- [ ] PDF / PowerPoint export of the briefing
- [ ] Multi-company batch mode
- [ ] Scheduled re-runs with change detection
- [ ] Slack / email delivery of briefings
- [ ] Google Sheets integration for review layer between Discovery and Research

---

*Built with n8n · Streamlit · Nebius AI · Tavily*
