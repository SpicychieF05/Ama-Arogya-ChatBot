# Ama Arogya - AI-Driven Health Assistant for Rural Odisha

<div align="center">
  <h3>🏥 Multilingual Health Chatbot for Rural Communities</h3>
  <p>Bridging the health information gap in Odisha with AI-powered assistance</p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
  [![Rasa](https://img.shields.io/badge/Rasa-3.6+-purple.svg)](https://rasa.com)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 🌟 Overview

Ama Arogya is an intelligent, multilingual health chatbot designed specifically for rural and semi-urban populations in Odisha, India. Built with FastAPI and Rasa, the system provides accurate, culturally appropriate health information in English, Hindi, and Odia languages through a modern web interface with future WhatsApp and SMS integration capabilities.

### ✨ Key Features

- **🌐 Multilingual Support**: Responds in English, Hindi, and Odia
- **🔍 Intelligent Symptom Checker**: AI-powered health assessment using Rasa NLU
- **📱 Modern Web Interface**: Responsive design with real-time chat functionality
- **⚡ High Performance**: FastAPI backend with async processing
- **📊 Analytics Dashboard**: Real-time usage statistics and insights
- **🛡️ Secure & Reliable**: Production-ready with proper error handling
- **🤖 Advanced NLP**: Powered by Rasa for intent recognition and dialogue management

## 🏗️ Architecture

```
ama-arogya-chatbot/
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   │   ├── main.py              # API endpoints
│   │   └── __init__.py
│   ├── models/                   # Database models
│   │   ├── database.py          # SQLAlchemy models
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   ├── helpers.py           # Core utilities
│   │   ├── security.py          # Security middleware
│   │   └── __init__.py
│   ├── config/                   # Configuration
│   │   ├── settings.py          # App settings
│   │   └── __init__.py
│   └── __init__.py
├── frontend/                     # Modern web interface
│   ├── index.html               # Main frontend page
│   ├── styles.css               # Modern CSS with CSS variables
│   └── script.js                # Interactive JavaScript
├── data/                         # Rasa training data
│   ├── nlu.yml                  # Natural Language Understanding
│   ├── stories.yml              # Conversation flows
│   ├── rules.yml                # Dialogue rules
│   └── health/                  # Health-specific data
│       ├── vector_borne_diseases.yml
│       └── water_borne_diseases.yml
├── actions/                      # Rasa custom actions
│   ├── __init__.py
│   └── actions.py               # Custom action implementations
├── models/                       # Trained Rasa models
├── scripts/                      # Setup and deployment scripts
│   ├── dev-setup.sh             # Linux/Mac setup
│   └── dev-setup.bat            # Windows setup
├── tests/                        # Test files
├── main.py                       # FastAPI application entry point
├── database.py                   # Database models and initialization
├── config.yml                   # Rasa configuration
├── domain.yml                    # Rasa domain definition
├── endpoints.yml                 # Rasa endpoints configuration
├── credentials.yml               # Rasa credentials
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment (recommended)

### 🔧 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/SpicychieF05/Ama-Arogya_ChatBot.git
cd Ama-Arogya_ChatBot
```

2. **Create Virtual Environment**
```bash
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
python database.py
```

5. **Train Rasa Model**
```bash
rasa train
```

6. **Start Rasa Server (in separate terminal)**
```bash
# Activate virtual environment first
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # Linux/Mac

# Start Rasa server
rasa run --enable-api --port 5005
```

7. **Start FastAPI Application**
```bash
# In another terminal, activate virtual environment
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

### 📱 Access Points

- **Web Interface**: http://127.0.0.1:8001/
- **API Documentation**: http://127.0.0.1:8001/docs
- **Health Check**: http://127.0.0.1:8001/health
- **Analytics Dashboard**: http://127.0.0.1:8001/dashboard

## 🧪 Testing the Chatbot

### Sample Queries to Try
- **English**: "Hello, I have a fever and headache"
- **Hindi**: "गर्भावस्था के दौरान क्या सावधानी बरतनी चाहिए?"
- **Odia**: "ନମସ୍କାର, ଟିକା ସମ୍ବନ୍ଧରେ ଜାଣିବାକୁ ଚାହୁଁଛି"
- **Vaccination**: "Tell me about vaccination schedule"
- **Maternal Care**: "pregnancy care advice"
- **Water-borne diseases**: "What are symptoms of cholera?"
- **Vector-borne diseases**: "How to prevent malaria?"

### Testing Methods

**Option 1: Web Interface**
Open http://127.0.0.1:8001/ in your browser and start chatting with the modern interface!

**Option 2: API Testing**
```bash
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I have a fever", "sender_id": "test_user", "language": "en"}'
```

**Option 3: Interactive API Documentation**
Visit http://127.0.0.1:8001/docs to test the API interactively using FastAPI's built-in documentation.

### Stop the Applications
- Stop FastAPI: Press `Ctrl+C` in the FastAPI terminal
- Stop Rasa: Press `Ctrl+C` in the Rasa server terminal

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104+ (High-performance async API)
- **NLP Engine**: Rasa 3.6+ (Intent recognition, entity extraction, dialogue management)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Modern HTML5, CSS3 with CSS Variables, Vanilla JavaScript
- **Language Support**: English, Hindi, Odia
- **Deployment**: Uvicorn ASGI server

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| GET | `/demo` | Alternative demo route |
| GET | `/health` | Health check endpoint |
| GET | `/dashboard` | Analytics dashboard |
| GET | `/docs` | Interactive API documentation |
| POST | `/chat` | Chat with the bot |

### Chat API

**Request Format:**
```json
{
  "message": "Hello, I have a fever",
  "sender_id": "user123", 
  "language": "en"
}
```

**Response Format:**
```json
{
  "response": "I understand you have a fever. This could be due to various reasons...",
  "language": "en",
  "intent": "ask_fever",
  "confidence": 0.95
}
```

## 🏥 Health Knowledge Base

The chatbot is trained on various health topics including:

- **Common Symptoms**: Fever, headache, cough, stomach pain
- **Vector-borne Diseases**: Malaria, dengue, chikungunya
- **Water-borne Diseases**: Cholera, diarrhea, typhoid, hepatitis
- **Preventive Care**: Vaccination schedules, hygiene practices
- **Maternal Health**: Pregnancy care, prenatal advice
- **Emergency Care**: When to seek immediate medical attention

## 🌍 Multilingual Support

- **English**: Primary language for development and testing
- **Hindi**: देवनागरी script support for wider reach
- **Odia**: ଓଡ଼ିଆ script for local Odisha population

## 🚀 Future Enhancements

- **WhatsApp Integration**: Business API integration for messaging
- **SMS Fallback**: Text messaging for users without smartphones
- **Voice Interface**: Speech-to-text and text-to-speech capabilities
- **Appointment Booking**: Integration with local healthcare facilities
- **Real-time Alerts**: Disease outbreak notifications
- **Offline Support**: Progressive Web App for low-connectivity areas

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and add tests where applicable
4. Ensure your code follows Python PEP8 standards
5. Run tests and ensure the project builds successfully
6. Submit a pull request with a clear description of changes

### Development Guidelines
- Follow PEP8 for Python code formatting
- Add docstrings to functions and classes
- Include type hints where appropriate
- Keep Rasa training data organized and well-documented
- Test your changes thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

**Rasa Server Not Starting:**
- Ensure you've trained the model: `rasa train`
- Check if port 5005 is available
- Verify virtual environment is activated

**Frontend Not Loading:**
- Ensure FastAPI server is running on port 8001
- Check if static files are properly mounted
- Verify frontend directory exists and contains required files

**Database Issues:**
- Run `python database.py` to reinitialize the database
- Check SQLite file permissions

### Getting Help

- Create an issue on GitHub with detailed error information
- Include steps to reproduce the problem
- Provide relevant log outputs

## 📞 Contact

- **Project Repository**: [GitHub](https://github.com/SpicychieF05/Ama-Arogya_ChatBot)
- **Issues**: [GitHub Issues](https://github.com/SpicychieF05/Ama-Arogya_ChatBot/issues)

---

**Ama Arogya** - Making healthcare information accessible to rural communities in Odisha through the power of AI and multilingual support. 🏥💙

*Project maintained by the Ama Arogya development team.*