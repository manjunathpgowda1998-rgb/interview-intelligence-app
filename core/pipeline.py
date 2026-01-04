from core.recorder import record_interview
from core.transcriber import transcribe_audio
from core.qa_segmenter import segment_qa
from core.evaluator import evaluate_answer

def run_interview_analysis(duration=30, role="CloudOps Engineer"):
    audio_file = record_interview(duration)
    transcript = transcribe_audio(audio_file)

    qa_blocks = segment_qa(transcript)

    results = []
    for idx, qa in enumerate(qa_blocks, start=1):
        evaluation = evaluate_answer(qa["answer"], role)
        results.append({
            "question_id": idx,
            "answer": qa["answer"],
            "evaluation": evaluation
        })

    return {
        "transcript": transcript,
        "analysis": results
    }
