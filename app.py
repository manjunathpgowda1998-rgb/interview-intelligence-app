import streamlit as st
import whisper
import requests
import tempfile
import html

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "tinyllama"   # fastest on CPU
# ---------------------------------------

st.set_page_config(page_title="Interview Voice Assistant", layout="wide")
st.title("🎙️ Interview Voice Assistant")

# ---------- Load Whisper ONCE ----------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base.en")

whisper_model = load_whisper()

# ---------- Session State ----------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# ---------- Role ----------
role = st.selectbox(
    "Select Role",
    ["CloudOps Engineer", "DevOps Engineer", "Backend Developer"]
)

st.info("Flow: Record → Edit → Copy → Generate → Continue")

# ---------- Chat History ----------
if st.session_state.chat:
    st.subheader("💬 Conversation")
    for item in st.session_state.chat:
        st.markdown(f"**You:** {item['question']}")
        st.markdown(f"**AI:** {item['answer']}")
        st.markdown("---")

# ---------- Browser Mic ----------
audio = st.audio_input("🎤 Record your question")

# ---------- Transcription ----------
if audio is not None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio.read())

        with st.spinner("Transcribing voice..."):
            result = whisper_model.transcribe(
                tmp.name,
                language="en",
                initial_prompt=(
                    "This is a technical interview question about "
                    "Docker, Kubernetes, DevOps, CI CD, cloud security, RBAC, ITIL."
                ),
                beam_size=1,
                best_of=1,
                fp16=False
            )

            st.session_state.transcript = result["text"].strip()

# ---------- Edit ----------
st.subheader("✏️ Edit Question")
edited_question = st.text_area(
    "Fix transcription if needed:",
    value=st.session_state.transcript,
    height=120
)

# ---------- Copy Button ----------
if edited_question.strip():
    escaped = html.escape(edited_question)
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{escaped}`)">
            📋 Copy Question
        </button>
        """,
        unsafe_allow_html=True
    )

# ---------- Generate ----------
if st.button("🤖 Generate Answer"):
    if edited_question.strip() == "":
        st.warning("Please record or type a question.")
    else:
        prompt = f"""
You are a professional {role} answering in a technical interview.

Rules:
- Speak clearly and confidently
- Use simple English
- Explain step by step
- Give 1 small real-world example if useful
- No commands unless asked
- Sound practical and experienced
Question:
{st.session_state.transcript}
"""

        with st.spinner("Generating answer..."):
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 500,
                        "temperature": 0.3,
                        "top_p": 0.9
                    }
                },
                timeout=25
            )

            answer = response.json().get("response", "No answer generated.")

        st.session_state.chat.append({
            "question": edited_question,
            "answer": answer
        })

        st.session_state.transcript = ""
        st.rerun()
