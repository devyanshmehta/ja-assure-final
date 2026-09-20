import os
import time
import sqlite3
from google import genai
from google.genai.errors import ServerError
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.6-flash"

def call_gemini_with_retry(prompt: str, retries=3, delay=2) -> str:
    """Helper to safely call Gemini API with auto-retry on 503 traffic spikes."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            return response.text.strip()
        except ServerError as e:
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                raise e

def generate_marketing_content(brand: str, platform: str, language: str, prompt_topic: str) -> str:
    """Generates localized marketing draft based on user prompt."""
    prompt = f"""
    You are an expert marketing agent for the brand '{brand}'.
    Write a {platform} post in {language} about: '{prompt_topic}'.
    Keep the tone engaging, professional, and suited for {platform}.
    Do NOT include meta-commentary, just return the content body.
    """
    return call_gemini_with_retry(prompt)

def check_compliance(content: str, brand: str) -> dict:
    """Evaluates content against insurance regulatory compliance guidelines."""
    conn = sqlite3.connect("ja_assure.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rejection_tag, human_notes FROM feedback_memory WHERE brand = ?", (brand,))
    past_feedback = cursor.fetchall()
    conn.close()

    memory_context = ""
    if past_feedback:
        memory_context = "PAST REJECTION HISTORY TO AVOID:\n" + "\n".join(
            [f"- Tag: {item[0]} | Note: {item[1]}" for item in past_feedback]
        )

    compliance_prompt = f"""
    You are a strictly regulated Insurance Compliance Auditor for brand: '{brand}'.
    Evaluate the following promotional draft for compliance violations:
    
    CONTENT DRAFT:
    \"\"\"{content}\"\"\"
    
    {memory_context}
    
    RULES TO ENFORCE:
    1. No guaranteed returns or absolute promises on claims without disclaimer.
    2. Must be transparent and truthful.
    3. Respect past rejection feedback if provided above.
    
    Respond in EXACTLY this format (3 lines only):
    STATUS: [APPROVED or REJECTED]
    TAG: [Compliant OR Violation Category e.g. Misleading Claim, Missing Disclaimer]
    REASON: [Brief 1-sentence explanation]
    """

    response_text = call_gemini_with_retry(compliance_prompt)
    lines = [line.strip() for line in response_text.split("\n") if line.strip()]
    
    status = "REJECTED"
    tag = "Unknown"
    reason = "Failed compliance parsing."

    for line in lines:
        if line.startswith("STATUS:"):
            status = line.replace("STATUS:", "").strip()
        elif line.startswith("TAG:"):
            tag = line.replace("TAG:", "").strip()
        elif line.startswith("REASON:"):
            reason = line.replace("REASON:", "").strip()

    return {
        "status": status,
        "tag": tag,
        "reason": reason
    }