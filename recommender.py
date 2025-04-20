import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Hardcoded job dataset
job_data = [
    {"jobtitle": "Data Scientist", "skills": "python, pandas, sklearn, machine learning, statistics, deep learning, tensorflow, pytorch"},
    {"jobtitle": "Data Analyst", "skills": "sql, excel, powerbi, tableau, data visualization, statistics, data cleaning, reporting"},
    {"jobtitle": "Software Developer", "skills": "java, python, git, problem solving, algorithms, object-oriented programming, software design"},
    {"jobtitle": "Web Developer", "skills": "html, css, javascript, react, nodejs, angular, vue.js, responsive design, git"},
    {"jobtitle": "AI Engineer", "skills": "tensorflow, pytorch, keras, deep learning, neural networks, computer vision, natural language processing"},
    {"jobtitle": "Business Analyst", "skills": "excel, communication, stakeholder management, sql, requirements gathering, business modeling"},
    {"jobtitle": "DevOps Engineer", "skills": "aws, docker, kubernetes, ci/cd, linux, azure, jenkins, automation, infrastructure management"},
    {"jobtitle": "Cybersecurity Analyst", "skills": "network security, firewalls, ethical hacking, risk assessment, penetration testing, threat analysis"},
    {"jobtitle": "Digital Marketer", "skills": "seo, sem, content marketing, analytics, communication, email marketing, social media strategy"},
    {"jobtitle": "Product Manager", "skills": "product roadmap, stakeholder management, analytics, communication, user stories, agile methodology"},
    {"jobtitle": "Cloud Architect", "skills": "cloud computing, aws, azure, gcp, microservices, cloud infrastructure, devops, security protocols"},
    {"jobtitle": "UX/UI Designer", "skills": "user research, wireframing, prototyping, figma, adobe xd, interaction design, usability testing"},
    {"jobtitle": "Mobile App Developer", "skills": "swift, kotlin, flutter, android, iOS, firebase, react native, mobile design patterns"},
    {"jobtitle": "Graphic Designer", "skills": "photoshop, illustrator, inDesign, typography, creativity, branding, logo design, visual communication"},
    {"jobtitle": "Content Writer", "skills": "seo writing, research, blogging, grammar, storytelling, creative writing, content strategy"},
    {"jobtitle": "Teacher", "skills": "subject knowledge, communication, lesson planning, classroom management, student engagement, grading"},
    {"jobtitle": "Customer Support Executive", "skills": "communication skills, problem solving, crm, patience, empathy, conflict resolution, active listening"},
    {"jobtitle": "Sales Executive", "skills": "lead generation, crm, communication, negotiation, closing deals, sales strategies, customer relationship management"},
    {"jobtitle": "HR Executive", "skills": "recruitment, payroll, employee engagement, onboarding, compliance, performance management, conflict resolution"},
    {"jobtitle": "Marketing Manager", "skills": "digital marketing, seo, sem, content strategy, analytics, social media marketing, email campaigns"},
    {"jobtitle": "Financial Analyst", "skills": "excel, financial modeling, forecasting, sql, accounting principles, budgeting, variance analysis"},
    {"jobtitle": "Accountant", "skills": "tally, gst, tax filing, balance sheet, ledger, ms excel, bookkeeping, financial reporting"},
    {"jobtitle": "Medical Transcriptionist", "skills": "typing, english proficiency, medical terminology, audio transcription, time management, attention to detail"},
    {"jobtitle": "Nurse", "skills": "patient care, first aid, emergency response, monitoring vitals, medication, patient education, medical records"},
    {"jobtitle": "Project Manager", "skills": "project planning, budgeting, communication, agile, risk management, team leadership, scheduling"},
    {"jobtitle": "Research Scientist", "skills": "research methodologies, data analysis, laboratory techniques, scientific writing, statistical software"},
    {"jobtitle": "Pharmacist", "skills": "pharmaceutical knowledge, drug interactions, patient counseling, prescription dispensing, inventory management"},
    {"jobtitle": "Civil Engineer", "skills": "structural design, construction management, autocad, project planning, site supervision, materials testing"},
    {"jobtitle": "Mechanical Engineer", "skills": "solidworks, catia, mechanical design, thermodynamics, materials science, product development"},
    {"jobtitle": "Electrical Engineer", "skills": "circuit design, electrical systems, power generation, control systems, signal processing, circuit analysis"},
    {"jobtitle": "Architect", "skills": "autocad, building design, construction management, project planning, architectural drawing, site management"},
    {"jobtitle": "Chef", "skills": "menu planning, food preparation, culinary techniques, kitchen management, food safety, creativity"},
    {"jobtitle": "Librarian", "skills": "cataloging, archiving, information management, research assistance, library software, customer service"},
    {"jobtitle": "Event Planner", "skills": "event coordination, budget management, vendor management, marketing, communication, logistics"},
    {"jobtitle": "Lawyer", "skills": "legal research, client consultation, contract law, case preparation, litigation, negotiation"},
    {"jobtitle": "Photographer", "skills": "photography techniques, editing, lighting, portrait photography, event photography, camera operation"},
    {"jobtitle": "Translator", "skills": "language proficiency, translation software, proofreading, cultural knowledge, interpretation, writing skills"},
    {"jobtitle": "Social Worker", "skills": "counseling, community outreach, case management, social services, crisis intervention, advocacy"},
    {"jobtitle": "Operations Manager", "skills": "operations planning, team management, logistics, process optimization, budgeting, performance monitoring"},
    {"jobtitle": "Construction Manager", "skills": "site management, construction planning, safety protocols, project management, scheduling, cost estimation"},
    {"jobtitle": "Public Relations Specialist", "skills": "media relations, communication strategies, press releases, brand management, social media marketing, crisis communication"},
    {"jobtitle": "Fashion Designer", "skills": "fashion illustration, pattern making, textile knowledge, garment construction, fashion trends, CAD"},
    {"jobtitle": "Interior Designer", "skills": "space planning, interior decor, CAD, color theory, furniture design, client consultation, project management"},
    {"jobtitle": "Real Estate Agent", "skills": "property sales, market research, negotiation, client relations, contract law, property valuation"},
    {"jobtitle": "Sales Manager", "skills": "sales strategy, team leadership, performance tracking, sales training, customer relations, negotiation skills"},
    {"jobtitle": "Business Development Manager", "skills": "strategic planning, lead generation, client acquisition, relationship management, market research, sales forecasting"},
    {"jobtitle": "Entrepreneur", "skills": "business development, leadership, marketing, product development, sales strategy, fundraising"}    
]

# Function to recommend jobs
def recommend_jobs(user_skills, top_n=5):
    user_skills_str = ' '.join(user_skills).lower()

    job_titles = [job["jobtitle"] for job in job_data]
    skill_corpus = [job["skills"] for job in job_data]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(skill_corpus)
    user_vector = vectorizer.transform([user_skills_str])

    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

    job_matches = [
        {
            "jobtitle": job_titles[i],
            "skills": skill_corpus[i],
            "score": round(similarity_scores[i], 2)
        }
        for i in range(len(similarity_scores))
    ]

    sorted_matches = sorted(job_matches, key=lambda x: x["score"], reverse=True)
    return sorted_matches[:top_n]
