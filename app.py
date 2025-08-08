import streamlit as st
from utils.resume_parser import parse_resume
from utils.question_generator import generate_questions
from utils.context_handler import handle_context

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

def main():
    # ————— 0) Greeting & Rules —————
    st.title("👋 Welcome to TalentScout's AI Hiring Assistant!")
    st.markdown(
        """
        **No pressure, just honest conversation.**  
        I’ll ask **10 questions** based on your skills, projects, education, and experience.  
        Please upload your resume (PDF) to begin.
        """
    )

    # ————— 1) Session State Init —————
    if 'parsed' not in st.session_state:
        st.session_state.parsed = False
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    # ————— 2) Upload & Parse —————
    if not st.session_state.parsed:
        resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
        if not resume_file:
            return  # wait for file

        # file has been uploaded → parse + question generation
        with st.spinner("Parsing resume…"):
            profile = parse_resume(resume_file)
            #st.write("🔍 Parsed profile:", profile)
            # if not profile.get("skills") and not profile.get("projects"):
            #     st.error(
            #         "⚠️ I couldn’t find any skills or projects in your resume. "
            #         "Please make sure it’s a text-based PDF or try another file."
            #     )
            #     return

            qs = generate_questions(profile)
            st.session_state.questions = qs[:10]
            st.session_state.parsed = True

        st.success("✅ Resume parsed and 10 tailored questions generated!")

    # ————— 3) Q&A Loop —————
    total = len(st.session_state.questions)
    idx = st.session_state.current_q

    if idx < total:
        question = st.session_state.questions[idx]
        st.markdown(f"**Question {idx+1} of {total}:** {question}")
        answer = st.text_area("Your answer:", key=f"ans_{idx}")

        if st.button("Submit Answer", key=f"sub_{idx}"):
            st.session_state.answers.append(answer.strip())
            st.session_state.current_q += 1
            st.success("✅ OKAY, LET’S MOVE ON TO THE NEXT QUESTION")
            return
    else:
        st.success("🎉 You've completed all questions! Thank you for your time.")
        st.write("We will review your answers and get back to you soon.")
        end_msg, ended = handle_context("bye")
        if ended:
            st.write(end_msg)

if __name__ == "__main__":
    main()
