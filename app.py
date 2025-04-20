import streamlit as st
from resume_parser import extract_text_from_pdf, extract_skills
from recommender import recommend_jobs
from interview import generate_questions_and_answers
from courses import get_courses
from fpdf import FPDF
import ollama

# Streamlit Page Setup
st.set_page_config(page_title="JobWiseAI – Free AI Career Assistant", layout="centered")
st.title("🤖 JobWiseAI – Free AI Career Assistant")
st.markdown("Upload your resume to get job recommendations, mock interview questions, and free learning resources.")

# File uploader to get the resume
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Skill Extraction
    st.subheader("1. ✅ Extracted Skills")
    text = extract_text_from_pdf("temp.pdf")
    skills = extract_skills(text)

    if not skills:
        st.warning("Please upload a resume with technical or professional skills.")
    else:
        st.success(", ".join(skills))

        # Step 2: Job Recommendations
        st.subheader("2. 🎯 Job Role Recommendations")
        recommended = recommend_jobs(skills)

        if recommended:
            st.write("Top Recommended Jobs:")
            job_titles = []
            for job in recommended:
                st.markdown(f"**🔹 {job['jobtitle']}** — Match: `{job['score']}`")
                st.caption(f"Required Skills: {job['skills']}")
                job_titles.append(job['jobtitle'])
        else:
            st.error("No recommendations found.")
            job_titles = []

        # Step 3: Mock Interview Questions
        st.subheader("3. 🧠 Mock Interview Questions")
        if job_titles:
            job_title = st.selectbox("Choose a role for mock questions", job_titles)

            try:
                qa_pairs = generate_questions_and_answers(job_title)
                if qa_pairs:
                    st.markdown("### 📚 Questions & Answers")
                    formatted_text = ""

                    for idx, (question, answer) in enumerate(qa_pairs, start=1):
                        question = question.strip()
                        answer = answer.strip()

                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; border-radius: 12px; padding: 20px; margin-bottom: 20px; background-color: #f9f9f9; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                                <div style="font-weight: 600; color: #333; font-size: 18px; margin-bottom: 10px;">✅ Q{idx}: {question}</div>
                                <div style="margin-left: 10px; color: #444; font-size: 16px; line-height: 1.6;">
                                    {answer.replace('\n', '<br/>')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        formatted_text += f"Q{idx}: {question}\nA: {answer}\n\n"

                    # Download buttons
                    st.download_button("⬇️ Download Q&A as TXT", formatted_text, file_name="interview_questions.txt", mime="text/plain")

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    for line in formatted_text.strip().split("\n"):
                        pdf.multi_cell(0, 10, line)
                    pdf_output = pdf.output(dest='S').encode('latin1')
                    st.download_button("⬇️ Download Q&A as PDF", pdf_output, file_name="interview_questions.pdf", mime="application/pdf")
                else:
                    st.warning("No questions generated.")
            except Exception as e:
                st.error(f"Error generating interview questions: {e}")
        else:
            st.info("Please get job recommendations first.")

        # Step 4: Free Learning Resources
        st.subheader("4. 📚 Free YouTube Courses Based on Your Skills")
        if skills:
            selected_skills = st.multiselect("Select one or more skills to view free courses", skills)
            if selected_skills:
                for selected_skill in selected_skills:
                    with st.spinner(f"Searching YouTube courses for '{selected_skill}'..."):
                        try:
                            course_results = get_courses(selected_skill)
                            if course_results:
                                st.markdown(f"#### 📘 Courses for **{selected_skill}**:")
                                for course in course_results:
                                    st.markdown(f"• [{course['title']}]({course['link']})")
                            else:
                                st.warning(f"No courses found for: {selected_skill}")
                        except Exception as e:
                            st.error(f"Failed to fetch courses for {selected_skill}: {e}")
        else:
            st.info("No skills found yet. Please upload your resume first.")

        # Step 5: Auto-Generated Cover Letter
        st.subheader("5. 📝 Auto-Generated Cover Letter")
        user_name = st.text_input("Enter your name:")
        if user_name and job_titles:
            selected_job_title = st.selectbox("Select job title for cover letter", job_titles)
            if st.button("Generate Cover Letter"):
                with st.spinner("Crafting your personalized cover letter..."):
                    skills_text = ', '.join(skills)
                    prompt = f"""
Write a professional cover letter for a candidate named {user_name} applying for the position of {selected_job_title}.
The candidate has experience with the following skills: {skills_text}.
Keep the tone formal, enthusiastic, and concise.
"""
                    try:
                        response = ollama.chat(model='llama3:8b', messages=[{"role": "user", "content": prompt}])
                        cover_letter = response['message']['content']
                        st.text_area("📄 Your Cover Letter", value=cover_letter, height=300)

                        st.download_button("⬇️ Download Cover Letter as TXT", cover_letter, file_name="cover_letter.txt", mime="text/plain")

                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        for line in cover_letter.split("\n"):
                            pdf.multi_cell(0, 10, line)
                        pdf_output = pdf.output(dest='S').encode('latin1')
                        st.download_button("⬇️ Download Cover Letter as PDF", pdf_output, file_name="cover_letter.pdf", mime="application/pdf")

                        st.success("Cover letter generated successfully!")
                    except Exception as e:
                        st.error(f"Failed to generate cover letter using Ollama: {e}")
        else:
            st.info("Please enter your name and select a job title to generate a cover letter.")
else:
    st.info("Please upload your resume to begin.")
