import sys
sys.path.insert(0, ".")
from ai.agent import agent

# Setup the agent
agent.setup()

# Ask 3 questions
questions = [
    "Which entity is most profitable?",
    "Are there any suspicious transactions?",
    "What happened to revenue during COVID in 2020?",
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {agent.ask(q)}")
    print("-" * 50)