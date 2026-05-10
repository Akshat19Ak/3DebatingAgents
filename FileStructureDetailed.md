# Multi-Agent Debate System: Complete File Structure Guide

This document breaks down the exact architecture of the project. It explains the "what, why, when, where, and how" for every single file in the repository.

---

## 📂 Project Repository: `3DebatingAgents/`
*(This is the Root Directory. It contains configuration files and the main source folder.)*

### 1. `requirements.txt`
| Metric | Description |
| :--- | :--- |
| **What is it?** | A plain text file listing all external Python packages required for the project. |
| **Why is it needed?** | Python projects rely on 3rd-party code (like `crewai`). Without this file, another developer wouldn't know what to install to make your code run. |
| **When to create it?** | Phase 1 (Setup). Created immediately after initializing the project repository before writing any python code. |
| **Where to place it?** | The absolute root directory (`3DebatingAgents/`). |
| **How does it work?** | You pass this file to the Python package manager (`pip install -r requirements.txt`). It reads the file top-to-bottom and downloads everything into your virtual environment. |

### 2. `.env` & `.env.example`
| Metric | Description |
| :--- | :--- |
| **What is it?** | Environment variable configuration files. They store secret keys (like `GROQ_API_KEY`). |
| **Why is it needed?** | Hardcoding API keys in `.py` files is a massive security risk. If pushed to GitHub, hackers will steal your keys. The `.env` file is hidden and ignored by Git. `.env.example` provides the *template* without the actual secrets. |
| **When to create it?** | Phase 1 (Setup). Created right before you start integrating external APIs/LLMs. |
| **Where to place it?** | The absolute root directory (`3DebatingAgents/`). |
| **How does it work?** | The `python-dotenv` framework loads the contents of this file into the operating system's memory during runtime, where `os.getenv()` can securely fetch them. |

### 3. `test_llm.py`
| Metric | Description |
| :--- | :--- |
| **What is it?** | A standalone debugger script we created to isolate and test the LLM connection. |
| **Why is it needed?** | When building complex agentic systems, if an error occurs, it's hard to tell if it's the Agent logic failing or the LLM connection failing. This script isolated the LLM to prove our API key and Model string worked. |
| **When to create it?** | As needed. Created during the debugging phase to fix the `fastapi` and OpenAI Key errors. |
| **Where to place it?** | The absolute root directory (`3DebatingAgents/`). |
| **How does it work?** | It bypasses the Crew engine entirely, initializes a single basic Agent, and attempts to contact Groq. |

---

## 📂 Source Code: `src/`
*(This directory isolates our actual Python application logic from our root configuration files. This is a critical best practice in enterprise software.)*

### 4. `src/agents.py`
| Metric | Description |
| :--- | :--- |
| **What is it?** | The identity registry. It defines *who* the AI personas are. |
| **Why is it needed?** | Separation of concerns. If we mixed Agent definitions, Task assignments, and Execution logic into one file, it would be unreadable. This file strictly handles the "Backstory/Role" prompt engineering. |
| **When to create it?** | Phase 2 (Implementation). This is the very first Python file written because Tasks cannot exist without an Agent to assign them to. |
| **Where to place it?** | Inside the `src/` directory. |
| **How does it work?** | Utilizes `crewai.Agent`. It configures the Groq LLM (the "brain") and binds it to specific personas (Optimist, Risk Analyst, Moderator). |

### 5. `src/tasks.py`
| Metric | Description |
| :--- | :--- |
| **What is it?** | The objective registry. It defines *what* needs to be done. |
| **Why is it needed?** | Agents are useless without instructions. This file maps the user's input (`decision_problem`) to specific goals (e.g., "Find the downside"). |
| **When to create it?** | Phase 2 (Implementation). Created immediately after `agents.py`. |
| **Where to place it?** | Inside the `src/` directory. |
| **How does it work?** | Utilizes `crewai.Task`. Crucially, it manages **Context Passing**. The moderator task in this file is explicitly programmed to wait for the outputs of the Optimist and Risk Analyst before executing. |

### 6. `src/crew.py`
| Metric | Description |
| :--- | :--- |
| **What is it?** | The orchestration engine. It defines *how* the Agents and Tasks flow together. |
| **Why is it needed?** | You have actors (`agents.py`) and a script (`tasks.py`). Now you need a director to put them on stage in the correct order. |
| **When to create it?** | Phase 2 (Implementation). Created after Agents and Tasks are fully defined. |
| **Where to place it?** | Inside the `src/` directory. |
| **How does it work?** | Utilizes `crewai.Crew`. It imports the agents and tasks, groups them into an array, and enforces `Process.sequential`—ensuring Agent 1 finishes before Agent 2 begins. |

### 7. `src/main.py`
| Metric | Description |
| :--- | :--- |
| **What is it?** | The interactive entry point. The only script the user actually runs. |
| **Why is it needed?** | It acts as the bridge between the human and the AI system. It handles user input (terminal `input()`), validates environment variables, and kicks off the Crew. |
| **When to create it?** | Phase 2 (Implementation). This is the final Python file written to tie the whole system together. |
| **Where to place it?** | Inside the `src/` directory. |
| **How does it work?** | It uses a standard `if __name__ == "__main__":` Python construct. It captures the user's string, passes it to the `build_debate_crew()` function from `crew.py`, and calls `.kickoff()` to initiate the LLM API requests. |

---

## 📂 Documentation (Root Directory)
*(These markdown guides were created strictly for mentorship and knowledge transfer.)*

- `1_TheoryAgenticAI.md`: Explains the paradigm shift from single-prompt LLMs to Goal-oriented AI.
- `2_basic_agentic_ai_concepts.md`: Explains tools, hierarchical vs sequential orchestration, and prompt engineering.
- `3_handson_implementation_plan.md`: Translates the theory into the blueprint for this exact project.
- `4_Project_Implementation_guide.md`: A lighter version of *this* document, explaining separation of concerns in `src/`.
- `5_Project_RUN_guide.md`: Step-by-step terminal commands for a beginner to start the code.
- `Multi_Agent_Debate_System_Complete_Workflow_Training_Guide.md`: The magnum opus. A comprehensive, interview-ready guide explaining the architectural trade-offs, the cost analysis, and production-hardening of the system.
- `FileStructureDetailed.md`: This file. Highlighting the exact lifecycle of the codebase.
