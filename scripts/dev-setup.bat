@echo off
REM Development setup script for Ama Arogya ChatBot (Windows)

echo 🚀 Setting up Ama Arogya ChatBot Development Environment

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Initialize database
echo 🗄️ Initializing database...
python -c "from src.models.database import initialize_database; initialize_database()"

echo ✅ Development environment setup complete!
echo 🎯 Run 'python main.py' to start the application
pause