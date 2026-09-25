import os
from crewai.llm import LLM
from crewai import Agent

def test_agent():
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    a = Agent(role="t", goal="t", backstory="t", llm=llm)
    print("Agent created successfully. Using groq/openai/gpt-oss-120b")
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    test_agent()
