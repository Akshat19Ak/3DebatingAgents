import os
from crewai.llm import LLM
from crewai import Agent

def test_agent():
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    a = Agent(role="t", goal="t", backstory="t", llm=llm)
    print("Agent created successfully. Using groq/llama-3.3-70b-versatile")
    
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    test_agent()
