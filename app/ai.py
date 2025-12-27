import os
import json
import base64
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash-exp")  # FREE tier model


# AI Helper Functions using Gemini
def get_ai_estimate(job_description, customer_address):
    """Use Gemini to generate a cost estimate"""
    try:
        prompt = (
            "You are a gutter installation and repair expert.\n"
            "Based on this job description, provide a detailed cost estimate.\n\n"
            f"Job Description: {job_description}\n"
            f"Property Address: {customer_address}\n\n"
            "Provide:\n"
            "1. Estimated labor hours\n"
            "2. Materials needed (gutters, downspouts, fasteners, etc.)\n"
            "3. Cost breakdown\n"
            "4. Total estimate range (low-high)\n"
            "5. Any potential complications or considerations\n\n"
            "Format your response as a clear, professional estimate."
        )

        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating estimate: {str(e)}"


def analyze_photo(photo_base64, context=""):
    """Use Gemini Vision to analyze a job site photo"""
    try:
        # Gemini expects image data without the data:image prefix
        if "," in photo_base64:
            image_data = photo_base64.split(",")[1]
        else:
            image_data = photo_base64

        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)

        prompt = (
            "Analyze this gutter-related photo. Identify:\n"
            "1. Current condition (damage, rust, sagging, clogs)\n"
            "2. Type of gutters (K-style, half-round, etc.)\n"
            "3. Approximate measurements if visible\n"
            "4. Recommended repairs or replacements\n"
            "5. Urgency level (low/medium/high)\n\n"
            f"Context: {context}\n\n"
            "Provide a detailed professional assessment."
        )

        # Upload the image and generate content
        response = gemini_model.generate_content(
            [prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
        )
        return response.text

    except Exception as e:
        return f"Error analyzing photo: {str(e)}"


def suggest_schedule(jobs_data, new_job_address):
    """Use Gemini to suggest optimal scheduling"""
    try:
        prompt = f"""Given these upcoming jobs: {json.dumps(jobs_data)}

New job location: {new_job_address}

Suggest the best date to schedule this job considering:
1. Route optimization (group nearby jobs)
2. Current workload
3. Weather considerations
4. Efficiency

Respond with just a date in YYYY-MM-DD format and brief reason."""

        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception:
        return None
