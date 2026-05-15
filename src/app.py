"""
app.py  –  Streamlit UI for the Multi-Agent Debate & Decision System
======================================================================
Run with:   streamlit run src/app.py
"""

import os
import sys
import io
import threading
import queue
import time
import streamlit as st
from dotenv import load_dotenv

# ── Make sure the project root is on the path so we can import `src.*`
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.crew import build_debate_crew
from src.metrics import DebateEvaluator

# ══════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be the very first Streamlit call)
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OmniView Debate System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  CUSTOM CSS  –  premium dark-mode look
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Global ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0d0d1a 0%, #111827 100%);
    color: #e2e8f0;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }

/* ── Headings ── */
h1 { background: linear-gradient(90deg, #818cf8, #38bdf8);
     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
     font-size: 2.4rem !important; font-weight: 800 !important; }
h2 { color: #818cf8 !important; }
h3 { color: #38bdf8 !important; }

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.5) !important;
}

/* ── Text area ── */
[data-testid="stTextArea"] textarea {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

/* ── Expanders (agent cards) ── */
[data-testid="stExpander"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem;
}
[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    font-size: 1.05rem !important;
}

/* ── Info / success / warning boxes ── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── Log box ── */
.log-box {
    background: #0f172a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    max-height: 340px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Badge chips ── */
.badge {
    display: inline-block;
    border-radius: 999px;
    padding: 3px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-right: 6px;
}
.badge-green  { background:#064e3b; color:#6ee7b7; }
.badge-purple { background:#3b0764; color:#e9d5ff; }
.badge-blue   { background:#1e3a5f; color:#93c5fd; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚖️ OmniView")
    st.markdown("---")

    # API Key status
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "")
    if api_key and api_key != "your_groq_api_key_here":
        st.markdown('<span class="badge badge-green">● API Key Connected</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge" style="background:#7f1d1d;color:#fca5a5;">✗ API Key Missing</span>', unsafe_allow_html=True)
        st.error("Groq API Key not found.")
        user_key = st.text_input("Enter Groq API Key:", type="password")
        if user_key:
            os.environ["GROQ_API_KEY"] = user_key
            api_key = user_key
            st.success("API Key loaded for this session!")

    st.markdown("---")
    st.markdown("### 🤖 The Agents")
    st.markdown("""
| Agent | Role |
|-------|------|
| 🚀 Optimist | Argues max benefits |
| ⚠️ Risk Analyst | Highlights all risks |
| ⚖️ Moderator | Synthesises & decides |
""")
    st.markdown("---")
    st.markdown("### 🛠 Tech Stack")
    st.markdown("""
<span class="badge badge-purple">CrewAI</span>
<span class="badge badge-blue">Groq LLaMA</span>
<span class="badge badge-green">Streamlit</span>
""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Platform Metrics")
    st.caption("OmniView evaluates debate diversity and ensures unbiased decisions via mathematical influence tracking.")
    st.markdown("---")
    st.caption("OmniView v2.0 SaaS Edition")


# ══════════════════════════════════════════════════════════════════════
#  SESSION STATE  –  persist results across re-runs
# ══════════════════════════════════════════════════════════════════════
defaults = {
    "running":         False,
    "logs":            [],
    "optimist_out":    None,
    "risk_out":        None,
    "final_decision":  None,
    "metrics_report":  None,
    "raw_metrics":     None,
    "error":           None,
    "last_topic":      "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════
#  STDOUT CAPTURE  –  pipe CrewAI's verbose prints into Streamlit
# ══════════════════════════════════════════════════════════════════════
class QueueWriter(io.TextIOBase):
    """A file-like object that forwards every write() into a queue."""
    def __init__(self, q: queue.Queue):
        self._q = q

    def write(self, text: str) -> int:
        if text.strip():            # skip blank-only lines
            self._q.put(text)
        return len(text)

    def flush(self):
        pass


def _run_crew_in_thread(decision_problem: str, log_queue: queue.Queue):
    """
    Run the CrewAI crew in a background thread.
    Redirects stdout so verbose logs land in `log_queue`.
    Puts a sentinel dict at the end with the results (or error).
    """
    original_stdout = sys.stdout
    sys.stdout = QueueWriter(log_queue)
    try:
        evaluator = DebateEvaluator(decision_problem)
        debate_crew = build_debate_crew(decision_problem)
        result      = debate_crew.kickoff()

        # ── Extract individual task outputs (from CrewAI's task list) ──
        tasks            = debate_crew.tasks
        optimist_output  = str(tasks[0].output) if tasks and tasks[0].output else "No output captured."
        risk_output      = str(tasks[1].output) if len(tasks) > 1 and tasks[1].output else "No output captured."
        final_decision   = str(result)
        
        raw_metrics = evaluator.evaluate(optimist_output, risk_output, final_decision)
        report = evaluator.get_formatted_report()

        log_queue.put({
            "type":           "done",
            "optimist_out":   optimist_output,
            "risk_out":       risk_output,
            "final_decision": final_decision,
            "metrics_report": report,
            "raw_metrics":    raw_metrics,
        })
    except Exception as exc:
        log_queue.put({"type": "error", "message": str(exc)})
    finally:
        sys.stdout = original_stdout


# ══════════════════════════════════════════════════════════════════════
#  MAIN PAGE
# ══════════════════════════════════════════════════════════════════════
st.markdown("# ⚖️ OmniView Multi-Agent Debate and Decision System")
st.markdown(
    "Enter any **business idea, strategic decision, or proposal** below. "
    "Three AI agents will debate it and deliver a **balanced executive verdict**."
)
st.markdown("---")

# ── Quick Actions ──────────────────────────────────────────────────
st.markdown("### ⚡ Quick Decision Templates (AI/ML & SWE)")
def set_topic(t):
    st.session_state.topic_widget = t

col1, col2, col3 = st.columns(3)
with col1:
    st.button("RAG: Vector vs Graph DB", on_click=set_topic, args=("Should we use vector databases or graph databases for our new RAG system?",))
with col2:
    st.button("Cloud: AWS to GCP Migration", on_click=set_topic, args=("Should we migrate from AWS to GCP to reduce ML inference costs?",))
with col3:
    st.button("Support: Human vs AI Bots", on_click=set_topic, args=("Should we replace our customer support human team completely with AI chatbots?",))

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────
topic = st.text_area(
    label       = "💡 Decision / Topic",
    placeholder = "e.g. 'Should we launch a subscription mobile payments product in Southeast Asia?'",
    height      = 110,
    key         = "topic_widget",
)

run_button = st.button("🚀 Run Debate", disabled=st.session_state.running)

# ── Trigger ────────────────────────────────────────────────────────
if run_button:
    if not topic.strip():
        st.warning("Please enter a topic before running the debate.")
    elif not (api_key and api_key != "your_groq_api_key_here"):
        st.error("Cannot run: GROQ_API_KEY is not configured. Check your `.env` file.")
    else:
        # Reset state for fresh run
        st.session_state.running        = True
        st.session_state.logs           = []
        st.session_state.optimist_out   = None
        st.session_state.risk_out       = None
        st.session_state.final_decision = None
        st.session_state.metrics_report = None
        st.session_state.raw_metrics    = None
        st.session_state.error          = None
        st.session_state.last_topic     = topic.strip()

        # Create the shared queue and start the background thread
        log_q  = queue.Queue()
        thread = threading.Thread(
            target=_run_crew_in_thread,
            args=(topic.strip(), log_q),
            daemon=True
        )
        thread.start()

        # ── Live log area ──────────────────────────────────────────
        st.markdown("### 🔄 Live Agent Logs")
        st.caption("The agents are thinking… logs will stream below in real time.")

        log_placeholder = st.empty()
        status_bar      = st.empty()
        collected_logs  = []

        # Poll the queue while the thread is alive or there is data left
        while thread.is_alive() or not log_q.empty():
            try:
                item = log_q.get(timeout=0.15)
            except queue.Empty:
                time.sleep(0.05)
                continue

            if isinstance(item, dict):
                # Sentinel – crew finished or errored
                if item["type"] == "done":
                    st.session_state.optimist_out   = item["optimist_out"]
                    st.session_state.risk_out       = item["risk_out"]
                    st.session_state.final_decision = item["final_decision"]
                    st.session_state.metrics_report = item.get("metrics_report")
                    st.session_state.raw_metrics    = item.get("raw_metrics")
                elif item["type"] == "error":
                    st.session_state.error = item["message"]
            else:
                # Plain log line
                collected_logs.append(item)
                st.session_state.logs = collected_logs
                log_text = "\n".join(collected_logs[-80:])   # show last 80 lines
                log_placeholder.markdown(
                    f'<div class="log-box">{log_text}</div>',
                    unsafe_allow_html=True
                )

        thread.join()
        st.session_state.running = False
        status_bar.success("✅ Debate complete!")
        st.rerun()  # Refresh to render the results section cleanly

# ══════════════════════════════════════════════════════════════════════
#  RESULTS SECTION  –  rendered after crew finishes
# ══════════════════════════════════════════════════════════════════════
if st.session_state.error:
    st.error(f"**An error occurred:** {st.session_state.error}")

elif st.session_state.final_decision:
    topic_shown = st.session_state.last_topic
    st.markdown(f"### 📋 Results for: *{topic_shown}*")
    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        with st.expander("🚀 Optimist Agent — Benefits & Opportunities", expanded=True):
            st.markdown(st.session_state.optimist_out)

    with col_right:
        with st.expander("⚠️ Risk Analyst Agent — Risks & Downsides", expanded=True):
            st.markdown(st.session_state.risk_out)

    st.markdown("---")
    st.markdown("## ⚖️ Final Moderator Decision")
    st.markdown(
        '<div style="background:#1e293b; border-left:4px solid #818cf8; '
        'border-radius:8px; padding:1.2rem 1.6rem; margin-top:0.5rem;">'
        + st.session_state.final_decision.replace("\n", "<br>")
        + "</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.raw_metrics:
        opt_inf = st.session_state.raw_metrics.get("Debate_Quality", {}).get("raw_opt_influence", 50.0)
        risk_inf = st.session_state.raw_metrics.get("Debate_Quality", {}).get("raw_risk_influence", 50.0)
        
        st.markdown("#### 🌡️ Moderator Inclination Analysis")
        st.markdown(f"""
        <div style="display: flex; height: 32px; border-radius: 16px; overflow: hidden; margin-bottom: 20px; border: 1px solid #334155;">
            <div style="width: {opt_inf}%; background: linear-gradient(90deg, #1e3a8a, #3b82f6); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.85rem; transition: width 1s ease;">
                Optimist ({opt_inf}%)
            </div>
            <div style="width: {risk_inf}%; background: linear-gradient(90deg, #ef4444, #7f1d1d); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 0.85rem; transition: width 1s ease;">
                Risk Analyst ({risk_inf}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.metrics_report:
        st.markdown("---")
        st.markdown("## 📊 Observability & Performance Metrics")
        st.markdown("Highlighting Agentic AI efficiency, neutrality, and token utilization:")
        st.markdown(
            f'<div class="log-box">{st.session_state.metrics_report}</div>',
            unsafe_allow_html=True
        )

    # ── Previous logs (collapsible) ────────────────────────────────
    if st.session_state.logs:
        with st.expander("📜 Show Full Agent Logs", expanded=False):
            full_log = "\n".join(st.session_state.logs)
            st.markdown(
                f'<div class="log-box">{full_log}</div>',
                unsafe_allow_html=True
            )

    st.balloons()

# ── Idle state (nothing run yet) ───────────────────────────────────
elif not st.session_state.running:
    st.info(
        "👆 Enter your decision topic above and click **Run Debate** to start. "
        "The three AI agents will debate for ~30–90 seconds depending on the topic."
    )
