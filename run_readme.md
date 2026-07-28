# 🐍 In-Depth Guide: Running the Multi-Agent Debate System in a Python Virtual Environment (`venv`)

This guide provides step-by-step, comprehensive instructions for setting up, configuring, and executing the **Multi-Agent Debate & Decision Intelligence System** inside an isolated Python Virtual Environment (`venv`). 

Using a virtual environment ensures that all project dependencies (such as CrewAI, LiteLLM, and Streamlit) remain isolated from your global Python environment and prevent dependency conflicts.

---

## 📑 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Step 1: Navigate to the Project Root](#step-1-navigate-to-the-project-root)
3. [Step 2: Create the Virtual Environment](#step-2-create-the-virtual-environment)
4. [Step 3: Activate the Virtual Environment](#step-3-activate-the-virtual-environment)
5. [Step 4: Upgrade pip & Install Dependencies](#step-4-upgrade-pip--install-dependencies)
6. [Step 5: Configure Environment Variables](#step-5-configure-environment-variables)
7. [Step 6: Verify API Connection & Setup](#step-6-verify-api-connection--setup)
8. [Step 7: Launch the Application](#step-7-launch-the-application)
   - [Mode A: Command Line Interface (CLI)](#mode-a-command-line-interface-cli)
   - [Mode B: Interactive Web UI (Streamlit Dashboard)](#mode-b-interactive-web-ui-streamlit-dashboard)
9. [Step 8: Deactivating the Virtual Environment](#step-8-deactivating-the-virtual-environment)
10. [Troubleshooting & Common Issues](#troubleshooting--common-issues)
11. [Key Project Files Reference](#key-project-files-reference)

---

## 1. Prerequisites

Before starting, verify that you have the required software installed:

- **Python 3.10 or higher**:
  Open your terminal and check your Python version:
  ```bash
  # Windows (PowerShell / Command Prompt)
  python --version

  # macOS / Linux
  python3 --version
  ```
  *If your Python version is below 3.10, please download and install Python 3.10+ from [python.org](https://www.python.org/downloads/).*

- **Groq API Key**:
  This system uses high-speed Groq LPU inference ([llama-3.3-70b-versatile](https://groq.com/)). You will need an API key from the [Groq Console](https://console.groq.com/keys).

---

## Step 1: Navigate to the Project Root

Open your terminal or command prompt and change directory (`cd`) into the root folder of the project:

```bash
cd path/to/3DebatingAgents
```

> [!IMPORTANT]
> All commands in this guide must be run from the **root directory** (`3DebatingAgents/`), where [requirements.txt](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/requirements.txt) is located.

---

## Step 2: Create the Virtual Environment

Run the following command to create a new virtual environment directory named `venv` inside the project root:

### Windows (PowerShell or Command Prompt)
```bash
python -m venv venv
```

### macOS / Linux
```bash
python3 -m venv venv
```

After execution, you will see a new `venv/` folder created in your project directory containing the standalone Python interpreter and package binaries.

---

## Step 3: Activate the Virtual Environment

You must activate the virtual environment so your shell uses the isolated Python interpreter.

### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

### Windows (Command Prompt - `cmd.exe`)
```cmd
venv\Scripts\activate.bat
```

### macOS / Linux
```bash
source venv/bin/activate
```

> [!NOTE]
> Once activated, your terminal prompt will display `(venv)` at the beginning of the command line, for example:
> `(venv) C:\path\to\3DebatingAgents>`

---

## Step 4: Upgrade `pip` & Install Dependencies

With `(venv)` active, first ensure your package manager (`pip`) is up to date, then install all project requirements specified in [requirements.txt](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/requirements.txt):

```bash
# 1. Upgrade pip to the latest version
python -m pip install --upgrade pip

# 2. Install required dependencies
pip install -r requirements.txt
```

### What gets installed?
- **CrewAI & LangChain-Groq**: Multi-agent orchestration and LLM wrappers.
- **LiteLLM**: Unified LLM calling interface.
- **Streamlit**: Interactive web dashboard framework.
- **Scikit-Learn & TextBlob**: Evaluator metrics (TF-IDF similarity, sentiment analysis).
- **Python-Dotenv & Pydantic**: Environment variable loading and data validation.

---

## Step 5: Configure Environment Variables

The system requires your Groq API key to invoke the Llama 3.3 70B model.

1. Create a new file named `.env` in the project root directory ([.env](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/.env)):
   ```bash
   # Linux / macOS / Windows PowerShell
   New-Item -Path .env -ItemType File
   ```
2. Open [.env](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/.env) in any text editor and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

> [!CAUTION]
> Never commit your `.env` file to version control. It is already excluded via [.gitignore](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/.gitignore).

---

## Step 6: Verify API Connection & Setup

Before running the full debate crew, run the built-in test script [test_llm.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/test_llm.py) to confirm that your `.env` key is loaded correctly and that LiteLLM/Groq communication works:

```bash
python test_llm.py
```

### Expected Output:
```text
Agent created successfully. Using groq/llama-3.3-70b-versatile
```

If you see this message, your virtual environment and API credentials are fully functional.

---

## Step 7: Launch the Application

You can execute the Multi-Agent Debate System in two different modes depending on your preference:

### Mode A: Command Line Interface (CLI)

The CLI mode runs the debate interactively inside your terminal and outputs a formatted markdown executive decision and an AI Observability Report.

1. Run the entry point [src/main.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/main.py):
   ```bash
   python src/main.py
   ```
2. Enter your business decision problem at the prompt (e.g., *"Should our startup migrate from AWS to a multi-cloud Kubernetes infrastructure?"*).
3. The system will sequentially trigger:
   - **Optimist Agent**: Builds the strategic benefits and upside argument.
   - **Risk Analyst Agent**: Uncovers vulnerabilities, costs, and failure risks.
   - **Executive Moderator**: Evaluates both arguments and delivers a Proceed/Abandon/Pivot verdict.
   - **Metrics Layer**: Outputs debate diversity, agent influence, and sentiment alignment scores.

---

### Mode B: Interactive Web UI (Streamlit Dashboard)

The web dashboard provides an executive graphical interface with real-time progress logging, side-by-side debate tabs, and visual metric indicators.

1. Launch Streamlit using [src/app.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/app.py):
   ```bash
   streamlit run src/app.py
   ```
2. Streamlit will automatically open your default browser at:
   ```text
   http://localhost:8501
   ```
3. Type your decision problem into the UI text box and click **"🚀 Initialize Debate Crew"**.

> [!TIP]
> If port `8501` is already in use by another application, you can specify an alternative port:
> ```bash
> streamlit run src/app.py --server.port 8502
> ```

---

## Step 8: Deactivating the Virtual Environment

When you are finished using the application, you can exit the virtual environment by running:

```bash
deactivate
```

Your command prompt will return to normal, and system-wide Python settings will be restored.

---

## Troubleshooting & Common Issues

| Symptom / Error | Root Cause | Solution |
| :--- | :--- | :--- |
| **`Activate.ps1 cannot be loaded because running scripts is disabled on this system`** (Windows PowerShell) | PowerShell execution policy restricts script execution. | Run PowerShell as Administrator or run this command for your current user: `<br>` `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| **`ERROR: GROQ_API_KEY is not set or is using the default placeholder`** | The `.env` file is missing, misnamed, or contains the placeholder string. | Ensure the file is named exactly `.env` (not `.env.txt`) in the project root and contains `GROQ_API_KEY=gsk_...`. |
| **`ModuleNotFoundError: No module named 'src'`** or **`No module named 'crewai'`** | Either the virtual environment is not activated or you are running from outside the project root. | 1. Ensure `(venv)` is displayed in your prompt.<br>2. Run commands from the directory containing `requirements.txt`. |
| **Streamlit UI appears unresponsive or stuck** | Heavy API inference can take 30-45 seconds for comprehensive analyses. | Do not refresh the page immediately; monitor terminal output logs to see live CrewAI task progression. |
| **`Address already in use` (Streamlit)** | Another Streamlit instance or service is using port 8501. | Stop the other process or launch with `--server.port 8502`. |

---

## Key Project Files Reference

| File / Directory Path | Description |
| :--- | :--- |
| [requirements.txt](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/requirements.txt) | List of required Python packages for the virtual environment. |
| [.env](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/.env) | Local environment variables file containing `GROQ_API_KEY`. |
| [test_llm.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/test_llm.py) | Verification script to test Groq API connectivity and LLM instantiation. |
| [src/main.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/main.py) | Command Line Interface (CLI) entry point. |
| [src/app.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/app.py) | Interactive Streamlit Web UI dashboard application. |
| [src/crew.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/crew.py) | Orchestration logic assembling agents and tasks into a CrewAI pipeline. |
| [src/agents.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/agents.py) | Persona definitions for Optimist, Risk Analyst, and Moderator. |
| [src/tasks.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/tasks.py) | Prompt engineering and sequential task flows. |
| [src/metrics.py](file:///c:/Users/KIIT0001/Desktop/Societies/Coding%20Ninjas/3rd%20yr%20ml/AgenticAI_Tasks/3DebatingAgents/src/metrics.py) | Evaluation layer computing debate diversity and agent influence. |
