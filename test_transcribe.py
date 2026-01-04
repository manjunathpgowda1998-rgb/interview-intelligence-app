from core.recorder import record_interview
from core.transcriber import transcribe_audio

audio_file = record_interview(10)
text = transcribe_audio(audio_file)

print("\n--- TRANSCRIPT ---\n")
print(text)
