# Software Engineering Lab Experiments & Traceability Matrix
## Complete Academic Record (Exp 1 - Exp 8) | MPSTME Semester 5

---

### 1. Overview & Lab Structure
In Semester 5 Software Engineering (B.Tech Computer Engineering, MPSTME, NMIMS University), students **Jay Gandhi (B124)** and **Aditya Rane (B129)** carried out a continuous semester-long case study developing the **AI-Assisted UMLRev** platform. 

This document tracks how the requirements evolved from initial user stories to formal data flow diagrams across all 8 laboratory experiments.

---

### 2. Experiment-by-Experiment Breakdown

```
┌──────┬────────────────────────────────────────────────────────┬───────────────────────────────────┐
│ Exp  │ Topic & Modeling Dimension                             │ Deliverable Artifact              │
├──────┼────────────────────────────────────────────────────────┼───────────────────────────────────┤
│ 1    │ Agile Functional Requirements (User Stories)           │ B124_B129_Exp1.pdf                │
│ 2    │ Non-Functional Requirements (NFRs) & Definition of Done│ B124_B129_Exp2.pdf                │
│ 3    │ Scenario-Based Modeling (Use Case Diagram)             │ B124_B129_Exp3.pdf                │
│ 4    │ Behavioral Flow Modeling (Activity Diagram)            │ Activity Diagram UMLRev.mdj / jpg │
│ 5    │ Structural & Domain Modeling (Class Diagram)           │ B124_B129_Exp5.pdf / docx         │
│ 6    │ Dynamic Behavioral Modeling (Sequence Diagram)         │ exp6 diagram.png / Exp6.pdf       │
│ 7    │ Dynamic Collaboration Modeling (Communication Diagram) │ B124_B129_Exp7.pdf                │
│ 8    │ Information & Data Flow Modeling (DFD Level 0 & 1)     │ umlrev_level0_dfd.png & level1    │
│ 9    │ Software Testing Techniques (TC-01 to TC-04 QA Matrix) │ B124_B129_Exp9.docx / test_api.py │
│ 10   │ System Implementation & Post-Testing Deployment        │ B124_B129_Exp10.docx              │
└──────┴────────────────────────────────────────────────────────┴───────────────────────────────────┘
```

---

### 3. Deep Dive into Lab Experiments

#### Experiment 1: Functional User Stories & Acceptance Criteria
- **Reference:** [B124_B129_Exp1.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp1.pdf)
- **Roles & User Stories:**
  1. **Software Developer:**
     - *Story:* "As a Software Developer, I want to upload my project, have the system automatically identify software features using AI, generate UML diagrams, and export them as editable Diagram-as-Code so that I can quickly document, maintain, and version-control my software architecture."
     - *Acceptance Criteria:* ZIP / Git repo support; AI auto-detection with developer review; successful Class and Sequence diagram generation; downloadable and editable PlantUML files.
  2. **Software Architect:**
     - *Story:* "As a Software Architect, I want to review feature-wise UML diagrams so that I can analyze the system architecture and validate design decisions."
     - *Acceptance Criteria:* Feature-organized diagrams; accurate reflection of latest codebase; intuitive diagram inspection.
  3. **Project Manager:**
     - *Story:* "As a Project Manager, I want to monitor generated UML documentation through a centralized dashboard so that I can understand project architecture and track development progress without reading source code."
     - *Acceptance Criteria:* Centralized dashboard displaying analyzed projects; easy diagram navigation; historical analysis archives.
  4. **Quality Assurance Engineer:**
     - *Story:* "As a QA Engineer, I want to view feature-specific UML diagrams so that I can better understand application workflows and prepare effective test cases."
     - *Acceptance Criteria:* Filter diagrams by feature; accurate structural and sequence views matching feature workflows.
  5. **DevOps Engineer:**
     - *Story:* "As a DevOps Engineer, I want the platform to integrate with the project's repository so that UML documentation can be regenerated whenever the codebase is updated."
     - *Acceptance Criteria:* Webhook / CI trigger on Git commits; automated regeneration of diagrams.
  6. **System Administrator:**
     - *Story:* "As a System Administrator, I want to manage user accounts, repositories, and access permissions so that the platform remains secure and accessible only to authorized users."
     - *Acceptance Criteria:* CRUD user management; Role-Based Access Control (RBAC); per-repository access enforcement.

---

#### Experiment 2: Non-Functional Requirements & Definition of Done
- **Reference:** [B124_B129_Exp2.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp2.pdf)
- **NFR Specifications:**
  1. **Performance:** AI feature identification finishes in $\le$ 30 seconds for repositories up to 5,000 files; diagram generation finishes in $\le$ 60 seconds; dashboard pages load in $\le$ 3 seconds.
  2. **Availability:** System achieves $\ge$ 99% operational uptime; planned maintenance is announced in advance with fallback messaging.
  3. **Security:** Mandatory authentication; strict workspace boundary isolation; encrypted source code handling.
  4. **Reliability:** Descriptive error handling for corrupted syntax or missing dependencies; idempotent diagram synthesis.
  5. **Usability:** End-to-end generation accomplished in $\le$ 3 user actions; interactive viewer supports pan, zoom, and symbol searching.
  6. **Scalability:** Handles $\ge$ 100 concurrent developers without performance degradation.
  7. **Maintainability:** Modular, decoupled architecture separating frontend, backend, AI clustering, and diagram engines.
- **Definition of Done (DoD):**
  - All functional user story acceptance criteria met.
  - AI-assisted feature identification executes reliably on benchmark code.
  - UML Class and Sequence diagrams synthesize cleanly.
  - PlantUML source code is downloadable.
  - Interactive viewer passes pan/zoom/search tests.
  - RBAC and auth tests verified.
  - Performance and security thresholds validated.
  - Documentation and architectural models updated.

---

#### Experiment 3: Scenario-Based Modeling (Use Case Diagram)
- **Reference:** [B124_B129_Exp3.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp3.pdf)
- **Key Relationships:**
  - `Analyze Project` includes `Review and Modify Features`.
  - `AI Feature Identification` includes `Review and Modify Features`.
  - Clear separation between Developer-facing creative tasks, Architect review tasks, and System Admin management tasks.

---

#### Experiment 4: Behavioral Modeling (Activity Diagram)
- **Reference:** [Activity Diagram UMLRev.mdj](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/docs/diagrams/Activity%20Diagram%20UMLRev.mdj)
- **Key Control Structures:**
  - Branching decision on repository validation (`Repository Valid?`).
  - Iterative human-in-the-loop review loop (`Features Correct?` -> `Modify Features` -> retry).
  - Concurrency modeling: `FORK` splitting diagram generation into parallel asynchronous workers for Class and Sequence diagrams, synchronized by a `JOIN` before completion.

---

#### Experiment 5: Structural Modeling (Class Diagram)
- **Reference:** [B124_B129_Exp5.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp5.pdf)
- **Key Highlights:**
  - Implementation of the **Strategy Pattern** for diagram types.
  - Multi-tiered domain model with `FeatureMembership` handling fuzzy, many-to-many class memberships.
  - Decoupled `evaluation` package enabling benchmarking against ground truth.

---

#### Experiment 6: Behavioral Interaction Modeling (Sequence Diagram)
- **Reference:** [exp6 diagram.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/exp6%20diagram.png)
- **Key Highlights:**
  - 7 lifelines spanning boundaries, controllers, and services.
  - Alternative frames (`alt`) covering negative and positive branches for repo validation and feature approvals.
  - Distinct message flow showing synchronous requests vs asynchronous diagram worker callbacks.

---

#### Experiment 7: Collaboration / Communication Modeling
- **Reference:** [B124_B129_Exp7.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp7.pdf)
- **Key Highlights:**
  - Emphasizes structural topology between objects.
  - 18 chronological messages directly mirroring the Sequence Diagram.

---

#### Experiment 8: Data Flow Modeling (DFD Levels 0 and 1)
- **Reference:** [B124_B129_Exp8.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp8.pdf)
- **Key Highlights:**
  - Level 0 context diagram clarifying boundaries with external actors and remote repositories.
  - Level 1 decomposition detailing data stores `D1` (User/Project), `D2` (Repo/Analysis), and `D3` (Features/UML).

---

#### Experiment 9: Software Testing Techniques (Black-Box, Boundary, Integration & End-to-End)
- **Reference:** [B124_B129_Exp9.docx](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/lab_reports/B124_B129_Exp9.docx) and [test_api.py](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/UMLRev/backend/tests/test_api.py)
- **Key Test Cases & Execution Results:**
  1. **TC-01 (Login & Dashboard Access — Functional Testing):**
     - *Objective:* Validate credential verification, token issuance, and dashboard unlock.
     - *Result:* **PASS** — Token issued with role `Software Developer`; dashboard unlocked for Aditya Rane (B129).
  2. **TC-02 (Repository Validation — Negative & Boundary Testing):**
     - *Objective:* Validate system rejection of invalid URLs, empty folders, and unsupported file formats.
     - *Result:* **PASS** — HTTP 400 Bad Request returned with descriptive messages; pipeline execution safely aborted.
  3. **TC-03 (AI Feature Identification & Review — Integration Testing):**
     - *Objective:* Validate automated clustering suggestions, interactive human-in-the-loop review, and persistence of developer approval.
     - *Result:* **PASS** — Feature renamed, descriptions modified, member classes updated, and changes persisted via `PUT /api/projects/{id}/features`.
  4. **TC-04 (UML Diagram Generation — End-to-End Testing):**
     - *Objective:* Validate automated synthesis and visual export of Class and Sequence diagrams.
     - *Result:* **PASS** — Both Class and Sequence diagrams generated cleanly in PlantUML and Mermaid formats with zero syntax errors.

---

### 4. Cross-Experiment Traceability Matrix

| Requirement / Concept | Exp 1 (Story) | Exp 2 (NFR/DoD) | Exp 3 (Use Case) | Exp 4 (Activity) | Exp 5 (Class) | Exp 6 & 7 (Seq / Collab) | Exp 8 (DFD) | Exp 9 (Testing QA) |
|---|---|---|---|---|---|---|---|---|
| **User Authentication** | Admin & Dev Stories | Sec & DoD | `Auth User` | Login / Auth User | `model.Project` | `login()`, `authSuccess()` | `1.0 User & Project` / `D1` | **TC-01** (Login & Dashboard Access - PASS) |
| **Repository Ingestion** | Developer Story 1 | Usability & Perf | `Upload or Connect Repo` | Upload / Validate Repo | `SourceFile` | `uploadRepository()`, `validate()` | `2.0 Repository Check` | **TC-02** (Repository Validation - PASS) |
| **AST Symbol Extraction** | Developer Story 1 | DoD | `Analyze Project` | `Analyze Project` | `SymbolExtractor`, `ClassSymbol` | `getSourceCode()` | `3.0 Code Analysis` / `D2` | **TC-03** (Discovers classes & symbols - PASS) |
| **AI Feature Identification** | Developer Story 1 | Perf ($\le$ 30s) & DoD | `AI Feature ID` | `AI Feature Identification` | `ClusterEngine`, `FeatureLabeller`, `LLMClient` | `identifyFeatures()`, `featureSuggestions()` | `4.0 AI Feature ID` / `D2` | **TC-03** (AI Feature Discovery - PASS) |
| **Human-in-the-Loop Review** | Developer Story 1 | Usability ($\le$ 3 steps) | `Review and Modify Features` | `Review Features`, `Features Correct?` | `Feature.memberCount()`, `FeatureMembership` | `reviewFeatures()`, `modifyFeatures()`, `approve()` | `5.0 Feature Review` | **TC-03** (Modify & Approve List - PASS) |
| **Class Diagram Synthesis** | Dev & Arch Stories | Perf ($\le$ 60s) & DoD | `Gen Class Diagram` | `Generate Class Diagram` (Fork) | `ClassDiagramStrategy` | `generateClassDiagram()` | `6.0 UML Gen` / `D3` | **TC-04** (UML Class Diagram - PASS) |
| **Sequence Diagram Synthesis**| Dev & QA Stories | Perf ($\le$ 60s) & DoD | `Gen Sequence Diagram` | `Generate Sequence Diagram` (Fork) | `SequenceDiagramStrategy`| `generateSequenceDiagram()` | `6.0 UML Gen` / `D3` | **TC-04** (UML Sequence Diagram - PASS) |
| **Diagram-as-Code (PlantUML)**| Developer Story 1 | DoD (Exportable) | `Gen Diagram-as-Code` | `UML Generation Complete` | `Diagram.export()` | `viewGeneratedDiagrams()` | `D3 Features / UML` | **TC-04** (PlantUML & Mermaid Export - PASS) |
