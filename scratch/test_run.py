import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crew import build_debate_crew
from src.metrics import DebateEvaluator
from dotenv import load_dotenv

load_dotenv()

topic = "Should we replace our customer support human team completely with AI chatbots?"

evaluator = DebateEvaluator(topic)
debate_crew = build_debate_crew(topic)
result = debate_crew.kickoff()

tasks = debate_crew.tasks
optimist_output = str(tasks[0].output) if tasks and tasks[0].output else ""
risk_output = str(tasks[1].output) if len(tasks) > 1 and tasks[1].output else ""
final_decision = str(result)

evaluator.evaluate(optimist_output, risk_output, final_decision)
print("=== METRICS ===")
for cat, data in evaluator.metrics.items():
    for k, v in data.items():
        print(f"{k}: {v}")
