import os
import sys
from dotenv import load_dotenv

# Ensure that the src modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crew import build_debate_crew
from src.metrics import DebateEvaluator

def main():
    print("="*60)
    print("WELCOME TO THE MULTI-AGENT DEBATE & DECISION SYSTEM")
    print("This system uses CrewAI to analyze business decisions.")
    print("Agents: [1] Optimist -> [2] Risk Analyst -> [3] Moderator")
    print("="*60)
    
    # Check if GROQ_API_KEY is available
    load_dotenv()
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("\nERROR: GROQ_API_KEY is not set or is using the default placeholder.")
        print("Please configure your .env file with a valid API key.")
        sys.exit(1)

    print("\nPlease enter the decision problem or proposed idea you would like analyzed:")
    decision_problem = input("> ")

    if not decision_problem.strip():
        print("A valid decision problem must be entered. Exiting...")
        sys.exit(1)

    print("\n" + "="*60)
    print(f"STARTING DEBATE CREW FOR: {decision_problem}")
    print("="*60 + "\n")

    try:
        # Initialize Evaluator
        evaluator = DebateEvaluator(decision_problem)

        # Build the crew
        debate_crew = build_debate_crew(decision_problem)
        
        # Kickoff the process
        # The result will be the final task's output (The Moderator's synthesis)
        result = debate_crew.kickoff()
        
        # Extract individual task outputs for evaluation
        tasks = debate_crew.tasks
        optimist_output = str(tasks[0].output) if tasks and tasks[0].output else ""
        risk_output = str(tasks[1].output) if len(tasks) > 1 and tasks[1].output else ""
        final_decision = str(result)

        # Evaluate performance
        evaluator.evaluate(optimist_output, risk_output, final_decision)

        print("\n" + "="*60)
        print("============= FINAL MODERATOR DECISION =============")
        print("="*60)
        print(final_decision)
        print("="*60)

        # Print the AI Observability Report
        print(evaluator.get_formatted_report())

    except Exception as e:
        print(f"\nAn error occurred during the Crew AI process: {str(e)}")

if __name__ == "__main__":
    main()
