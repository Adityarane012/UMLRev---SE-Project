"""
Runner utility for AI-Assisted UMLRev
Allows running CLI analysis or launching the Web System from inside UMLRev.
"""

import sys
import os
import subprocess
import argparse

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
    uvicorn.run("backend.umlrev.api.app:app", host="127.0.0.1", port=port, reload=True, app_dir=CUR_DIR)

def run_frontend():
    frontend_dir = os.path.join(CUR_DIR, "frontend")
    print(f"[*] Starting Vite dev server in {frontend_dir}...")
    subprocess.run("npm run dev", shell=True, cwd=frontend_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Assisted UMLRev Launcher")
    parser.add_argument("mode", choices=["cli", "backend", "frontend", "benchmark"], help="Operation mode")
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
