#!/bin/bash

echo "Starting RAG System..."
echo ""

# Check for Python installation
if ! command -v python3 &> /dev/null
then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check for virtual environment
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
fi

# Activate virtual environment
source env/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start Flask backend in a new terminal
echo "Starting Flask backend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source env/bin/activate && cd flask_app && python app.py"'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$(pwd)' && source env/bin/activate && cd flask_app && python app.py; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd '$(pwd)' && source env/bin/activate && cd flask_app && python app.py" &
    else
        echo "Could not find a suitable terminal emulator. Please start the Flask backend manually."
    fi
else
    echo "Unsupported OS. Please start the Flask backend manually."
fi

# Wait for Flask to start
echo "Waiting for Flask to start..."
sleep 5

# Start Streamlit frontend in a new terminal
echo "Starting Streamlit frontend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript -e 'tell app "Terminal" to do script "cd '"$(pwd)"' && source env/bin/activate && cd streamlit_app && streamlit run app.py"'
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd '$(pwd)' && source env/bin/activate && cd streamlit_app && streamlit run app.py; exec bash"
    elif command -v xterm &> /dev/null; then
        xterm -e "cd '$(pwd)' && source env/bin/activate && cd streamlit_app && streamlit run app.py" &
    else
        echo "Could not find a suitable terminal emulator. Please start the Streamlit frontend manually."
    fi
else
    echo "Unsupported OS. Please start the Streamlit frontend manually."
fi

echo ""
echo "RAG System is now running!"
echo "Flask backend: http://localhost:5001"
echo "Streamlit frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to shut down the system..."

# Keep the script running until the user terminates it
trap "echo 'Shutting down RAG System...'; pkill -f 'python.*app.py'" SIGINT
while true; do sleep 1; done