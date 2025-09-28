# run_server.py
import subprocess
import time
import sys

print("Starting SDLC Multi-Agent Assistant Backend...")

# Start the uvicorn server
cmd = [
    sys.executable, "-m", "uvicorn",
    "main_ultra_minimal:app",
    "--host", "127.0.0.1",
    "--port", "8083",
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
    time.sleep(3)

    # Check if process is still running
    if process.poll() is None:
        print("✅ Server appears to be running successfully!")
        print("Press Ctrl+C to stop the server")

        # Keep the script running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("Stopping server...")
            process.terminate()
            process.wait()
    else:
        stdout, stderr = process.communicate()
        print("❌ Server process exited immediately")
        print("STDOUT:", stdout)
        print("STDERR:", stderr)

except Exception as e:
    print(f"❌ Error starting server: {e}")