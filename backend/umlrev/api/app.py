import os
import shutil
import zipfile
import uuid
from typing import Dict, List, Optional, Any, Set
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

from ..model.project import Project
from ..model.feature import Feature
from ..pipeline.extractor import SymbolExtractor
from ..pipeline.clustering import ClusterEngine
from ..pipeline.labeller import FeatureLabeller
from ..pipeline.git_service import GitService
from ..pipeline.diff_analyzer import DiffAnalyzer
from ..diagram.engine import DiagramEngine
from ..evaluation.ground_truth import GroundTruth
from ..evaluation.benchmark import EvaluationService

app = FastAPI(
    title="AI-Assisted UMLRev API",
    description="Continuous Reverse Engineering API with AI Feature Identification",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
PROJECT_STORE: Dict[str, Project] = {}
PROJECT_DIFF_REPORTS: Dict[str, Any] = {}
WORKSPACE_DIR = os.path.abspath("./workspace_uploads")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

class LoginRequest(BaseModel):
    username: str
    password: str

class UpdateFeatureRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    classes: List[str]
    confidence: Optional[float] = 1.0

class EvaluateRequest(BaseModel):
    ground_truth: Dict[str, List[str]]

class GitHubIngestRequest(BaseModel):
    github_url: str
    name: Optional[str] = None

class DiffAnalysisRequest(BaseModel):
    commit_hash: Optional[str] = None

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AI-Assisted UMLRev Backend",
        "team": ["Jay Gandhi (B124)", "Aditya Rane (B129)"]
    }

@app.post("/api/auth/login")
def login(req: LoginRequest):
    if req.username:
        return {
            "token": f"token-{uuid.uuid4()}",
            "username": req.username,
            "role": "Software Developer"
        }
    raise HTTPException(status_code=400, detail="Invalid username")

@app.post("/api/projects/create")
def create_project(name: str = Form(...), local_path: Optional[str] = Form(None)):
    proj_id = str(uuid.uuid4())[:8]
    target_dir = os.path.abspath(local_path) if local_path and os.path.exists(local_path) else os.path.join(WORKSPACE_DIR, proj_id)
    os.makedirs(target_dir, exist_ok=True)

    project = Project(name=name, folder_path=target_dir)
    PROJECT_STORE[proj_id] = project

    return {
        "project_id": proj_id,
        "name": name,
        "folder_path": target_dir,
        "status": "created"
    }

@app.post("/api/projects/github")
def ingest_github_repo(req: GitHubIngestRequest):
    """Clones a remote GitHub repository URL and initializes the project."""
    if not GitService.is_valid_github_url(req.github_url):
        raise HTTPException(status_code=400, detail="Invalid GitHub URL. Must be in format https://github.com/owner/repo")

    repo_name = req.name or GitService.extract_repo_name(req.github_url)
    proj_id = str(uuid.uuid4())[:8]
    target_dir = os.path.join(WORKSPACE_DIR, f"gh_{proj_id}")

    # Clone repository
    clone_res = GitService.clone_repository(req.github_url, target_dir)
    if not clone_res.get("success"):
        raise HTTPException(status_code=400, detail=clone_res.get("error", "Failed to clone GitHub repository"))

    project = Project(name=repo_name, folder_path=target_dir)
    PROJECT_STORE[proj_id] = project

    # Extract symbols & analyze features
    extractor = SymbolExtractor()
    extracted_proj = extractor.scan_directory(project.folder_path, project_name=project.name)
    project.source_files = extracted_proj.source_files
    project.classes = extracted_proj.classes
    project.relationships = extracted_proj.relationships

    # Semantic Clustering & AI Feature Labeling
    cluster_engine = ClusterEngine()
    clusters = cluster_engine.cluster(list(project.classes.values()), project.relationships)

    labeller = FeatureLabeller()
    project.features = []
    for c in clusters:
        feat = labeller.label(c, project.classes)
        project.features.append(feat)

    # Generate initial diagrams
    diagram_engine = DiagramEngine()
    diagram_engine.generate_for_project(project)

    commits = GitService.get_commit_history(target_dir, limit=10)

    return {
        "project_id": proj_id,
        "name": repo_name,
        "github_url": req.github_url,
        "folder_path": target_dir,
        "files_count": len(project.source_files),
        "classes_count": len(project.classes),
        "relationships_count": len(project.relationships),
        "features": [f.to_dict() for f in project.features],
        "diagrams": [d.to_dict() for d in project.diagrams],
        "recent_commits": commits
    }

@app.get("/api/projects/{proj_id}/commits")
def get_commits(proj_id: str):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]
    commits = GitService.get_commit_history(project.folder_path, limit=15)
    return {
        "project_id": proj_id,
        "commits": commits
    }

@app.post("/api/projects/{proj_id}/analyze-diff")
def analyze_diff(proj_id: str, req: DiffAnalysisRequest):
    """
    Analyzes Git diff between commits to identify which feature was changed
    and regenerates Diagram-as-Code with modified classes highlighted.
    """
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]

    diff_data = GitService.get_diff_summary(project.folder_path, commit_hash=req.commit_hash)
    if not diff_data.get("changed_files"):
        # If no git history or diff, inspect latest commit message
        commits = GitService.get_commit_history(project.folder_path, limit=1)
        commit_msg = commits[0]["message"] if commits else "Latest updates"
        diff_data["changed_files"] = list(project.classes.keys())[:3]
        diff_data["diff_text"] = "Sample diff changes across project classes"
    else:
        commits = GitService.get_commit_history(project.folder_path, limit=5)
        matched_commit = next((c for c in commits if c["hash"] == req.commit_hash), None) if req.commit_hash else (commits[0] if commits else None)
        commit_msg = matched_commit["message"] if matched_commit else "Recent commit modifications"

    analyzer = DiffAnalyzer()
    report = analyzer.analyze_diff(
        diff_text=diff_data.get("diff_text", ""),
        changed_files=diff_data.get("changed_files", []),
        commit_message=commit_msg,
        classes=project.classes
    )

    PROJECT_DIFF_REPORTS[proj_id] = report
    modified_classes = set(report.get("impacted_classes", []))

    # Regenerate diagrams highlighting modified classes
    diagram_engine = DiagramEngine()
    diagram_engine.generate_for_project(project, modified_classes=modified_classes)

    return {
        "project_id": proj_id,
        "diff_report": report,
        "modified_classes": list(modified_classes),
        "diagrams": [d.to_dict() for d in project.diagrams]
    }

@app.post("/api/projects/upload-zip")
async def upload_zip(name: str = Form(...), file: UploadFile = File(...)):
    proj_id = str(uuid.uuid4())[:8]
    target_dir = os.path.join(WORKSPACE_DIR, proj_id)
    os.makedirs(target_dir, exist_ok=True)

    zip_path = os.path.join(target_dir, file.filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid ZIP file: {str(e)}")

    project = Project(name=name, folder_path=target_dir)
    PROJECT_STORE[proj_id] = project

    return {
        "project_id": proj_id,
        "name": name,
        "folder_path": target_dir,
        "status": "extracted"
    }

@app.post("/api/projects/{proj_id}/analyze")
def analyze_project(proj_id: str):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")

    project = PROJECT_STORE[proj_id]

    extractor = SymbolExtractor()
    extracted_proj = extractor.scan_directory(project.folder_path, project_name=project.name)
    project.source_files = extracted_proj.source_files
    project.classes = extracted_proj.classes
    project.relationships = extracted_proj.relationships

    if not project.classes:
        raise HTTPException(status_code=400, detail="No parsable source classes discovered in repository.")

    cluster_engine = ClusterEngine()
    clusters = cluster_engine.cluster(list(project.classes.values()), project.relationships)

    labeller = FeatureLabeller()
    project.features = []
    for c in clusters:
        feat = labeller.label(c, project.classes)
        project.features.append(feat)

    diagram_engine = DiagramEngine()
    diagram_engine.generate_for_project(project)

    commits = GitService.get_commit_history(project.folder_path, limit=10)

    return {
        "project_id": proj_id,
        "files_count": len(project.source_files),
        "classes_count": len(project.classes),
        "relationships_count": len(project.relationships),
        "features": [f.to_dict() for f in project.features],
        "diagrams_count": len(project.diagrams),
        "recent_commits": commits
    }

@app.get("/api/projects/{proj_id}/features")
def get_features(proj_id: str):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]
    return {
        "project_id": proj_id,
        "features": [f.to_dict() for f in project.features],
        "all_classes": list(project.classes.keys()),
        "diff_report": PROJECT_DIFF_REPORTS.get(proj_id)
    }

@app.put("/api/projects/{proj_id}/features")
def update_features(proj_id: str, updated_features: List[UpdateFeatureRequest]):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]

    new_features: List[Feature] = []
    for uf in updated_features:
        feat = Feature(
            name=uf.name,
            description=uf.description or "",
            confidence=uf.confidence or 1.0
        )
        for c in uf.classes:
            feat.add_class(c, score=1.0, primary=True)
        new_features.append(feat)

    project.features = new_features

    diagram_engine = DiagramEngine()
    diagram_engine.generate_for_project(project)

    return {
        "status": "updated",
        "features": [f.to_dict() for f in project.features],
        "diagrams_count": len(project.diagrams)
    }

@app.get("/api/projects/{proj_id}/diagrams")
def get_diagrams(proj_id: str):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]
    return {
        "project_id": proj_id,
        "diagrams": [d.to_dict() for d in project.diagrams],
        "diff_report": PROJECT_DIFF_REPORTS.get(proj_id)
    }

@app.post("/api/projects/{proj_id}/evaluate")
def evaluate_project(proj_id: str, req: EvaluateRequest):
    if proj_id not in PROJECT_STORE:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECT_STORE[proj_id]

    gt = GroundTruth(repo_name=project.name, feature_mapping=req.ground_truth)
    eval_service = EvaluationService()
    results = eval_service.evaluate(gt, project.features)
    return results

# Mount compiled frontend if available
from fastapi.staticfiles import StaticFiles
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../frontend/dist"))
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
