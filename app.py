
import streamlit as st
from datetime import datetime

from study_agent import run_study_agent


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Study Agent 2.0",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "study_mode" not in st.session_state:
    st.session_state.study_mode = "Explain a topic"

if "answer" not in st.session_state:
    st.session_state.answer = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# --------------------------------------------------
# 3. NAVIGATION CALLBACK
# --------------------------------------------------

def open_workspace(mode):
    st.session_state.study_mode = mode
    st.session_state.page = "Study Workspace"


# --------------------------------------------------
# 4. CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background-color: #111C32;
    border-right: 1px solid #263653;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(120deg, #14294B, #174A87);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid #2863A6;
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 34px;
}

.hero p {
    color: #D5E5FA;
    font-size: 16px;
}

.feature-card {
    background: #15233B;
    border: 1px solid #293D5D;
    padding: 20px;
    border-radius: 14px;
    min-height: 125px;
}

.feature-card h3 {
    color: #60A5FA;
    font-size: 18px;
}

.feature-card p {
    color: #CBD5E1;
    font-size: 14px;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #3B82F6;
    color: white;
}

div[data-baseweb="select"] > div,
.stTextArea textarea {
    background-color: #15233B;
    color: white;
}

h1, h2, h3 {
    color: #F1F5F9;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 5. SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 📚 Study Agent 2.0")

    st.caption("AI-powered learning workspace")

    st.divider()

    st.radio(
        "Navigation",
        ["Dashboard", "Study Workspace", "Recent Sessions"],
        key="page",
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### About")

    st.caption(
        "Your personal AI study assistant for "
        "understanding, summarizing and revising topics."
    )

    st.caption("Powered by CrewAI + Groq")


# --------------------------------------------------
# 6. DASHBOARD
# --------------------------------------------------

if st.session_state.page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to Your Learning Space 👋</h1>
        <p>
        Learn smarter, understand difficult concepts,
        and prepare for your studies with your AI Study Agent.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("What would you like to do today?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📘 Explain a Topic</h3>
            <p>Understand difficult concepts in simple language.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Start Explanation",
            use_container_width=True,
            on_click=open_workspace,
            args=("Explain a topic",)
        )

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Create Summary</h3>
            <p>Turn complex topics into concise study notes.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Create Summary",
            use_container_width=True,
            on_click=open_workspace,
            args=("Summarize",)
        )

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>❓ Generate Quiz</h3>
            <p>Test your knowledge with practice questions.</p>
        </div>
        """, unsafe_allow_html=True)

        st.button(
            "Generate Quiz",
            use_container_width=True,
            on_click=open_workspace,
            args=("Generate quiz questions",)
        )

    st.divider()

    st.subheader("Your Study Activity")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Study Sessions",
            len(st.session_state.history)
        )

    with col2:
        st.metric(
            "Available Study Modes",
            5
        )


# --------------------------------------------------
# 7. STUDY WORKSPACE
# --------------------------------------------------

elif st.session_state.page == "Study Workspace":

    st.title("📖 Study Workspace")

    st.write(
        "Choose a study mode and enter your topic or question."
    )

    study_modes = [
        "Explain a topic",
        "Summarize",
        "Generate quiz questions",
        "Ask a study question",
        "Create revision notes"
    ]

    study_mode = st.selectbox(
        "Select Study Mode",
        study_modes,
        key="study_mode"
    )

    user_input = st.text_area(
        "Your Topic or Question",
        height=160,
        placeholder="Example: Explain reciprocal inhibition in simple language."
    )

    if st.button("✨ Generate Answer", use_container_width=True):

        if not user_input.strip():

            st.warning("Please enter a topic or question.")

        else:

            request = f"""
            Study mode: {study_mode}

            Student request:
            {user_input}
            """

            with st.spinner("Your AI Study Agent is working..."):

                try:

                    result = run_study_agent(request)

                    answer = str(result)

                    st.session_state.answer = answer

                    st.session_state.history.insert(0, {
                        "mode": study_mode,
                        "question": user_input,
                        "answer": answer,
                        "time": datetime.now().strftime(
                            "%d %b %Y, %I:%M %p"
                        )
                    })

                except Exception as e:

                    st.error(
                        "Something went wrong. "
                        "Please check your API key and configuration."
                    )

                    st.exception(e)

    if st.session_state.answer:

        st.divider()

        st.subheader("✨ Your AI-Generated Answer")

        with st.container(border=True):
            st.markdown(st.session_state.answer)


# --------------------------------------------------
# 8. RECENT SESSIONS
# --------------------------------------------------

elif st.session_state.page == "Recent Sessions":

    st.title("🕘 Recent Study Sessions")

    st.write("Review your previous study activity.")

    if not st.session_state.history:

        st.info(
            "No study sessions yet. "
            "Start learning in the Study Workspace."
        )

    else:

        for session in st.session_state.history:

            with st.expander(
                f"{session['mode']} — {session['time']}"
            ):

                st.markdown("**Your Question:**")

                st.write(session["question"])

                st.markdown("**AI Answer:**")

                st.markdown(session["answer"])

        if st.button("Clear Session History"):

            st.session_state.history = []
            st.session_state.answer = None

            st.rerun()


# --------------------------------------------------
# 9. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Study Agent 2.0 | AI-powered academic learning assistant"
)
