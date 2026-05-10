from crewai import Task
from .agents import optimist_agent, risk_analyst_agent, moderator_agent

def create_tasks(decision_problem: str):
    # Task 1: The Optimist's Analysis
    optimist_task = Task(
        description=f"Analyze this proposed idea/decision: '{decision_problem}'. "
                    "Write a comprehensive report detailing the maximum possible benefits, "
                    "expected ROI, structural improvements, and strategic advantages. "
                    "Be highly optimistic and visionary.",
        expected_output="A bulleted list or structured paragraph explaining why this idea is brilliant and the best possible outcomes.",
        agent=optimist_agent,
    )

    # Task 2: The Risk Analyst's Analysis
    risk_task = Task(
        description=f"Analyze the exact same proposed idea/decision: '{decision_problem}'. "
                    "Write a severe and detailed critique outlining the potential failures, risks, "
                    "losses, and operational dangers. "
                    "Be highly skeptical and focus strictly on what could go horribly wrong.",
        expected_output="A bulleted list or structured paragraph outlining all the severe risks and downsides of the idea.",
        agent=risk_analyst_agent,
    )

    # Task 3: The Moderator's Synthesis
    moderation_task = Task(
        description=f"Review the Optimist's report and the Risk Analyst's report regarding the idea: '{decision_problem}'. "
                    "Weigh both sides carefully. Do not just summarize. "
                    "Synthesize the arguments into a single, cohesive, and balanced executive decision. "
                    "Decide whether the organization should PROCEED, ABANDON, or PIVOT the idea.",
        expected_output="An Executive Summary containing:\n"
                        "1. A brief summary of the upside.\n"
                        "2. A brief summary of the downside.\n"
                        "3. The Final Verdict (Proceed/Abandon/Pivot) with a clear, logical justification.",
        agent=moderator_agent,
        context=[optimist_task, risk_task] # Moderator needs the outputs of both agents
    )

    return optimist_task, risk_task, moderation_task
