from crewai import Task

def create_tasks(decision_problem: str, optimist_agent, risk_analyst_agent, moderator_agent):
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
                    "You must evaluate both sides sequentially in a crisp, to-the-point manner. "
                    "First, you MUST create a strict, properly formatted Markdown Table with exactly three columns: '| Aspect | Pros (Optimist) | Cons (Risk Analyst) |'. "
                    "Ensure the markdown table lines up perfectly with proper spacing and borders. "
                    "Populate this table with the most critical points from both sides organized by aspect/category. "
                    "Finally, synthesize the arguments into a single, cohesive, and balanced executive decision. "
                    "You must arrive at a single decision out of the question: whether the organization should PROCEED, ABANDON, or PIVOT.",
        expected_output="An Executive Summary containing exactly:\n"
                        "1. A strictly formatted Markdown Table comparing Aspect, Pros, and Cons side-by-side.\n"
                        "2. MODERATOR INCLINATION: A 1-sentence statement declaring whether you lean more towards the Optimist or the Risk Analyst based on the severity of the points.\n"
                        "3. FINAL VERDICT: A single, extremely crisp definitive decision (Proceed/Abandon/Pivot) with a 1-2 sentence logical justification.",
        agent=moderator_agent,
        context=[optimist_task, risk_task] # Moderator needs the outputs of both agents
    )

    return optimist_task, risk_task, moderation_task
