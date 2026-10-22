"""
Runner utility for UMLRev
Allows running CLI analysis, launching backend/frontend, or launching the unified live demo.
"""

import sys
import os
import subprocess
import argparse
import threading
import webbrowser
import time

# Ensure current script directory is in sys.path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
if CUR_DIR not in sys.path:
    sys.path.insert(0, CUR_DIR)

def load_env():
    """Loads environment variables from backend/.env or .env if present."""
    env_paths = [
        os.path.join(CUR_DIR, "backend", ".env"),
        os.path.join(CUR_DIR, ".env")
    ]
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v

load_env()

def run_cli(repo_path, output_path="output"):
    from backend.umlrev.cli import main
    abs_repo = os.path.abspath(os.path.join(CUR_DIR, repo_path)) if not os.path.isabs(repo_path) else repo_path
    abs_out = os.path.abspath(os.path.join(CUR_DIR, output_path)) if not os.path.isabs(output_path) else output_path
    sys.argv = ["cli.py", "--repo", abs_repo, "--output", abs_out]
    main()

def run_backend(port=8000):
    import uvicorn
    print(f"[*] Starting FastAPI backend on http://127.0.0.1:{port}...")
    reload_dirs = [os.path.join(CUR_DIR, "backend", "umlrev")]
    uvicorn.run("backend.umlrev.api.app:app", host="127.0.0.1", port=port, reload=True, reload_dirs=reload_dirs, app_dir=CUR_DIR)

def run_frontend():
    frontend_dir = os.path.join(CUR_DIR, "frontend")
    print(f"[*] Starting Vite dev server in {frontend_dir}...")
    subprocess.run("npm run dev", shell=True, cwd=frontend_dir)

def is_port_free(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

def run_demo(port=8000):
    import uvicorn
    import socket

    # 1. Ensure frontend distribution exists
    frontend_dist = os.path.join(CUR_DIR, "frontend", "dist")
    index_html = os.path.join(frontend_dist, "index.html")
    if not os.path.exists(index_html):
        print("[*] Compiling frontend distribution bundle...")
        subprocess.run("npm run build", shell=True, cwd=os.path.join(CUR_DIR, "frontend"))

    # 2. Check port availability; fallback to 8001 or 8080 if occupied
    demo_port = port
    if not is_port_free(demo_port):
        # Check if existing server on 8000 is our UMLRev instance
        try:
            import urllib.request
            resp = urllib.request.urlopen(f"http://127.0.0.1:{demo_port}/api/health", timeout=1.0)
            if resp.status == 200:
                print(f"[*] UMLRev server is already actively running on http://127.0.0.1:{demo_port}")
                url = f"http://127.0.0.1:{demo_port}"
                print(f"[*] Opening browser to existing instance: {url}")
                webbrowser.open(url)
                return
        except Exception:
            pass

        # If occupied by foreign process, find next free port
        for cand in [8001, 8080, 8088]:
            if is_port_free(cand):
                demo_port = cand
                print(f"[*] Port {port} is occupied. Redirecting demo to free port {demo_port}.")
                break

    def open_browser_when_ready():
        url = f"http://127.0.0.1:{demo_port}"
        # Poll socket until backend is actively listening
        for _ in range(40):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
                if s.connect_ex(('127.0.0.1', demo_port)) == 0:
                    s.close()
                    break
                s.close()
            except Exception:
                pass
            time.sleep(0.2)

        print(f"[*] Backend server ready! Opening browser: {url}")
        webbrowser.open(url)

    # Launch browser automatically in background once server is bound
    threading.Thread(target=open_browser_when_ready, daemon=True).start()

    print("=" * 72)
    print("  UMLRev: Live Production Demo")
    print("  Developed by: Jay Gandhi (B124) & Aditya Rane (B129)")
    print("  MPSTME, NMIMS University - Semester 5 Software Engineering")
    print("=" * 72)
    print(f"[*] Unified React Dashboard & REST API running on: http://127.0.0.1:{demo_port}")
    print(f"[*] Interactive Swagger API Documentation:       http://127.0.0.1:{demo_port}/docs")
    print("=" * 72)
    print("[*] Press Ctrl+C to terminate demo server.")

    uvicorn.run("backend.umlrev.api.app:app", host="127.0.0.1", port=demo_port, reload=False, app_dir=CUR_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UMLRev Launcher")
    parser.add_argument("mode", choices=["cli", "backend", "frontend", "benchmark", "demo"], help="Operation mode")
    parser.add_argument("--repo", default="examples/tell_story", help="Target repository path")
    parser.add_argument("--output", default="output", help="Output directory")
    args = parser.parse_args()

    if args.mode == "cli":
        run_cli(args.repo, args.output)
    elif args.mode == "benchmark":
        run_cli("examples/tell_story", "output")
    elif args.mode == "backend":
        run_backend()
    elif args.mode == "frontend":
        run_frontend()
    elif args.mode == "demo":
        run_demo()
