import re

def segment_qa(transcript_text):
    """
    Splits interview transcript into Q&A blocks
    based on common interviewer patterns.
    """

    # Simple heuristic-based split
    questions = re.split(
        r"(?:^|\n)(?:question|can you|could you|tell me|explain)\b",
        transcript_text,
        flags=re.IGNORECASE
    )

    qa_pairs = []
    for idx, block in enumerate(questions):
        block = block.strip()
        if len(block) < 20:
            continue

        qa_pairs.append({
            "question_id": idx,
            "answer": block
        })

    return qa_pairs
