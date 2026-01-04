from core.recorder import record_interview
from core.transcriber import transcribe_audio
from core.realtime_answer import generate_answer

print("🎤 Ask your question...")
audio = record_interview(7)

question = transcribe_audio(audio)
print("\n📝 Question:", question)

answer = generate_answer(question)
print("\n🤖 AI Answer:\n", answer)
