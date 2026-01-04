import sounddevice as sd
import numpy as np
import wave
import time
import os

SAMPLE_RATE = 16000
CHANNELS = 1

# ==================================================
# 1️⃣ Used by Interview Analysis Mode (pipeline.py)
# KEEP FILE SAVE (offline analysis)
# ==================================================
def record_interview(duration=30):
    """
    Records full interview and saves WAV.
    Optimized:
    - Records int16 directly (no float math)
    """
    os.makedirs("audio", exist_ok=True)
    filename = f"audio/interview_{int(time.time())}.wav"

    print(f"🎙 Recording interview for {duration} seconds...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"          # 🔥 faster, no conversion
    )
    sd.wait()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)     # int16
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    print(f"✅ Interview saved: {filename}")
    return filename


# ==================================================
# 2️⃣ Used by Real-Time Answer Mode (app.py)
# SAME FUNCTION NAME — MUCH FASTER
# ==================================================
def record_until_silence(max_seconds=4):
    """
    FAST real-time recording.
    Changes:
    ❌ No callback loop
    ❌ No Python silence detection
    ❌ No disk write here
    ✅ RAM-only audio
    Silence trimming should be done AFTER using VAD.
    """
    print("🎙 Listening... speak now")

    audio = sd.rec(
        int(max_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    sd.wait()

    # Return RAW audio instead of filename (FASTER)
    return audio.flatten()
