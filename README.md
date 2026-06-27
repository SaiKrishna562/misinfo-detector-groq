<div align="center">

# 🕵️ FactTrace — AI Misinformation Detector

**Paste any claim, news snippet, or viral statement and get a sourced, scored fact-check in seconds — powered by Groq's Llama 3.3 70B and live web search.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Llama%203.3%2070B-F55036)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📖 Overview

**FactTrace** is an AI-powered fact-checking agent. Drop in a claim, a viral social media post, or a chunk of news text, and it will:

1. Break it down into individual, verifiable sub-claims
2. Search live web sources for each one (Tavily + DuckDuckGo)
3. Score each claim's credibility (0–100) with a verdict, reasoning, key finding, and bias flags
4. Visualize how each source relates to the claim in an interactive lineage graph

It's built to catch the kind of misinformation that spreads fastest — confidently-worded myths, misleading headlines, and half-true viral claims — and show its work rather than just giving a verdict.

> ⚠️ **Disclaimer:** This is an AI-assisted research/educational tool, not a definitive source of truth. Always cross-check important claims with primary sources and professional fact-checkers.

## ✨ Features

- 🔎 **Claim extraction** — splits any input into 2–4 specific, verifiable factual claims (preserving the original framing, not flipping or reinterpreting it)
- 🌐 **Live multi-source search** — pulls up to 8 deduplicated sources per claim from **Tavily** (primary) and **DuckDuckGo** (fallback), with domain-level dedup so one site can't dominate the results
- 📊 **Credibility scoring** — each claim gets a 0–100 score against a strict rubric, plus a verdict: `TRUE`, `FALSE`, `MISLEADING`, or `UNVERIFIED`
- 🚩 **Bias / framing flags** — flags patterns like cherry-picked data or misleading headlines
- 🕸️ **Claim lineage graph** — an interactive visual graph (green = supports, red = contradicts, gray = related) for each claim's sources, click any node to open the source
- 🗂️ **Session history** — sidebar tracks your last 10 analyses with verdict and average score
- 🎨 **Custom dark UI** — purpose-built Streamlit theme, not the default look

## 🛠️ Tech Stack

| Layer            | Technology                                              |
|-------------------|------------------------------------------------------------|
| UI                | [Streamlit](https://streamlit.io/)                         |
| LLM               | Llama 3.3 70B via [Groq](https://groq.com/) (OpenAI-compatible API) |
| Web search        | [Tavily](https://tavily.com/) (primary) + DuckDuckGo (fallback, no key required) |
| Graph visualization | [vis.js](https://visjs.org/) (rendered via `streamlit.components.v1`) |
| Language          | Python 3.10+                                                |

## 📂 Project Structure

```
misinfo-detector/
├── app.py                      # Streamlit UI — input, analysis flow, scoring display, history
├── agents/
│   ├── claim_extractor.py      # Groq/Llama: extract verifiable sub-claims from raw input
│   ├── searcher.py              # Tavily + DuckDuckGo: fetch & dedupe live sources per claim
│   ├── fact_analyser.py         # Groq/Llama: score + verdict + reasoning + bias flags
│   └── graph_builder.py         # Builds the vis.js claim lineage graph HTML
├── requirements.txt
├── .env.example                 # Template for your API keys (copy to .env)
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com/keys)
- A free [Tavily API key](https://tavily.com/) (1,000 searches/month on the free tier)

### Installation

```bash
# Clone the repository
git clone https://github.com/SaiKrishna562/misinfo-detector-groq.git
cd misinfo-detector-groq

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configure your API keys

```bash
cp .env.example .env
```

Then open `.env` and fill in your own keys:

```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

> **Never commit your real `.env` file.** It's already excluded via `.gitignore`.

### Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## 🧠 How It Works

1. **Input** — paste a claim, headline, or snippet of text into the text area.
2. **Claim extraction** (`agents/claim_extractor.py`) — Llama 3.3 70B (via Groq) extracts 2–4 distinct, verifiable claims from the input, preserving the original wording/direction so the system doesn't accidentally fact-check a strawman version of the claim.
3. **Source search** (`agents/searcher.py`) — each claim is searched via Tavily (advanced search depth, with answer synthesis) and DuckDuckGo as a free fallback; results are merged and deduplicated (max 2 sources per domain, up to 8 total).
4. **Credibility analysis** (`agents/fact_analyser.py`) — the claim and its sources are passed to Llama 3.3 70B with a strict scoring rubric, returning a verdict, a 0–100 score, reasoning, a one-line key finding, supporting/contradicting source URLs, and bias flags.
5. **Visualization** (`agents/graph_builder.py`) — sources are rendered as a clickable lineage graph around the claim node, colored by whether they support or contradict it.
6. **Summary** — once all claims are processed, an overall risk assessment (`VERIFIED` / `MISLEADING` / `HIGH RISK` / `UNVERIFIED`) and average credibility score are shown.

## 🎯 Credibility Score Rubric

| Score Range | Meaning                                  |
|-------------|--------------------------------------------|
| 85–100      | Multiple credible sources confirm           |
| 65–84       | Mostly supported, minor gaps                |
| 45–64       | Mixed or insufficient evidence              |
| 25–44       | Mostly contradicted / misleading            |
| 0–24        | Clearly false, debunked                     |

## 🧪 Demo Claims to Try

- "5G towers caused COVID-19 by weakening immune systems"
- "NASA confirmed the moon landing was filmed by Stanley Kubrick"
- "Drinking lemon water boosts metabolism by 40% and cures diabetes"

## 🗺️ Roadmap / Ideas

- [ ] Source credibility weighting (favor known fact-checking sites / primary sources)
- [ ] Export analysis as a shareable PDF/Markdown report
- [ ] Batch fact-checking for multiple claims/articles at once
- [ ] Caching repeated claim lookups to save API calls
- [ ] Support for additional LLM providers as alternatives to Groq

## 🤝 Contributing

Suggestions and pull requests are welcome — feel free to open an issue first to discuss what you'd like to change.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙋 Author

**Undinty Sai Krishna** 
