#!/bin/bash

# Activate virtual environment - Cross-platform support
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash, WSL, or Cygwin)
    source djenv/Scripts/activate
else
    # macOS/Linux
    source djenv/bin/activate

# Move to app directory
cd djbotapp

# Start Daphne server
echo "🚀 Starting Daphne ASGI server on port 8000..."
daphne -p 8000 djbotapp.asgi:application
