import streamlit as st
import tempfile
import whisper
import os
from groq import Groq

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Interview Voice Assistant", layout="wide")
st.title("🎙️ Interview Voice Assistant (FAST – FREE MODE)")
# ---------------------------------------

# ---------- Load Whisper ONCE ----------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base.en")  # fast on CPU

whisper_model = load_whisper()

# ---------- Groq Client ----------
if "GROQ_API_KEY" not in os.environ:
    st.error("GROQ_API_KEY not found. Please set environment variable.")
    st.stop()

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

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

st.info("Flow: Speak → Transcribe → Edit → Generate → Continue")

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
                fp16=False
            )
            st.session_state.transcript = result["text"].strip()

# ---------- Edit ----------
st.subheader("✏️ Edit / Type Question")
edited_question = st.text_area(
    "Question:",
    value=st.session_state.transcript,
    height=120
)

# ---------- Generate ----------
if st.button("🤖 Generate Answer"):
    if not edited_question.strip():
        st.warning("Please record or type a question.")
    else:
        prompt = f"""
You are a senior {role} in an interview.

Answer clearly and professionally.
Use simple spoken English.
Explain step by step.
Give enough detail an interviewer expects.

Question:
{edited_question}
"""

        with st.spinner("Generating answer..."):
            response = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a senior interview expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=400
            )

            answer = response.choices[0].message.content

        # Save conversation
        st.session_state.chat.append({
            "question": edited_question,
            "answer": answer
        })

        st.session_state.transcript = ""
        st.rerun()

# ---------- Scrollable Chat History ----------
st.subheader("💬 Conversation")

st.markdown(
    """
    <style>
    .chat-box {
        max-height: 420px;
        overflow-y: auto;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for item in reversed(st.session_state.chat):  # newest first
    st.markdown(f"**🧑 You:** {item['question']}")
    st.markdown(f"**🤖 AI:** {item['answer']}")
    st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)
