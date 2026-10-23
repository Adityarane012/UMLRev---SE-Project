# Automated Feature Identification for Continuous Reverse Engineering of UML Models
## Project Overview & Academic Context

---

### 1. Academic & Student Context
- **Institution:** Mukesh Patel School of Technology Management & Engineering (MPSTME), NMIMS University
- **Course:** Software Engineering (SE), Semester 5, B.Tech Computer Engineering (Div B, Batch B2)
- **Project Team:**
  - **Jay Gandhi** (Roll No. **B124**)
  - **Aditya Rane** (Roll No. **B129**)
- **Academic Milestone:** Term Mini-Project / Lab Continuous Assessment (Experiments 1 to 8)
- **Primary Source Document:** `B124_B129_SEProject.pdf` (held locally; not published in this repository)

---

### 2. Executive Summary
Modern software engineering practices follow **Agile development** and **Continuous Integration / Continuous Deployment (CI/CD)** pipelines. While codebases evolve rapidly with daily or hourly commits, software architecture documentation (specifically **Unified Modeling Language (UML)** models) quickly degrades and becomes obsolete. Developers rarely update diagrams by hand due to tight release deadlines and significant cognitive overhead.

To counter software design drift, recent research proposed **UMLRev** (*A Context-Aware Feature-Oriented Approach to Support Continuous Reverse Engineering of UML Models*), an automated tool that extracts execution traces during CI test runs and reverse-engineers feature-centric UML class and sequence diagrams.

However, **UMLRev has a fundamental limitation**:
> **The Manual Feature Identification Bottleneck:** UMLRev requires software developers to manually define features and explicitly bind them to execution traces/test scenarios prior to reverse engineering. For legacy systems or large-scale projects with hundreds of classes and dynamic execution flows, this manual mapping is tedious, error-prone, and severely limits automated continuous reverse engineering.

This project, developed by **Jay (B124)** and **Aditya (B129)**, enhances the UMLRev paradigm by introducing **Automated Feature Identification**:
1. **Automated Static & Semantic Analysis:** Parsing source code to extract structural symbols (`ClassSymbol`, imports, methods, relationships).
2. **AI / LLM Clustering & Feature Labeling:** Grouping cohesive classes into feature clusters and using Large Language Models (LLMs) to automatically detect and name software features.
3. **Human-in-the-Loop Verification:** Giving developers a web dashboard to review, approve, or adjust AI-suggested feature boundaries before final diagram generation.
4. **Continuous Diagram Generation:** Synthesizing feature-specific UML Class and Sequence diagrams (both interactive visual representations and downloadable PlantUML Diagram-as-Code artifacts) directly in the CI/CD pipeline.

---

### 3. Core Problem Statement & Need for the Topic
```
+----------------------------------------------------------------------------------------------------+
|                                    TRADITIONAL REVERSE ENGINEERING                                 |
| - Monolithic, massive diagrams that overwhelm developers.                                          |
| - Disconnected from release pipelines; updated manually or irregularly.                           |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+----------------------------------------------------------------------------------------------------+
|                                  BASE RESEARCH PARADIGM: UMLRev                                    |
| - Feature-oriented (decomposes diagrams by user feature, not entire system at once).               |
| - Non-intrusive runtime trace capture using AspectJ pointcuts during CI test runs.                 |
| ❌ BOTTLENECK: Relies on developers to MANUALLY identify and map features to tests.                 |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+----------------------------------------------------------------------------------------------------+
|                         ADITYA & JAY'S ENHANCEMENT: AI-ASSISTED UMLRev                             |
| - Symbol extraction (AST parsing) + Semantic clustering of source code.                            |
| - Automated feature identification (clustering, then LLM or heuristic labelling).                  |
| - Interactive review dashboard for developer oversight.                                            |
| - Synchronized, continuous, and automated UML generation across CI/CD releases.                    |
+----------------------------------------------------------------------------------------------------+
```

---

### 4. Key Functional Capabilities
1. **Repository Ingestion:** Clone any public GitHub repository from the dashboard, or point the CLI at a local directory.
2. **Automated Symbol Extraction:** Extract classes, methods, package scopes, and inheritance/dependency hierarchies.
3. **Feature Mining & Clustering:** Group source files into functional clusters and infer high-level business feature names with confidence scores.
4. **Developer Review Loop:** Web dashboard allowing architects and developers to accept, split, or rename feature clusters.
5. **Multi-Diagram Generation:** Automatically output:
   - **UML Class Diagrams** representing structural feature views.
   - **UML Sequence Diagrams** illustrating dynamic runtime interactions.
   - **Diagram-as-Code:** PlantUML and Mermaid markup for version-controlled documentation.
6. **Commit Impact Analysis:** Reads commit history, determines which features a commit touches, and regenerates the affected diagrams with the modified classes highlighted. *(Webhook-triggered regeneration inside a hosted CI pipeline remains future work.)*

---

### 5. Repository File Reference
All project deliverables and reference artifacts are stored within the project:
- **Base Research Paper:** [UMLRev Paper (IEEE Access 2026)](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/reference/UMLRev_A_Context-Aware_Feature-Oriented_Approach_to_Support_Continuous_Reverse_Engineering_of_UML_Models.pdf)
- **Project Proposal Document:** `B124_B129_SEProject.pdf` (held locally; not published in this repository)
- **StarUML Activity Model:** [Activity Diagram UMLRev.mdj](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/diagrams/Activity%20Diagram%20UMLRev.mdj) and export [ActivityDiagram UMLRev.jpg](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/diagrams/ActivityDiagram%20UMLRev.jpg)
- **Sequence Diagram Export:** [exp6 diagram.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/exp6%20diagram.png)
- **Data Flow Diagrams:**
  - Level 0 Context Diagram: [umlrev_level0_dfd.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/diagrams/umlrev_level0_dfd.png)
  - Level 1 Decomposition: [umlrev_level1_dfd.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/diagrams/umlrev_level1_dfd.png)
- **SE Course Lab Reports (Exp 1 - Exp 8):** Cataloged in [lab_reports/](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports)
