from core.qa_segmenter import segment_qa

sample_text = """
Can you explain what Docker is?
Docker is a containerization platform that allows applications
to be packaged with their dependencies.

Tell me about a production issue you handled.
I faced a server outage where CPU usage was high.
"""

qa = segment_qa(sample_text)

for item in qa:
    print(f"\nQ{item['question_id']} ANSWER:")
    print(item["answer"])
