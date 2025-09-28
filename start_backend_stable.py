# start_backend_stable.py
import subprocess
import time
import os
import sys

def start_backend():
    """Start the backend with proper process management."""
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if GROQ_API_KEY is set
    if not os.environ.get('GROQ_API_KEY'):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file or environment")
        return False
    
    backend_dir = r"c:\YOKA\Research\sdlc-assistant\backend"
    os.chdir(backend_dir)
    
    print("🚀 Starting FLUX Backend...")
    
    # Start uvicorn directly
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000", 
        "--log-level", "info"
    ]
    
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Use CREATE_NEW_PROCESS_GROUP to prevent termination issues
        process = subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print(f"✅ Backend started with PID: {process.pid}")
        
        # Monitor output for a few seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            if process.poll() is not None:
                print("❌ Process exited early")
                break
                
            # Check if server is responding
            try:
                import requests
                response = requests.get("http://localhost:8000/health", timeout=1)
                if response.status_code == 200:
                    print("✅ Backend is healthy and responding!")
                    print("🌐 Access the application at: http://localhost:3000")
                    print("📊 Backend API docs at: http://localhost:8000/docs")
                    print(f"🔧 Backend PID: {process.pid} (use 'Stop-Process -Id {process.pid}' to stop)")
                    return process
            except requests.exceptions.RequestException:
                pass
                
            time.sleep(1)
            
        print("⏰ Server startup taking longer than expected...")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

if __name__ == "__main__":
    process = start_backend()
    if process:
        try:
            print("Press Ctrl+C to stop the server...")
            process.wait()
        except KeyboardInterrupt:
            print("\\n🛑 Stopping server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped")