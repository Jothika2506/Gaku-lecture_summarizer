import subprocess
import time
import webbrowser
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

BACKEND = os.path.join(ROOT, "backend", "api.py")
FRONTEND = os.path.join(ROOT, "frontend")

# Use the *current* Python executable (the venv one)
PYTHON = sys.executable

print("🚀 Starting Gaku Backend + Frontend...")

# Start backend (Flask on port 5000)
backend_process = subprocess.Popen(
    [PYTHON, BACKEND],
    cwd=ROOT
)

time.sleep(2)  # give backend a moment

# Start frontend (http.server on port 8000)
frontend_process = subprocess.Popen(
    [PYTHON, "-m", "http.server", "8000"],
    cwd=FRONTEND
)

time.sleep(1)
webbrowser.open("http://127.0.0.1:8000")

print("\n💡 Gaku is running:")
print("  Backend  → http://127.0.0.1:5000")
print("  Frontend → http://127.0.0.1:8000")
print("\nPress CTRL+C in this window to stop both.\n")

try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping servers...")
    backend_process.terminate()
    frontend_process.terminate()