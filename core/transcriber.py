import whisper
import streamlit as st

# --------------------------------------------------
# Load Whisper ONCE (FAST ENGLISH MODEL)
# --------------------------------------------------
@st.cache_resource
def load_whisper_model():
    # 🔥 base.en = best speed / accuracy on CPU
    return whisper.load_model("base.en")

model = load_whisper_model()

# --------------------------------------------------
# Optimized Technical Prompt (shortened)
# --------------------------------------------------
TECH_PROMPT = (
    "Technical interview about DevOps, CloudOps, "
    "Docker, Kubernetes, CI CD, AWS, Azure, Linux, RBAC."
)

# --------------------------------------------------
# Transcription (FAST SETTINGS)
# --------------------------------------------------
def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe(
        audio_path,
        language="en",
        task="transcribe",
        fp16=False,
        temperature=0,
        beam_size=1,        # 🔥 HUGE speed gain
        best_of=1,          # 🔥 no retries
        initial_prompt=TECH_PROMPT,
        condition_on_previous_text=False,
        verbose=False
    )
    return result["text"].strip()
