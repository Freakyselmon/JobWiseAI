from google import genai
import re
import time

# Initialize the genai client with your API key
client = genai.Client(api_key="AIzaSyCPmIO_4GfvaFW61wabuPmaBe-ivVBANaE")  # Replace with your actual API key

def generate_questions_and_answers(job_title):
    prompt = (
        f"Generate 5 technical interview questions for a '{job_title}' position. "
        f"Each question should begin with a question wordsorce (e.g., What, How, Why) and end with a question mark. "
        f"Only generate the questions, and number them from 1 to 5. Do not include any additional text or information."
    )

    try:
        # Generate interview questions
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        generated_text = response.text.strip()

        # Extract questions
        questions = re.findall(r'\d+\.\s*(.*?\?)', generated_text)
        questions_and_answers = []

        # Generate answers for each question
        for question in questions:
            answer_prompt = f"Provide a concise answer for the following question: {question}"
            answer_response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=answer_prompt,
            )
            answer = answer_response.text.strip()
            questions_and_answers.append((question, answer))

        return questions_and_answers

    except Exception as e:
        # Log the error message for debugging purposes
        print(f"Error generating interview questions: {e}")
        return [f"Error generating interview questions: {e}"]

# Test the function
if __name__ == "__main__":
    job_title = "Data Scientist"
    
    try:
        result = generate_questions_and_answers(job_title)

        if isinstance(result, list) and result[0].startswith("Error"):
            print(result[0])  # Print the error if it's in the result
        else:
            for idx, (q, a) in enumerate(result, start=1):
                print(f"Question {idx}: {q}")
                print(f"Answer {idx}: {a}")
                print("-" * 40)

    except Exception as e:
        print(f"An error occurred: {e}")
