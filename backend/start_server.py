# start_server.py
import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variable for debugging
# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Check if GROQ_API_KEY is set
if not os.environ.get('GROQ_API_KEY'):
    print("❌ GROQ_API_KEY not found in environment variables")
    print("Please set GROQ_API_KEY in your .env file or environment")
    exit(1)

print("Starting SDLC Multi-Agent Assistant...")
print(f"Python version: {sys.version}")
print(f"GROQ_API_KEY set: {'Yes' if os.getenv('GROQ_API_KEY') else 'No'}")

try:
    from main import app
    print("✅ FastAPI app imported successfully")

    # Start the server
    print("🚀 Starting uvicorn server...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)