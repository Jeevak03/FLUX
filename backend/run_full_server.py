# run_full_server.py
import subprocess
import time
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

print("🚀 Starting FLUX - Where Agents Meet Agile Backend with WebSocket support...")

# Check if GROQ_API_KEY is set
if not os.environ.get('GROQ_API_KEY'):
    print("❌ GROQ_API_KEY not found in environment variables")
    print("Please set GROQ_API_KEY in your .env file or environment")
    exit(1)

# Start the uvicorn server
cmd = [
    sys.executable, "-m", "uvicorn",
    "main:app",
    "--host", "127.0.0.1",
    "--port", "8000",
    "--log-level", "info"
]

print(f"Running command: {' '.join(cmd)}")

try:
    process = subprocess.Popen(
        cmd,
        cwd=r"c:\YOKA\Research\sdlc-assistant\backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print(f"Server process started with PID: {process.pid}")

    # Wait a bit for the server to start
    time.sleep(5)

    # Check if process is still running
    if process.poll() is None:
        print("✅ Backend server is running successfully on http://localhost:8000!")
        print("Server will continue running. Check the health endpoint to verify.")

        # Don't wait for the process, let it run in background
        print("Server is running in background...")
    else:
        stdout, stderr = process.communicate()
        print("❌ Server process exited immediately")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)

except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()