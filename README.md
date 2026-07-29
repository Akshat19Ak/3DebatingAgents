I# ⚖️ Multi-Agent Debate & Decision Intelligence System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/Framework-CrewAI-red.svg)](https://crewai.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Groq](https://img.shields.io/badge/Inference-Groq_LPU-orange.svg)](https://groq.com)

A production-grade **Agentic AI** framework designed to synthesize complex business decisions through adversarial reasoning. This system orchestrates multiple specialized AI agents to debate a topic from opposing viewpoints, delivering a balanced, metrics-backed executive verdict.

---

## 🌟 Key Features

-   **Adversarial Multi-Agent Architecture**: Leverages specialized "Visionary Optimist" and "Ruthless Risk Analyst" agents to eliminate binary bias.
-   **Executive Synthesis**: A Moderator agent that weighs conflicting analyses to provide a logical "Proceed/Abandon/Pivot" recommendation.
-   **High-Speed Inference**: Powered by **Groq LPU** technology using **Llama 3.3 70B**, achieving elite-level token-per-second performance.
-   **Deep Observability**: A custom-built metrics layer that tracks debate diversity, agent contribution influence, and consensus quality.
-   **Hybrid Interface**: Run the system via a professional **CLI** or a premium **Streamlit** web dashboard.
-   **Enterprise Ready**: Fully containerized with **Docker & Docker Compose** for one-command deployment.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Orchestration** | [CrewAI](https://github.com/joaomdmoura/crewai) |
| **LLM Inference** | [Groq](https://groq.com) (Llama-3.3-70b-versatile) |
| **Logic/Backend** | Python 3.11, [LiteLLM](https://github.com/BerriAI/litellm) |
| **Web Interface** | Streamlit (Custom CSS & Background Threading) |
| **Evaluation Layer** | Scikit-Learn (TF-IDF Similarity), TextBlob (Sentiment) |
| **Containerization** | Docker, Docker Compose |
| **Environment** | python-dotenv, Pydantic |

---

## 📊 Factual Performance Benchmarks

Based on a standard complex decision cycle (e.g., *"Should we replace our human team with AI chatbots?"*):

-   **Total Execution Latency**: `35.04 seconds`
-   **Total Tokens Processed**: `3,691 tokens`
-   **Consensus Quality Score**: `94.74 / 100`
-   **Agent Contribution Influence**: Balanced at `47.37% (Optimist)` vs `52.63% (Risk Analyst)`.
-   **Logical Consistency**: `100 / 100` (Adherence to structured output schema).
-   **Economic Efficiency**: `~$0.00369 USD` per comprehensive executive report.

---

## 🧬 System Architecture

### The Agents
1.  **🚀 Visionary Optimist**: Passionately argues for maximum benefits, ROI, and strategic advantages.
2.  **⚠️ Ruthless Risk Analyst**: Skeptically identifies every potential failure mode, operational danger, and hidden cost.
3.  **⚖️ Executive Moderator**: Reviews both reports and synthesizes a cohesive final decision.

### The Metrics Layer
The `src/metrics.py` module tracks:
-   **Debate Diversity**: Cosine similarity between opposing agents to ensure distinct viewpoints.
-   **Contribution Effect**: Quantifies how much each agent influenced the final moderator verdict.
-   **Sentiment Alignment**: Verifies that agents adhered to their assigned personas.

---

## 🚀 Getting Started

### 1. Prerequisites
- Docker Desktop (Recommended) **OR** Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 2. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_key_here
```

### 3. Run via Docker (Easiest)
```bash
docker-compose up --build
```
*Access the UI at: http://localhost:8501*

### 4. Run via Python (Manual)
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start CLI
python src/main.py

# Start Web UI
streamlit run src/app.py
```

---

## 📂 Project Structure

```text
3DebatingAgents/
├── src/
│   ├── agents.py       # Agent persona definitions
│   ├── tasks.py        # Task descriptions & context flows
│   ├── crew.py         # CrewAI assembly
│   ├── metrics.py      # Observability & Evaluation logic
│   ├── app.py          # Streamlit Web UI
│   └── main.py         # CLI Entry point
├── temp/
│   ├── resume.md       # High-impact resume showcase
│   ├── Docker_Tutorial.ipynb
│   └── metrics.ipynb   # Why metrics matter in Agentic AI
├── Dockerfile          # Optimized slim build
└── docker-compose.yml  # Orchestration config
```

---

## 📈 Future Roadmap
- [ ] **RAG Integration**: Grounding agent debates in external knowledge bases/PDFs.
- [ ] **Persistent Memory**: Allowing the crew to remember previous debate outcomes.
- [ ] **Historical Analytics Dashboard**: Tracking metric trends over time via PostgreSQL.

---
*Created as a demonstration of production-grade Agentic AI Design Patterns.*
