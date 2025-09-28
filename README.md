# Ama Arogya - AI-Driven Health Assistant for Rural Odisha

<div align="center">
  <h3>🏥 Multilingual Health Chatbot for Rural Communities</h3>
  <p>Bridging the health information gap in Odisha with AI-powered assistance</p>
  
  [![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com)
  [![Rasa](https://img.shields.io/badge/Rasa-3.6+-purple.svg)](https://rasa.com)
  [![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen.svg)](test_api.py)
  [![Security](https://img.shields.io/badge/Security-Enabled-red.svg)](src/utils/security.py)
  [![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](.github/workflows/ci.yml)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
</div>

## 🌟 Overview

Ama Arogya is an intelligent, multilingual health chatbot designed specifically for rural and semi-urban populations in Odisha, India. Built with FastAPI and Rasa, the system provides accurate, culturally appropriate health information in English, Hindi, and Odia languages through a modern web interface with future WhatsApp and SMS integration capabilities.

### ✨ Key Features

- **🌐 Multilingual Support**: Responds in English, Hindi, and Odia
- **🔍 Intelligent Symptom Checker**: AI-powered health assessment using Rasa NLU
- **📱 Modern Web Interface**: Responsive design with real-time chat functionality
- **⚡ High Performance**: FastAPI backend with async processing and optimized timeouts
- **📊 Analytics Dashboard**: Real-time usage statistics and insights
- **🛡️ Enterprise Security**: Production-ready security middleware with rate limiting and request validation
- **🤖 Advanced NLP**: Powered by Rasa with custom actions for enhanced dialogue management
- **🧪 Comprehensive Testing**: 18+ automated tests covering all endpoints and scenarios
- **🚀 CI/CD Pipeline**: Automated testing, security scanning, and deployment validation
- **⚙️ Environment Configuration**: Flexible configuration management with environment variables

## 🏗️ Architecture

```
ama-arogya-chatbot/
├── .github/                      # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   │   ├── main.py              # API endpoints
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   ├── helpers.py           # Core utilities
│   │   ├── security.py          # Security middleware & validation
│   │   └── __init__.py
│   ├── config/                   # Configuration
│   │   ├── settings.py          # App settings
│   │   └── __init__.py
│   └── __init__.py
├── static/                       # Frontend assets
│   ├── styles.css               # Modern CSS with CSS variables
│   └── script.js                # Interactive JavaScript
├── index.html                    # Main web interface
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
├── docs/                         # Documentation
│   └── API.md                   # API documentation
├── scripts/                      # Setup and deployment scripts
│   ├── dev-setup.sh             # Linux/Mac setup
│   └── dev-setup.bat            # Windows setup
├── tests/                        # Test files
│   └── test_stories.yml         # Test conversation flows
├── main.py                       # FastAPI application entry point
├── test_api.py                   # Comprehensive API test suite (18+ tests)
├── database.py                   # Database models and initialization
├── config.yml                   # Rasa configuration
├── domain.yml                    # Rasa domain definition with custom actions
├── endpoints.yml                 # Rasa endpoints configuration (actions enabled)
├── credentials.yml               # Rasa credentials
├── requirements.txt              # Python dependencies (pinned versions)
├── .env.example                  # Environment configuration template
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
. .venv/Scripts/activate
# Linux/Mac:
source .venv/bin/activate
```

3. **Configure Environment Variables**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# HOST=0.0.0.0
# PORT=8000
# DEBUG=false
# RASA_API_URL=http://localhost:5005
# API_TIMEOUT=5
```

4. **Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Initialize Database**
```bash
python database.py
```

6. (Optional) **Train Rasa Model**
```bash
rasa train
```

7. (Optional) **Start Rasa Actions Server** (separate terminal)
```bash
# Activate virtual environment first
. .venv/Scripts/activate  # Windows bash
# source .venv/bin/activate  # Linux/Mac

# Start Rasa actions server for custom actions
rasa run actions --port 5055
```

8. (Optional) **Start Rasa Server** (separate terminal)
```bash
# Activate virtual environment first
. .venv/Scripts/activate  # Windows bash
# source .venv/bin/activate  # Linux/Mac

# Start Rasa server
rasa run --enable-api --port 5005
```

9. **Start FastAPI Application**
```bash
# In another terminal, activate virtual environment and run:
python main.py
# Or alternatively:
# python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

10. (VS Code) **Run with Tasks**
- Open the Command Palette → "Run Task" → choose `Run FastAPI dev server`
- Quick checks: `Run API quick test` or `API sanity run` tasks

### 📱 Access Points

- **Web Interface**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Analytics Dashboard**: http://localhost:8000/dashboard

## 🧪 Testing the Chatbot

### Automated Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest test_api.py -v

# Run with coverage reporting
python -m pytest test_api.py -v --cov=main --cov-report=html

# Run specific test class
python -m pytest test_api.py::TestChatEndpoint -v

# Run CI/CD pipeline locally (requires GitHub CLI)
gh workflow run ci.yml
```

### Manual Testing

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
Open http://localhost:8000/ in your browser and start chatting with the modern interface!

**Option 2: API Testing**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I have a fever", "sender_id": "test_user", "language": "en"}'
```

**Option 3: Interactive API Documentation**
Visit http://localhost:8000/docs to test the API interactively using FastAPI's built-in documentation.

### Stop the Applications
- Stop FastAPI: Press `Ctrl+C` in the FastAPI terminal
- Stop Rasa Actions: Press `Ctrl+C` in the Rasa actions terminal
- Stop Rasa Server: Press `Ctrl+C` in the Rasa server terminal

### Model Evaluation

You can run the built-in evaluation script against the running API (port 8000):

```bash
python evaluate_model.py
```

This will print overall accuracy, per-language accuracy, and per-topic performance based on predefined test cases.

### VS Code Tasks

The workspace includes tasks for convenience:
- `Run FastAPI dev server`: starts the app on `127.0.0.1:8000`
- `Run API quick test`: spins up a temporary server and performs a health + chat call
- `API sanity run`: similar to quick test with minimal output

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI 0.104+ (High-performance async API)
- **NLP Engine**: Rasa 3.6+ (Intent recognition, entity extraction, dialogue management)
- **Security**: Custom SecurityMiddleware with rate limiting and request validation
- **Database**: SQLite with SQLAlchemy ORM (updated to modern syntax)
- **Frontend**: Modern HTML5, CSS3 with CSS Variables, Vanilla JavaScript
- **Language Support**: English, Hindi, Odia
- **Testing**: Pytest with 18+ comprehensive tests
- **CI/CD**: GitHub Actions with automated testing, security scanning, and deployment
- **Configuration**: Environment-based configuration with python-dotenv
- **Deployment**: Uvicorn ASGI server with production optimizations

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description | Security |
|--------|----------|-------------|----------|
| GET | `/` | Main web interface | Rate limited |
| GET | `/demo` | Alternative demo route | Rate limited |
| GET | `/health` | Health check endpoint | Public |
| GET | `/stats` | Usage statistics | Rate limited |
| GET | `/dashboard` | Analytics dashboard | Rate limited |
| GET | `/docs` | Interactive API documentation | Public (dev) |
| POST | `/chat` | Chat with the bot | Rate limited, validated |
| POST | `/api/chat` | Chat (alias in `src/api/main.py`) | Rate limited, validated |

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
  "intent": "rasa_processed" | "fallback"
}
```

## 🧪 Test Suite

The project includes a comprehensive test suite with 18+ automated tests:

### Test Categories

- **Health Endpoint Tests**: API health check validation
- **Chat Functionality Tests**: Multi-language chat testing (English, Hindi, Odia)
- **Error Handling Tests**: Input validation, edge cases, security testing
- **API Validation Tests**: Request/response format validation
- **Static File Tests**: Frontend asset serving
- **Mock Testing**: Database and external service mocking

### Running Tests

```bash
# Run all tests
python -m pytest test_api.py -v

# Run with coverage
python -m pytest test_api.py --cov=main --cov-report=html

# Run specific test categories
python -m pytest test_api.py::TestChatEndpoint -v
python -m pytest test_api.py::TestErrorHandling -v
```

### Test Results
```
18 passed, 2 warnings in 30.51s
- TestHealthEndpoint: 2 tests ✅
- TestChatEndpoint: 7 tests ✅  
- TestStatsEndpoint: 1 test ✅
- TestStaticFiles: 2 tests ✅
- TestErrorHandling: 5 tests ✅
- Individual Functions: 1 test ✅
```

### Security Features

- **Rate Limiting**: 100 requests per minute per IP
- **Request Validation**: Input sanitization and size limits
- **Security Headers**: CORS, CSP, and other security headers
- **Error Handling**: Graceful error responses without sensitive information leak

**Response Format:**
```json
{
  "response": "I understand you have a fever. This could be due to various reasons...",
  "language": "en",
  "intent": "rasa_processed" | "fallback"
}
```

## 🧰 Troubleshooting

- Web shows demo mode or offline banner
  - Ensure API is up: `curl http://127.0.0.1:8000/health`
  - Frontend uses same-origin relative URLs; make sure you opened the site from port `8000`
- Rasa not responding
  - Start Rasa servers (optional features):
    - `rasa run --enable-api --port 5005`
    - `rasa run actions --port 5055`
  - The app will gracefully fall back to built-in responses when Rasa is unavailable
- Dependency conflicts
  - We pin `fastapi==0.95.2`, `pydantic==1.10.9`, `scikit-learn==1.1.3`, `spacy==3.5.4` for Rasa 3.6 compatibility
  - Avoid forcing a TensorFlow version; let Rasa manage it
- Windows activation
  - Use `. .venv/Scripts/activate` when using bash on Windows (Git Bash/WSL)

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
- **Advanced Analytics**: ML-powered usage insights and health trend analysis
- **Multi-tenant Support**: Support for multiple healthcare organizations

## 🛡️ Security & Production Features

- **Security Middleware**: Enterprise-grade security with rate limiting
- **Request Validation**: Input sanitization and XSS protection  
- **Environment Configuration**: Secure configuration management
- **Error Handling**: Graceful error responses without information leakage
- **Monitoring**: Comprehensive logging and health checks
- **Testing**: 18+ automated tests covering all scenarios
- **CI/CD Pipeline**: Automated security scanning and deployment validation

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
- Write tests for new features using pytest
- Run the test suite before submitting: `python -m pytest test_api.py -v`
- Ensure CI/CD pipeline passes all checks
- Update documentation for new features

### Local Development Setup

```bash
# Install development dependencies
pip install pytest pytest-cov flake8 black

# Run linting
flake8 . --max-line-length=127

# Format code
black .

# Run tests with coverage
python -m pytest test_api.py -v --cov=main --cov-report=html
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Troubleshooting

### Common Issues

**Rasa Server Not Starting:**
- Ensure you've trained the model: `rasa train`
- Check if port 5005 is available
- Verify virtual environment is activated

**Rasa Actions Not Working:**
- Ensure Rasa actions server is running: `rasa run actions --port 5055`
- Check that `endpoints.yml` has the action_endpoint uncommented
- Verify custom actions are defined in `domain.yml`

**Frontend Not Loading:**
- Ensure FastAPI server is running on the configured port (default: 8000)
- Check if static files are properly mounted
- Verify frontend directory exists and contains required files

**Database Issues:**
- Run `python database.py` to reinitialize the database
- Check SQLite file permissions

**Security/Rate Limiting Issues:**
- Check if you're exceeding the rate limit (100 requests/minute)
- Verify SecurityMiddleware is properly configured
- Review error logs for security-related rejections

**Environment Configuration Issues:**
- Ensure `.env` file exists (copy from `.env.example`)
- Check that all required environment variables are set
- Verify python-dotenv is installed: `pip install python-dotenv`

**Test Failures:**
- Run tests individually to isolate issues: `python -m pytest test_api.py::TestClass::test_method -v`
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure the application can import properly: `python -c "import main"`

### Getting Help

- Create an issue on GitHub with detailed error information
- Include steps to reproduce the problem
- Provide relevant log outputs

## 📞 Contact

- **Project Repository**: [GitHub](https://github.com/SpicychieF05/Ama-Arogya-ChatBot)
- **Issues**: [GitHub Issues](https://github.com/SpicychieF05/Ama-Arogya-ChatBot/issues)

---

**Ama Arogya** - Making healthcare information accessible to rural communities in Odisha through the power of AI and multilingual support. 🏥💙

*Enterprise-ready healthcare chatbot with comprehensive testing, security, and CI/CD pipeline.*

**Key Stats:**
- 🧪 18+ Automated Tests
- 🛡️ Enterprise Security
- 🚀 CI/CD Pipeline  
- 🌐 3 Languages Supported
- ⚡ High Performance API

*Project maintained and developed by the Arogya Allies team.*
---
*Team ID - 61328*
---
*Smart India Hackathon 2025*
