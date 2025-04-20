import requests

def generate_cover_letter_llama(name, job_title, skills):
    prompt = f"""
    Write a professional cover letter for {name} applying for the role of {job_title}.
    Highlight these skills: {', '.join(skills)}.
    Keep it concise, formal, and impressive.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data["response"]

# Example usage
if __name__ == "__main__":
    name = "Ayan"
    job_title = "Data Analyst"
    skills = ["Python", "SQL", "Machine Learning"]

    cover_letter = generate_cover_letter_llama(name, job_title, skills)
    print("\nGenerated Cover Letter:\n")
    print(cover_letter)
