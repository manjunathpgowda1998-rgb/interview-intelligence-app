from core.realtime_answer import generate_answer

question = "What is Docker and why is it used?"

answer = generate_answer(question)
print("\nQUESTION:\n", question)
print("\nAI ANSWER:\n", answer)
