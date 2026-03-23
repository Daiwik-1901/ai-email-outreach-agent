from .config import GEMINI_API_KEY

def generate_email(name: str, company: str) -> str:
    """
    Generate a personalized professional job inquiry email using Google Gemini.

    Args:
        name (str): The recruiter's name
        company (str): The company name

    Returns:
        str: The generated email body
    """
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    prompt = f"""
    Generate a personalized, professional job inquiry email addressed to {name} at {company}.
    The email should be polite, concise, and highlight the Daiwik Saxena's skills in competitive programming, backend development, and AI/machine learning projects.
    Structure the email with a greeting, introduction, skills mention, call to action, and professional closing.
    Keep it under 200 words.
    """

    # Use gemini-2.5-flash which is available and performant for this task
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()