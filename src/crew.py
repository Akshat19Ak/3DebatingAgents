from crewai import Crew, Process
from .agents import create_agents
from .tasks import create_tasks

def build_debate_crew(decision_problem: str, api_key: str):
    """
    Assembles the Multi-Agent Debate Crew.
    The process is sequential:
    1. Optimist provides their analysis.
    2. Risk Analyst provides their critique.
    3. Moderator reviews the optimist and risk analyst outputs and synthesizes the final decision.
    """
    
    # 0. Instantiate the agents for this specific session
    optimist_agent, risk_analyst_agent, moderator_agent = create_agents(api_key)

    # 1. Instantiate the tasks using the decision problem and agents
    optimist_task, risk_task, moderation_task = create_tasks(decision_problem, optimist_agent, risk_analyst_agent, moderator_agent)

    # 2. Build the Crew configuration
    debate_crew = Crew(
        agents=[optimist_agent, risk_analyst_agent, moderator_agent],
        tasks=[optimist_task, risk_task, moderation_task],
        process=Process.sequential,  # Executes tasks linearly
        verbose=True,  # Enable detailed logging to the terminal
        # Ensure that the context flows naturally (moderation_task manually takes context of the first two)
    )
    
    return debate_crew
