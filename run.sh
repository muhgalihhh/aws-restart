#!/bin/bash

# SIAKAD Startup Script
echo "Starting SIAKAD - Sistem Informasi Akademik Sekolah"
echo "=============================================="

# Check if requirements are installed
python3 -c "import flask, flask_sqlalchemy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install --break-system-packages -r requirements.txt
fi

# Start the application
echo "Starting Flask application..."
echo "Access the application at: http://localhost:5000"
echo "Default login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py