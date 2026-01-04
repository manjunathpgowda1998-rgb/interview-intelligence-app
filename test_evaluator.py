from core.evaluator import evaluate_answer

answer = """
Docker is a containerization platform that allows applications
to be packaged with their dependencies.
"""

result = evaluate_answer(answer)

print(result)
