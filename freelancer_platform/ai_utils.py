import requests
import json
import os

# Use the provided Gemini API key
GEMINI_API_KEY = "AIzaSyB4Owr1pklmI7WZUE5PqM07HGGZ3drBjRE"

# Use the correct Gemini model endpoint for free content generation
GEMINI_MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_skill_recommendations(skill):
    """
    Get AI-powered recommendations for a specific skill
    """
    try:
        prompt = f"""
        I have the skill of {skill}. Suggest AI-powered or freelance opportunities I can explore in my local area.
        Include:
        1. Local business opportunities
        2. Certifications that would help
        3. Marketing strategies
        4. Pricing suggestions
        5. Equipment or tools needed
        6. Target customers
        7. Seasonal opportunities
        
        Format the response in a clear, structured way with bullet points.
        Focus on practical, actionable advice for someone in a local community.
        """
        
        response = requests.post(
            GEMINI_MODEL_URL,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and data['candidates']:
                return data['candidates'][0]['content']['parts'][0]['text']
        
        return f"Unable to generate recommendations at this time."
    except Exception as e:
        return f"Unable to generate recommendations at this time. Error: {str(e)}"

def get_similar_skills(skill):
    """
    Get similar skills that might be relevant
    """
    try:
        prompt = f"""
        Given the skill of {skill}, suggest 5-8 related or complementary skills that someone could learn to expand their opportunities.
        Focus on practical, local service skills that are in demand.
        Return only the skill names, one per line.
        """
        
        response = requests.post(
            GEMINI_MODEL_URL,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and data['candidates']:
                text = data['candidates'][0]['content']['parts'][0]['text']
                return [skill.strip() for skill in text.split('\n') if skill.strip()]
        
        return []
    except Exception as e:
        return []

def get_job_matching_score(freelancer_skills, job_required_skills):
    """
    Calculate a matching score between freelancer skills and job requirements
    """
    try:
        prompt = f"""
        Rate the match between these skills on a scale of 1-10:
        
        Freelancer Skills: {freelancer_skills}
        Job Required Skills: {job_required_skills}
        
        Consider:
        - Direct skill matches
        - Related skills
        - Transferable skills
        - Experience level
        
        Return only the number (1-10).
        """
        
        response = requests.post(
            GEMINI_MODEL_URL,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and data['candidates']:
                text = data['candidates'][0]['content']['parts'][0]['text']
                try:
                    return int(text.strip())
                except:
                    return 5  # Default score
        
        return 5  # Default score
    except Exception as e:
        return 5  # Default score