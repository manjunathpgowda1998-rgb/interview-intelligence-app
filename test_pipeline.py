from core.pipeline import run_interview_analysis

result = run_interview_analysis(duration=20, role="CloudOps Engineer")

for item in result["analysis"]:
    print("\n====================")
    print("ANSWER:")
    print(item["answer"])
    print("\nEVALUATION:")
    print(item["evaluation"])
