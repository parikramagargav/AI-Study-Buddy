import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader

# ----------------------------
# Setup
# ----------------------------
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 15% 0%, #1b2440 0%, #0f1525 45%, #0a0e1a 100%);
        }

        #MainMenu, footer, header {visibility: hidden;}

        /* ---------- Hero ---------- */
        .hero {
            padding: 2.4rem 2.6rem;
            border-radius: 20px;
            background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 55%, #c026d3 100%);
            margin: 0.5rem 0 1.8rem 0;
            box-shadow: 0 20px 45px rgba(79, 70, 229, 0.28);
            position: relative;
            overflow: hidden;
        }
        .hero::after {
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 280px;
            height: 280px;
            background: rgba(255,255,255,0.08);
            border-radius: 50%;
        }
        .hero h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 800;
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.02em;
        }
        .hero p {
            color: rgba(255,255,255,0.88);
            font-size: 1.05rem;
            margin: 0;
            max-width: 600px;
            line-height: 1.5;
        }

        /* ---------- Upload card ---------- */
        .upload-card {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 16px;
            padding: 1.4rem 1.6rem 0.6rem 1.6rem;
            margin-bottom: 1.6rem;
        }
        .upload-title {
            color: #e2e8f0;
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        [data-testid="stFileUploader"] section {
            background: rgba(255,255,255,0.02);
            border: 1.5px dashed rgba(124, 58, 237, 0.45);
            border-radius: 12px;
        }
        [data-testid="stFileUploader"] section:hover {
            border-color: #a78bfa;
        }

        /* ---------- Cards ---------- */
        .card {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 16px;
            padding: 1.5rem 1.7rem;
            margin-bottom: 1.2rem;
        }
        .card h3 {
            margin: 0 0 0.3rem 0;
            color: #f1f5f9;
            font-weight: 700;
            font-size: 1.25rem;
        }
        .card .desc {
            color: #94a3b8;
            font-size: 0.92rem;
            margin-bottom: 1.1rem;
        }

        /* ---------- Section label ---------- */
        .section-label {
            display: inline-block;
            background: rgba(124, 58, 237, 0.16);
            color: #c4b5fd;
            padding: 0.28rem 0.85rem;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        /* ---------- Status chip ---------- */
        .status-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(34,197,94,0.13);
            color: #4ade80;
            border: 1px solid rgba(34,197,94,0.25);
            padding: 0.4rem 0.95rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }

        /* ---------- Stat boxes ---------- */
        .stat-box {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 14px;
            padding: 1rem 1.2rem;
        }
        .stat-box .num {
            color: #c4b5fd;
            font-size: 1.7rem;
            font-weight: 800;
            line-height: 1;
        }
        .stat-box .lbl {
            color: #94a3b8;
            font-size: 0.78rem;
            margin-top: 0.35rem;
            font-weight: 500;
        }

        /* ---------- Buttons ---------- */
        .stButton > button {
            width: 100%;
            border-radius: 11px;
            border: none;
            background: linear-gradient(120deg, #6366f1, #a855f7);
            color: white;
            font-weight: 700;
            font-size: 0.95rem;
            padding: 0.65rem 1rem;
            transition: all 0.18s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 24px rgba(124, 58, 237, 0.38);
            color: white;
        }
        .stButton > button:active {
            transform: translateY(0px);
        }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: rgba(255,255,255,0.03);
            padding: 6px;
            border-radius: 14px;
        }
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8;
            font-weight: 600;
            font-size: 0.9rem;
            border-radius: 10px;
            padding: 0.55rem 1rem;
        }
        .stTabs [aria-selected="true"] {
            color: white !important;
            background: linear-gradient(120deg, #6366f1, #a855f7);
        }

        /* ---------- Text input ---------- */
        .stTextInput > div > div > input {
            border-radius: 11px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.1);
            color: #f1f5f9;
        }
        .stTextInput > div > div > input:focus {
            border-color: #a78bfa;
        }

        /* ---------- Expander ---------- */
        [data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,0.09);
            border-radius: 12px;
            background: rgba(255,255,255,0.02);
        }

        /* ---------- Output block ---------- */
        .output-block {
            background: rgba(255,255,255,0.03);
            border-left: 3px solid #a855f7;
            padding: 1rem 1.3rem;
            border-radius: 0 12px 12px 0;
            color: #e2e8f0;
            font-size: 0.95rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }

        /* ---------- Empty state ---------- */
        .empty-state {
            text-align: center;
            padding: 3rem 1.8rem;
        }
        .empty-state h3 {
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        }
        .empty-state p {
            color: #94a3b8;
            max-width: 420px;
            margin: 0 auto;
        }

        /* ---------- Flashcard ---------- */
        .flashcard-wrap {
            display: flex;
            justify-content: center;
            margin: 0.5rem 0 1.2rem 0;
        }
        .flashcard {
            width: 100%;
            max-width: 560px;
            min-height: 230px;
            border-radius: 18px;
            padding: 2rem 2.2rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            cursor: pointer;
            position: relative;
        }
        .flashcard.question {
            background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(168,85,247,0.18));
            border: 1.5px solid rgba(168,85,247,0.4);
        }
        .flashcard.answer {
            background: linear-gradient(135deg, rgba(34,197,94,0.16), rgba(16,185,129,0.16));
            border: 1.5px solid rgba(34,197,94,0.4);
        }
        .flashcard .eyebrow {
            position: absolute;
            top: 1rem;
            left: 1.2rem;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #94a3b8;
        }
        .flashcard .body-text {
            color: #f1f5f9;
            font-size: 1.18rem;
            font-weight: 600;
            line-height: 1.55;
        }
        .flashcard .hint {
            margin-top: 1.1rem;
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 500;
        }
        .flash-progress {
            text-align: center;
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Session State
# ----------------------------
for key, default in {
    "pdf_text": "",
    "summary": "",
    "mcqs": "",
    "flashcards": [],
    "qa_history": [],
    "pdf_name": "",
    "page_count": 0,
    "flash_index": 0,
    "flash_flipped": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def extract_json_array(raw_text):
    """Pull a JSON array out of a model response, stripping any markdown fences."""
    cleaned = re.sub(r"```json|```", "", raw_text).strip()
    match = re.search(r"\[.*\]", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(0)
    return json.loads(cleaned)


# ----------------------------
# Hero
# ----------------------------
st.markdown(
    """
    <div class="hero">
        <h1>📚 AI Study Buddy</h1>
        <p>Upload your study material and let AI generate summaries, quizzes,
        flashcards, and instant answers — straight from your own notes.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Upload — main page
# ----------------------------
st.markdown('<div class="upload-card">', unsafe_allow_html=True)
st.markdown('<div class="upload-title">📤 Upload your PDF</div>', unsafe_allow_html=True)
pdf = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Main Logic
# ----------------------------
if pdf:
    if st.session_state.pdf_name != pdf.name:
        reader = PdfReader(pdf)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
        st.session_state.pdf_text = text
        st.session_state.pdf_name = pdf.name
        st.session_state.page_count = len(reader.pages)
        # reset previous generations for the new file
        st.session_state.summary = ""
        st.session_state.mcqs = ""
        st.session_state.flashcards = []
        st.session_state.qa_history = []
        st.session_state.flash_index = 0
        st.session_state.flash_flipped = False

    text = st.session_state.pdf_text

    st.markdown(
        f'<div class="status-chip">✅ {pdf.name} uploaded successfully</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="stat-box"><div class="num">{st.session_state.page_count}</div>'
            f'<div class="lbl">Pages</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-box"><div class="num">{len(text):,}</div>'
            f'<div class="lbl">Characters extracted</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        word_count = len(text.split())
        st.markdown(
            f'<div class="stat-box"><div class="num">{word_count:,}</div>'
            f'<div class="lbl">Words</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    with st.expander("👀 View Extracted Text"):
        st.write(text[:2000] + ("..." if len(text) > 2000 else ""))

    st.write("")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📝 Summary", "❓ MCQs", "🃏 Flashcards", "💬 Ask Questions"]
    )

    # ---- Summary Tab ----
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Summary</span>', unsafe_allow_html=True)
        st.markdown("<h3>Generate a Summary</h3>", unsafe_allow_html=True)
        st.markdown('<p class="desc">Get a simple, student-friendly summary of your material.</p>', unsafe_allow_html=True)
        if st.button("✨ Generate Summary", key="summary_btn"):
            with st.spinner("Summarizing your material..."):
                response = model.generate_content(
                    f"""
                    Summarize the following study material in simple student-friendly language:
                    {text}
                    """
                )
                st.session_state.summary = response.text
        if st.session_state.summary:
            st.markdown(f'<div class="output-block">{st.session_state.summary}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- MCQs Tab ----
    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Practice</span>', unsafe_allow_html=True)
        st.markdown("<h3>Test Yourself with MCQs</h3>", unsafe_allow_html=True)
        st.markdown('<p class="desc">Generate 10 multiple choice questions to check your understanding.</p>', unsafe_allow_html=True)
        if st.button("✨ Generate MCQs", key="mcq_btn"):
            with st.spinner("Creating MCQs..."):
                mcq_response = model.generate_content(
                    f"""
                    Generate 10 multiple choice questions from the following study material.
                    For each question provide:
                    Question
                    Option A
                    Option B
                    Option C
                    Option D
                    Correct Answer

                    Study Material:
                    {text}
                    """
                )
                st.session_state.mcqs = mcq_response.text
        if st.session_state.mcqs:
            st.markdown(f'<div class="output-block">{st.session_state.mcqs}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Flashcards Tab ----
    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Revision</span>', unsafe_allow_html=True)
        st.markdown("<h3>Quick-Review Flashcards</h3>", unsafe_allow_html=True)
        st.markdown('<p class="desc">Click a card to flip it. Use Previous / Next to move through the deck.</p>', unsafe_allow_html=True)

        if st.button("✨ Generate Flashcards", key="flash_btn"):
            with st.spinner("Building flashcards..."):
                flashcard_response = model.generate_content(
                    f"""
                    Create exactly 10 flashcards from the study material below.
                    Respond with ONLY a valid JSON array, no markdown fences, no extra text.
                    Each item must be an object with exactly two keys: "question" and "answer".
                    Keep each question and answer short — one or two sentences max.

                    Study Material:
                    {text}
                    """
                )
                try:
                    cards = extract_json_array(flashcard_response.text)
                    cards = [
                        c for c in cards
                        if isinstance(c, dict) and "question" in c and "answer" in c
                    ]
                    st.session_state.flashcards = cards
                    st.session_state.flash_index = 0
                    st.session_state.flash_flipped = False
                    if not cards:
                        st.error("Couldn't parse flashcards from the response. Try again.")
                except (json.JSONDecodeError, AttributeError):
                    st.error("Couldn't parse flashcards from the response. Try again.")

        cards = st.session_state.flashcards
        if cards:
            total = len(cards)
            idx = st.session_state.flash_index
            current = cards[idx]

            st.markdown(
                f'<div class="flash-progress">Card {idx + 1} of {total}</div>',
                unsafe_allow_html=True,
            )

            flipped = st.session_state.flash_flipped
            face_class = "answer" if flipped else "question"
            eyebrow = "ANSWER" if flipped else "QUESTION"
            body = current["answer"] if flipped else current["question"]

            st.markdown(
                f"""
                <div class="flashcard-wrap">
                    <div class="flashcard {face_class}">
                        <span class="eyebrow">{eyebrow}</span>
                        <div class="body-text">{body}</div>
                        <div class="hint">{'Click "Flip Card" to see the question' if flipped else 'Click "Flip Card" to reveal the answer'}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            nav1, nav2, nav3 = st.columns([1, 1.2, 1])
            with nav1:
                if st.button("⬅ Previous", key="flash_prev", disabled=(idx == 0)):
                    st.session_state.flash_index -= 1
                    st.session_state.flash_flipped = False
                    st.rerun()
            with nav2:
                if st.button("🔄 Flip Card", key="flash_flip"):
                    st.session_state.flash_flipped = not st.session_state.flash_flipped
                    st.rerun()
            with nav3:
                if st.button("Next ➡", key="flash_next", disabled=(idx == total - 1)):
                    st.session_state.flash_index += 1
                    st.session_state.flash_flipped = False
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Q&A Tab ----
    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<span class="section-label">Q&amp;A</span>', unsafe_allow_html=True)
        st.markdown("<h3>Ask Anything from the PDF</h3>", unsafe_allow_html=True)
        st.markdown('<p class="desc">Ask a direct question — answers come strictly from your uploaded material.</p>', unsafe_allow_html=True)
        question = st.text_input(
            "Enter your question",
            placeholder="e.g. What is the main theory discussed in chapter 2?",
            label_visibility="collapsed",
        )
        if st.button("🔍 Get Answer", key="qa_btn"):
            if question.strip():
                with st.spinner("Finding your answer..."):
                    answer = model.generate_content(
                        f"""
                        You are a study assistant.
                        Use ONLY the information from the study material below to answer.

                        Study Material:
                        {text}

                        Question:
                        {question}
                        """
                    )
                    st.session_state.qa_history.insert(0, (question, answer.text))
            else:
                st.warning("Please enter a question first.")

        if st.session_state.qa_history:
            st.write("")
            st.markdown("**💬 Q&A History**")
            for q, a in st.session_state.qa_history:
                with st.expander(f"Q: {q}"):
                    st.markdown(f'<div class="output-block">{a}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class="card empty-state">
            <h3>👋 Get Started</h3>
            <p>Upload a PDF above to unlock summaries, MCQs, flashcards, and Q&amp;A.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )