import os
import subprocess
import re
from typing import List, Dict, Optional, Any

class GitService:
    """
    Handles live GitHub repository cloning, fetching, commit history, and diff extraction.
    """

    @staticmethod
    def is_valid_github_url(url: str) -> bool:
        if not url or not isinstance(url, str):
            return False
        clean = url.strip()
        pattern = r"^(https?://)?(www\.)?github\.com/[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-\.]+(?:/.*)?$"
        return bool(re.match(pattern, clean))

    @staticmethod
    def normalize_github_url(url: str) -> str:
        clean = url.strip().rstrip("/")
        if not clean.startswith("http://") and not clean.startswith("https://"):
            clean = f"https://{clean}"
        parts = clean.split("/")
        if len(parts) >= 5:
            clean = f"{parts[0]}//{parts[2]}/{parts[3]}/{parts[4]}"
        if clean.endswith(".git"):
            clean = clean[:-4]
        return clean

    @staticmethod
    def extract_repo_name(url: str) -> str:
        clean = GitService.normalize_github_url(url)
        return clean.split("/")[-1]

    @staticmethod
    def clone_repository(github_url: str, destination_dir: str, depth: int = 15) -> Dict[str, Any]:
        """Clones a remote GitHub repository to destination_dir."""
        clean_url = github_url.strip()
        if not clean_url.endswith(".git"):
            clean_url = f"{clean_url}.git"

        os.makedirs(destination_dir, exist_ok=True)
        cmd = ["git", "clone", "--depth", str(depth), clean_url, destination_dir]

        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=120,
                encoding="utf-8",
                errors="replace"
            )
            return {
                "success": True,
                "destination": destination_dir,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "error": f"Git clone failed: {e.stderr or e.stdout}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute git clone: {str(e)}"
            }

    @staticmethod
    def get_commit_history(repo_dir: str, limit: int = 15) -> List[Dict[str, str]]:
        """Retrieves recent commit history."""
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            return []

        cmd = ["git", "log", f"-n{limit}", "--pretty=format:%h|%an|%s|%cI"]
        try:
            res = subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
                errors="replace"
            )
            commits = []
            for line in res.stdout.strip().split("\n"):
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        commits.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "message": parts[2],
                            "date": parts[3]
                        })
            return commits
        except Exception:
            return []

    @staticmethod
    def get_diff_summary(repo_dir: str, commit_hash: Optional[str] = None) -> Dict[str, Any]:
        """
        Extracts git diff for a commit or HEAD. Handles normal commits with parents,
        as well as root commits and shallow graft points without parents.
        """
        if not os.path.exists(os.path.join(repo_dir, ".git")):
            return {"changed_files": [], "diff_text": "", "summary": "No git repository found"}

        try:
            target = commit_hash.strip() if commit_hash and commit_hash.strip() else "HEAD"

            # Check if target commit has a valid parent
            parent_check = subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet", f"{target}~1"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            has_parent = (parent_check.returncode == 0)

            if has_parent:
                diff_cmd = ["git", "diff", f"{target}~1", target, "--name-only"]
                raw_diff_cmd = ["git", "diff", f"{target}~1", target]
            else:
                diff_cmd = ["git", "show", "--pretty=", "--name-only", target]
                raw_diff_cmd = ["git", "show", target]

            files_res = subprocess.run(
                diff_cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            changed_files = [
                f.strip() for f in files_res.stdout.strip().split("\n")
                if f.strip() and not f.startswith("commit") and not f.startswith("Author")
            ]

            diff_res = subprocess.run(
                raw_diff_cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            diff_text = diff_res.stdout[:5000]

            count_res = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            count = int(count_res.stdout.strip()) if count_res.stdout.strip().isdigit() else 1

            return {
                "changed_files": changed_files,
                "diff_text": diff_text,
                "commit_count": count
            }
        except Exception as e:
            return {
                "changed_files": [],
                "diff_text": "",
                "error": str(e)
            }
