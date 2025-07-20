#!/usr/bin/env python3
"""
Unified entry point for the Knowledge Management System.
Starts both the FastAPI backend and Next.js frontend.
"""
import sys
import subprocess
import time
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
BACKEND_CMD = [
    "uvicorn", 
    "backend.app:app", 
    "--host", "0.0.0.0", 
    "--port", "8000",
    "--reload"
]
FRONTEND_CMD = ["npm", "run", "dev"]
FRONTEND_DIR = BASE_DIR / "frontend"

def is_port_in_use(port):
    """Check if a port is already in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_process(command, cwd=None, shell=False, check_port=None):
    """Start a subprocess and return the process object"""
    if check_port and is_port_in_use(check_port):
        print(f"⚠️  Port {check_port} is already in use. Assuming the service is already running.")
        return None
        
    print(f"Starting: {' '.join(command)}")
    try:
        return subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=sys.stdout,
            stderr=subprocess.STDOUT
        )
    except Exception as e:
        print(f"❌ Failed to start process: {e}")
        return None

def ensure_frontend_dependencies():
    """Ensure frontend dependencies are installed"""
    print("Checking frontend dependencies...")
    if not (FRONTEND_DIR / "node_modules").exists():
        print("Installing frontend dependencies (this may take a few minutes)...")
        subprocess.run(
            ["npm", "install"],
            cwd=FRONTEND_DIR,
            check=True
        )

def main():
    """Main entry point for the application"""
    print("🚀 Starting Knowledge Management System...")
    
    # Ensure frontend dependencies are installed
    ensure_frontend_dependencies()
    
    # Start backend and frontend processes
    processes = []
    
    try:
        # Start backend
        print("\nStarting backend server...")
        backend_process = start_process(BACKEND_CMD, check_port=8000)
        if backend_process:  # Only append if process was started
            processes.append(backend_process)
            # Give backend a moment to start
            print("Waiting for backend to initialize...")
            time.sleep(3)
        
        # Start frontend
        print("\nStarting frontend development server...")
        frontend_process = start_process(FRONTEND_CMD, cwd=FRONTEND_DIR, check_port=3000)
        if frontend_process:  # Only append if process was started
            processes.append(frontend_process)
        
        print("\n✅ Application started successfully!")
        print("   - Frontend: http://localhost:3000")
        print("   - Backend API: http://localhost:8000")
        print("   - API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the application")
        
        # Keep the main process running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Terminate all child processes
        print("\nTerminating processes...")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        print("✅ All processes terminated.")

if __name__ == "__main__":
    main()