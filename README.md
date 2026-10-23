# UMLRev

Continuous reverse engineering of UML models with automated feature identification.

Developed by **Jay Gandhi (B124)** and **Aditya Rane (B129)** for the Software Engineering (SE) Semester 5 curriculum at MPSTME, NMIMS University.

The project contains the reverse engineering engine, semantic clustering pipeline, React web dashboard, benchmark test suites, and academic documentation.

---

## Directory Layout

```
UMLRev/
├── README.md                      # Project documentation and usage guide
├── run_system.py                  # System launcher (demo, cli, backend, frontend, benchmark)
├── docs/                          # SE documentation suite (Exp 1 - 8 and IEEE paper analysis)
│   ├── B124_B129_UMLRev_MiniProject_Report.docx  # Mini project report (submission deliverable)
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
| **[docs/01_project_overview.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/01_project_overview.md)** | **Project Overview:** Student details (B124/B129), documentation drift, and how automated feature clustering removes the manual tagging bottleneck in UMLRev. |
| **[docs/02_base_paper_summary.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/02_base_paper_summary.md)** | **Base Research Paper Analysis:** Breakdown of *UMLRev (IEEE Access 2026)*, covering FOSD principles, AspectJ tracing, component architecture, and the manual annotation gap. |
| **[docs/03_system_architecture_and_ai_pipeline.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/03_system_architecture_and_ai_pipeline.md)** | **System Architecture and Analysis Pipeline:** Structural design of the four backend packages, AST symbol extraction, semantic clustering, and diagram strategies. |
| **[docs/04_uml_and_dfd_models.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/04_uml_and_dfd_models.md)** | **Visual Models:** PlantUML and Mermaid specifications for Use Case, Activity, Class, Sequence, Collaboration, and Data Flow Diagrams. |
| **[docs/B124_B129_UMLRev_MiniProject_Report.docx](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/B124_B129_UMLRev_MiniProject_Report.docx)** | **Mini Project Report (submission deliverable):** Introduction and authors, problem statement with objectives O1-O7 and scope, architecture and design diagrams, measured results with screenshots, conclusion and references. |
| **[docs/05_se_lab_experiments_traceability.md](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/05_se_lab_experiments_traceability.md)** | **Lab Experiments and Traceability:** Traceability matrix linking User Stories, NFRs, Use Cases, Activities, Classes, Sequence Diagrams, and DFDs across Experiments 1 to 8. |

---

## Running the System

Use `run_system.py` to launch the dashboard, run the CLI, or execute benchmarks:

### 1. Launch the Full Demo (recommended)
Builds the frontend if needed, serves the dashboard and REST API together on one port, and opens a browser:
```powershell
python run_system.py demo
```
The dashboard ingests **public GitHub repositories**; the CLI below covers local directories.

### 2. Run Automated CLI Benchmark
Executes the reverse engineering pipeline on the IEEE "Tell Story" benchmark and exports PlantUML diagrams into `output/`:
```powershell
python run_system.py benchmark
```

### 3. Launch FastAPI REST Backend
Starts the FastAPI server on `http://127.0.0.1:8000`:
```powershell
python run_system.py backend
```
Interactive Swagger documentation is available at: `http://127.0.0.1:8000/docs`

### 4. Launch Frontend Dev Server (hot reload)
Starts the Vite development server:
```powershell
python run_system.py frontend
```
Open `http://127.0.0.1:5173` in your browser.

### 5. Custom Repository Analysis (CLI)
Reverse engineer any local repository:
```powershell
python run_system.py cli --repo "path/to/source_code" --output "output/my_project"
```

### 6. Run Automated Tests
Executes the backend unit and integration test suite:
```powershell
python -m unittest discover -s backend/tests -p "test_*.py"
```

---

## Verification and Quality Metrics

### Regression benchmark: IEEE Access "Tell Story" project
The pipeline is given the source directory only, with no feature information of any kind.
This is a **regression check that the pipeline still reproduces a known mapping end to end**,
not a measurement of general accuracy - see the caveats below the table.

| Measure | Result |
|---|---|
| Source files parsed | 4 |
| Discovered classes | 4 (`Enemy`, `Hero`, `Princess`, `Story`) |
| Discovered relationships | 7 (field associations, method calls, dependencies) |
| Clusters formed | 1 |
| Feature identified | "Tell Story" (confidence 96.0%) |
| True positives / false positives / false negatives | 4 / 0 / 0 |
| **Precision / Recall / F1** | **100.0% / 100.0% / 1.00** |

Scoring operates on individual feature-to-class assignments, so a partially correct cluster is
partially credited. F1 is quoted rather than precision or recall alone because each of those is
trivially gamed in isolation.

**How much this result proves.** Not much on its own, and it should not be read as an accuracy
figure:
- The reference project has **one** feature and **four tightly coupled classes** (`Story` holds a
  field of each of the other three), so there is almost no room for a false positive or a false
  negative. A perfect score is close to the expected outcome.
- `FeatureLabeller` falls back to `LLMClient._heuristic_fallback`, which contains a keyword branch
  returning the name `"Tell Story"` for this project's vocabulary. On this benchmark the **feature
  name is recalled, not derived** - the clustering is genuinely automatic, the label is not.
- Matching a discovered feature name against a reference name is a lenient substring test, so the
  score is driven far more by the class grouping than by the chosen name.

Treat a pass as evidence that extraction and clustering still work end to end. Establishing
accuracy would require reference mappings for several projects with multiple features each.

### Scale
| Repository | Scale | Outcome |
|---|---|---|
| UMLRev itself | 250 files, 229 classes, 550 relationships | 8 features, 16 diagrams, ~14 s |
| `pallets/click` | 174 classes | 8 features, all diagrams rendered |

### Test and output validation
- **12/12** unit and integration tests pass, including TC-01 to TC-04 from Experiment 9.
- **32/32** generated diagrams parse cleanly against the Mermaid parser (16 from initial
  analysis, 16 regenerated with commit-diff highlighting). Stage 4 of the dashboard reports
  this verdict per diagram, and shows the parser's own error plus the offending source line
  when a diagram fails.
