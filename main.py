from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, HealthContent, UserInteraction, get_db
from typing import Optional
import os
import requests
import json

app = FastAPI(title="Ama Arogya - Public Health Chatbot API", version="1.0.0")

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Rasa server configuration
RASA_API_URL = "http://localhost:5005"


class ChatRequest(BaseModel):
    message: str
    sender_id: str
    language: Optional[str] = "en"


class ChatResponse(BaseModel):
    response: str
    language: str
    intent: Optional[str] = None


def get_health_content(topic: str, language: str, db: Session):
    """Get health content from database"""
    content = db.query(HealthContent).filter(
        HealthContent.topic == topic,
        HealthContent.language == language
    ).first()
    return content


def log_interaction(sender_id: str, message: str, response: str, intent: str, language: str, db: Session):
    """Log user interaction"""
    interaction = UserInteraction(
        sender_id=sender_id,
        message=message,
        response=response,
        intent=intent,
        language=language
    )
    db.add(interaction)
    db.commit()


async def get_rasa_response(message: str, sender_id: str):
    """Get response from Rasa server"""
    try:
        rasa_payload = {
            "sender": sender_id,
            "message": message
        }

        response = requests.post(
            f"{RASA_API_URL}/webhooks/rest/webhook",
            json=rasa_payload,
            timeout=10
        )

        if response.status_code == 200:
            rasa_responses = response.json()
            if rasa_responses and len(rasa_responses) > 0:
                # Get the first response from Rasa
                return rasa_responses[0].get("text", "I'm sorry, I couldn't understand that.")
            else:
                return "I'm sorry, I couldn't understand that. Please ask about health-related topics."
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa: {e}")
        return None


def get_fallback_response(message: str, language: str):
    """Fallback responses when Rasa is not available"""
    message_lower = message.lower()

    # Check for specific topics and provide fallback responses
    if any(word in message_lower for word in ["fever", "ज्वर", "ଜ୍ବର", "jwor", "bukhar"]):
        if language == "hi":
            return "बुखार के लिए पर्याप्त आराम लें और हाइड्रेटेड रहें। यदि बुखार 3 दिनों से अधिक समय तक बना रहता है तो डॉक्टर से संपर्क करें।"
        elif language == "or":
            return "ଜ୍ବର ପାଇଁ ଯଥେଷ୍ଟ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଏବଂ ପାଣି ପିଅନ୍ତୁ। ଯଦି ଜ୍ବର 3 ଦିନରୁ ଅଧିକ ସମୟ ପାଇଁ ରହିଥାଏ ତେବେ ଡାକ୍ତରଙ୍କ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ।"
        else:
            return "For fever, take adequate rest and stay hydrated. If fever persists for more than 3 days, consult a doctor."

    elif any(word in message_lower for word in ["headache", "सिरदर्द", "ମାଥା ବଥା", "matharu batha"]):
        if language == "hi":
            return "सिरदर्द के लिए आराम और ठंडी पट्टी सहायक होती है।"
        elif language == "or":
            return "ମାଥା ବଥା ପାଇଁ ବିଶ୍ରାମ ଓ ଠଣ୍ଡା ସେକ ସାହାଯ୍ୟକାରୀ।"
        else:
            return "For headache, rest in a dark room and apply cold compress."

    elif any(word in message_lower for word in ["pregnancy", "maternal", "गर्भावस्था", "ଗର୍ଭାବସ୍ଥା"]):
        if language == "hi":
            return "गर्भावस्था के दौरान नियमित जांच और संतुलित आहार महत्वपूर्ण है।"
        elif language == "or":
            return "ଗର୍ଭାବସ୍ଥା ସମୟରେ ନିୟମିତ ଯାଞ୍ଚ ଏବଂ ସନ୍ତୁଲିତ ଆହାର ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ।"
        else:
            return "During pregnancy, regular check-ups and balanced diet are important."

    elif any(word in message_lower for word in ["vaccination", "टीका", "ଟୀକା", "tikakaran"]):
        if language == "hi":
            return "टीकाकरण बच्चों के स्वास्थ्य के लिए महत्वपूर्ण है। नियमित टीकाकरण कार्यक्रम का पालन करें।"
        elif language == "or":
            return "ଟୀକାକରଣ ପିଲାମାନଙ୍କ ସ୍ୱାସ୍ଥ୍ୟ ପାଇଁ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ। ନିୟମିତ ଟୀକାକରଣ କାର୍ଯ୍ୟକ୍ରମର ଅନୁସରଣ କରନ୍ତୁ।"
        else:
            return "Vaccination is important for children's health. Follow the regular vaccination schedule."

    elif any(word in message_lower for word in ["hello", "hi", "namaste", "ନମସ୍କାର", "namaskar"]):
        if language == "hi":
            return "नमस्ते! मैं अमा आरोग्य हूं, आपका स्वास्थ्य सहायक। आपकी कैसे मदद कर सकता हूं?"
        elif language == "or":
            return "ନମସ୍କାର! ମୁଁ ଅମା ଆରୋଗ୍ୟ, ଆପଣଙ୍କର ସ୍ୱାସ୍ଥ୍ୟ ସହାୟକ। ମୁଁ ଆପଣଙ୍କୁ କିପରି ସାହାଯ୍ୟ କରିପାରେ?"
        else:
            return "Hello! I'm Ama Arogya, your health assistant. How can I help you today?"

    else:
        if language == "hi":
            return "मैं आपकी मदद करने के लिए यहाँ हूँ। कृपया स्वास्थ्य संबंधी प्रश्न पूछें।"
        elif language == "or":
            return "ମୁଁ ଆପଣଙ୍କୁ ସାହାଯ୍ୟ କରିବା ପାଇଁ ଏଠାରେ ଅଛି। ଦୟାକରି ସ୍ୱାସ୍ଥ୍ୟ ସମ୍ବନ୍ଧୀୟ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ।"
        else:
            return "I'm here to help you with health-related questions. Please ask about symptoms, treatments, or health advice."


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handle chatbot messages using Rasa model with fallback
    """
    message = request.message
    language = request.language
    sender_id = request.sender_id

    # Try to get response from Rasa first
    rasa_response = await get_rasa_response(message, sender_id)

    if rasa_response:
        response = rasa_response
        intent = "rasa_processed"
    else:
        # Fall back to hardcoded responses if Rasa is unavailable
        response = get_fallback_response(message, language)
        intent = "fallback"

    # Log the interaction
    log_interaction(sender_id, message, response, intent, language, db)

    return ChatResponse(
        response=response,
        language=language,
        intent=intent
    )


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get basic statistics
    """
    total_interactions = db.query(UserInteraction).count()
    language_stats = db.query(UserInteraction.language, func.count(
        UserInteraction.id)).group_by(UserInteraction.language).all()

    return {
        "total_interactions": total_interactions,
        "language_distribution": dict(language_stats)
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """
    Serve the analytics dashboard
    """
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
@app.get("/demo", response_class=HTMLResponse)
async def get_demo():
    """
    Serve the demo frontend interface
    """
    frontend_file = os.path.join(os.path.dirname(
        __file__), "frontend", "index.html")
    if os.path.exists(frontend_file):
        with open(frontend_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return HTMLResponse("Demo frontend not found. Please ensure frontend files are in the 'frontend' directory.", status_code=404)
