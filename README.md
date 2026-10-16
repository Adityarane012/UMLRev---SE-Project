# AI-Assisted UMLRev

Continuous reverse engineering of UML models with automated AI feature identification.

Developed by **Jay Gandhi (B124)** and **Aditya Rane (B129)** for the Software Engineering (SE) Semester 5 curriculum at MPSTME, NMIMS University.

The project contains the reverse engineering engine, AI clustering pipeline, React web dashboard, benchmark test suites, and academic documentation.

---

## Directory Layout

```
UMLRev/
├── README.md                      # Project documentation and usage guide
├── run_system.py                  # System launcher (cli, backend, frontend, benchmark)
├── docs/                          # SE documentation suite (Exp 1 - 8 and IEEE paper analysis)
│   ├── B124_B129_SEProject.pdf    # Official project report
│   ├── 01_project_overview.md
│   ├── 02_base_paper_summary.md
│   ├── 03_system_architecture_and_ai_pipeline.md
│   ├── 04_uml_and_dfd_models.md
│   ├── 05_se_lab_experiments_traceability.md
│   └── diagrams/                  # StarUML (.mdj), DFDs, and diagram assets
├── backend/                       # Python reverse engineering core and FastAPI REST API
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template for API keys and server ports
│   ├── tests/                     # Unit and integration test suite
│   │   ├── test_extractor.py
│   │   ├── test_clustering.py
│   │   └── test_api.py
│   └── umlrev/
│       ├── cli.py                 # CLI runner for headless continuous analysis
│       ├── api/app.py             # FastAPI REST endpoints
│       ├── model/                 # Project, ClassSymbol, Feature, and Diagram entities
│       ├── pipeline/              # Extractor, ClusterEngine, FeatureLabeller, GitService, DiffAnalyzer
│       ├── diagram/               # DiagramEngine with Class and Sequence strategies
│       └── evaluation/            # Benchmark service computing Precision, Recall, and F1
├── frontend/                      # Web dashboard (React 19 + Vite)
│   ├── src/
│   │   ├── App.jsx                # Coordinator layout
│   │   ├── services/api.js        # REST API client
│   │   └── components/            # Modular tab and stage components
│   ├── dist/                      # Production distribution build
│   └── package.json
├── examples/                      # Test benchmark repositories
│   └── tell_story/                # IEEE Access benchmark (Story, Hero, Enemy, Princess)
├── output/                        # Destination for exported PlantUML diagrams and JSON summaries
└── reference/                     # Base IEEE research paper and reference implementation
    ├── UMLRev_A_Context-Aware_Feature-Oriented_Approach_to_Support_Continuous_Reverse_Engineering_of_UML_Models.pdf
    └── reference-umlrev/
```

---

## Documentation Index

The `docs/` directory documents the project specifications and curriculum requirements:

| Document | Purpose and Contents |
|---|---|
| **[docs/01_project_overview.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/01_project_overview.md)** | **Project Overview:** Student details (B124/B129), documentation drift, and how AI feature clustering removes the manual tagging bottleneck in UMLRev. |
| **[docs/02_base_paper_summary.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/02_base_paper_summary.md)** | **Base Research Paper Analysis:** Breakdown of *UMLRev (IEEE Access 2026)*, covering FOSD principles, AspectJ tracing, component architecture, and the manual annotation gap. |
| **[docs/03_system_architecture_and_ai_pipeline.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/03_system_architecture_and_ai_pipeline.md)** | **System Architecture and AI Pipeline:** Structural design of the four backend packages, AST symbol extraction, semantic clustering, and diagram strategies. |
| **[docs/04_uml_and_dfd_models.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/04_uml_and_dfd_models.md)** | **Visual Models:** PlantUML and Mermaid specifications for Use Case, Activity, Class, Sequence, Collaboration, and Data Flow Diagrams. |
| **[docs/05_se_lab_experiments_traceability.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/05_se_lab_experiments_traceability.md)** | **Lab Experiments and Traceability:** Traceability matrix linking User Stories, NFRs, Use Cases, Activities, Classes, Sequence Diagrams, and DFDs across Experiments 1 to 8. |

---

## Running the System

Use `run_system.py` to run the CLI, start the servers, or execute benchmarks:

### 1. Run Automated CLI Benchmark
Executes the reverse engineering pipeline on the IEEE "Tell Story" benchmark and exports PlantUML diagrams into `output/`:
```powershell
python run_system.py benchmark
```

### 2. Launch FastAPI REST Backend
Starts the FastAPI server on `http://127.0.0.1:8000`:
```powershell
python run_system.py backend
```
Interactive Swagger documentation is available at: `http://127.0.0.1:8000/docs`

### 3. Launch Interactive Web Dashboard
Starts the Vite development server:
```powershell
python run_system.py frontend
```
Open `http://127.0.0.1:5173` in your browser.

### 4. Custom Repository Analysis (CLI)
Reverse engineer any local repository:
```powershell
python run_system.py cli --repo "path/to/source_code" --output "output/my_project"
```

### 5. Run Automated Tests
Executes the backend unit and integration test suite:
```powershell
python -m unittest discover -s backend/tests -p "test_*.py"
```

---

## Verification and Quality Metrics

Results on the IEEE Access benchmark project:
- **Discovered Classes:** 4 (`Enemy`, `Hero`, `Princess`, `Story`)
- **Discovered Relationships:** 13 (Field associations, method calls, dependencies)
- **AI Feature Identified:** "Tell Story" (Confidence: 95.0%)
- **Precision:** 100.0%
- **Recall:** 100.0%
- **F1 Score:** 1.00
