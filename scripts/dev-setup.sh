#!/bin/bash
# Development setup script for Ama Arogya ChatBot

echo "🚀 Setting up Ama Arogya ChatBot Development Environment"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/Scripts/activate || source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
fi

# Create logs directory
mkdir -p logs

# Initialize database
echo "🗄️ Initializing database..."
python -c "from src.models.database import initialize_database; initialize_database()"

echo "✅ Development environment setup complete!"
echo "🎯 Run 'python main.py' to start the application"