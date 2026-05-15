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
                    "You must evaluate both sides sequentially. "
                    "First, explicitly state the Pros given by the Optimist. "
                    "Second, explicitly state the Cons given by the Risk Analyst. "
                    "Finally, synthesize the arguments into a single, cohesive, and balanced executive decision. "
                    "You must arrive at a single decision out of the question: whether the organization should PROCEED, ABANDON, or PIVOT.",
        expected_output="An Executive Summary containing exactly:\n"
                        "1. PROS (Optimist View): A clear summary of the upside.\n"
                        "2. CONS (Risk Analyst View): A clear summary of the downside.\n"
                        "3. FINAL VERDICT: A single definitive decision (Proceed/Abandon/Pivot) with a clear, logical justification.",
        agent=moderator_agent,
        context=[optimist_task, risk_task] # Moderator needs the outputs of both agents
    )

    return optimist_task, risk_task, moderation_task
