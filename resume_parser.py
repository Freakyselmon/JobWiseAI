import fitz  # PyMuPDF
import re
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Initialize the question-generation pipeline
qg = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text += page.get_text("text")  # Extract text from each page
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"Error reading the PDF file: {e}")
    return text

def extract_skills_section(text):
    """Extract the skills section from the resume."""
    skill_headers = ['skills', 'technical skills', 'core competencies', 'key skills']
    skill_section = None
    for header in skill_headers:
        match = re.search(rf'{header}.*?(?=\n[A-Z]|\n$)', text, re.IGNORECASE | re.DOTALL)
        if match:
            skill_section = match.group(0)
            break
    return skill_section

def extract_skills(text):
    """Extract potential skills from the skills section of the resume."""
    if not text:
        return []

    # Flat list of known skills
    known_skills = set(map(str.lower, """
    Python, Java, Machine Learning, Data Analysis, Algorithms, Software Development,
    SQL, Excel, Communication, Reporting, Project Management, Business Intelligence,
    TensorFlow, React, Node.js, HTML, CSS, R, Keras, Tableau, Power BI,
    Docker, Kubernetes, AWS, DevOps, UI/UX Design, Figma, Agile, Scrum,
    C++, JavaScript, PHP, MySQL, Django, Flask, MongoDB, Git, Linux
    """.replace('\n', '').split(',')))
    known_skills = {skill.strip() for skill in known_skills}

    # Tokenize and clean
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [
        word for word in words
        if word.isalpha() and word not in stop_words and word in known_skills
    ]

    return list(set(filtered_words))  # Remove duplicates

def generate_questions_based_on_skills(skills):
    """Generate interview questions based on the extracted skills."""
    skills_text = ', '.join(skills)
    prompt = f"Generate 5 technical interview questions based on these skills: {skills_text}."
    response = qg(prompt, max_length=200, do_sample=True)[0]['generated_text']
    questions = [q.strip() for q in response.split('.') if '?' in q]
    return questions[:5]

# --------- MAIN EXECUTION ---------
file_path = "/Users/shabbirshaikh/Documents/JobWiseAI/sample_resume.pdf"
resume_text = extract_text_from_pdf(file_path)

if not resume_text.strip():
    print("No extractable text found in the PDF. It may be image-based or empty.")
else:
    print("Resume text successfully extracted.")

    skill_section = extract_skills_section(resume_text)
    if skill_section:
        print("\n🔍 Skills Section Found:")
        print(skill_section)

        skills = extract_skills(skill_section)
        if skills:
            print("\n✅ Extracted Skills:", skills)

            questions = generate_questions_based_on_skills(skills)
            print("\n📌 Generated Interview Questions:")
            for q in questions:
                print("•", q)
        else:
            print("⚠️ No recognizable skills found in the skills section.")
    else:
        print("⚠️ Skills section not found in the resume.")
