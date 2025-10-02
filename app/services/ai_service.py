import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

class AIService:
    @staticmethod
    async def enhance_text(text: str, context: str = "") -> str:
        prompt = f"Enhance the following text for a resume {context}: {text}"
        response = model.generate_content(prompt)
        return response.text.strip()

    @staticmethod
    async def analyze_resume(resume_content: dict, job_desc: str = None) -> dict:
        if job_desc:
            prompt = f"Analyze this resume against the job description and suggest improvements: Resume: {resume_content} Job: {job_desc}"
        else:
            prompt = f"Provide a general analysis of this resume: {resume_content}"
        
        response = model.generate_content(prompt)
        return {"analysis": response.text.strip()}

    @staticmethod
    async def generate_prep_kit(resume: dict, job_desc: dict, experience: str) -> dict:
        prompt = f"Generate a job preparation kit based on resume: {resume}, job description: {job_desc}, experience: {experience}. Include email draft, cover letter, HR questions, managerial questions, technical questions, DSA questions with solutions in C++/Java/Python, puzzles."
        
        response = model.generate_content(prompt)
        content = response.text
        # Parse the response into structured format
        return {"kit": content}  # Placeholder, need to parse properly