import streamlit as st
import tempfile
import whisper
import os
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Interview Voice Assistant",
    layout="wide"
)
st.title("🎙️ Interview Voice Assistant (FAST – FREE MODE)")

# ---------------- LOAD WHISPER (ONCE) ----------------
@st.cache_resource
def load_whisper():
    # base.en = best balance for Indian accent + tech words
    return whisper.load_model("base.en")

whisper_model = load_whisper()

# ---------------- GROQ CLIENT ----------------
if "GROQ_API_KEY" not in os.environ:
    st.error("❌ GROQ_API_KEY not set. Please add it as an environment variable.")
    st.stop()

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# ---------------- ROLE SELECTION ----------------
role = st.selectbox(
    "Select Role",
    ["CloudOps Engineer", "DevOps Engineer", "Backend Developer"]
)

st.info("🎯 Speak → Transcribe → Edit → Generate → Ask next question")

st.divider()

# ================== INPUT SECTION (ALWAYS TOP) ==================
st.subheader("🎤 Ask Your Question")

audio = st.audio_input("Record your question")

# ---------------- TRANSCRIPTION (OPTIMIZED) ----------------
if audio is not None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(audio.read())

        with st.spinner("🧠 Transcribing voice..."):
            result = whisper_model.transcribe(
                tmp.name,
                language="en",
                temperature=0.0,   # improves accuracy
                beam_size=1,       # fastest decoding
                best_of=1,         # no extra guessing
                fp16=False,
                condition_on_previous_text=False,
                initial_prompt=(
                    "This is a technical interview question about "
                    "DevOps, Docker, Kubernetes, CI CD, cloud, "
                    "security, RBAC, monitoring, ITIL."
                )
            )

            st.session_state.transcript = result["text"].strip()

# ---------------- EDIT QUESTION ----------------
edited_question = st.text_area(
    "✏️ Edit / Type your question:",
    value=st.session_state.transcript,
    height=120
)

# ---------------- GENERATE ANSWER ----------------
if st.button("🤖 Generate Answer", use_container_width=True):
    if not edited_question.strip():
        st.warning("Please record or type a question.")
    else:
        prompt = f"""
You are a senior {role} in a technical interview.

Rules:
- Use clear, simple spoken English
- Explain step by step
- Give enough detail an interviewer expects
- Avoid unnecessary theory and repetition

Question:
{edited_question}
"""

        with st.spinner("⚡ Generating answer (very fast)..."):
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are an interview expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            answer = response.choices[0].message.content

        # Save conversation (latest on top)
        st.session_state.chat.insert(0, {
            "question": edited_question,
            "answer": answer
        })

        # Clear for next question
        st.session_state.transcript = ""
        st.rerun()

# ================== CONVERSATION HISTORY ==================
st.divider()

with st.expander("💬 Previous Questions & Answers", expanded=False):
    if not st.session_state.chat:
        st.info("No previous questions yet.")
    else:
        for item in st.session_state.chat:
            st.markdown(f"**🧑 You:** {item['question']}")
            st.markdown(f"**🤖 AI:** {item['answer']}")
            st.markdown("---")

# ================== CLEAR BUTTON ==================
if st.button("🧹 Clear Conversation"):
    st.session_state.chat = []
    st.session_state.transcript = ""
    st.rerun()
