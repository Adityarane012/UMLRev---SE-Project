# Complete UML and Data Flow Models (DFD)
## Comprehensive Diagram Specifications, Traceability, and Markup

This document consolidates all architectural and behavioral modeling artifacts created for the **AI-Assisted UMLRev** project across Software Engineering Lab Experiments 3 through 8.

---

## 1. Use Case Diagram (Exp 3)
- **Primary Source:** [B124_B129_Exp3.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp3.pdf)
- **Scope Boundary:** *AI-Assisted UML Generation Platform*

### Actors & Roles
1. **Software Developer:** Primary user uploading repositories, reviewing AI features, generating diagrams, and downloading Diagram-as-Code.
2. **Software Architect:** Reviews high-level feature-wise class and sequence diagrams to evaluate architectural integrity.
3. **Project Manager:** Monitors architecture evolution and project health via a centralized dashboard.
4. **QA Engineer:** Explores feature-specific diagrams to understand control flows and draft targeted test scenarios.
5. **System Administrator:** Manages user accounts, credentials, and repository permissions.
6. **New Team Member:** Explores interactive diagrams to onboard quickly without reading raw code.

### PlantUML Specification
```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Software Developer" as Dev
actor "Project Manager" as PM
actor "Software Architect" as Arch
actor "New Team Member" as NewMember
actor "QA Engineer" as QA
actor "System Admin" as Admin

rectangle "AI-Assisted UML Generation Platform" {
  usecase "Manage Project" as UC_Manage
  usecase "Upload or Connect Repo" as UC_Upload
  usecase "Analyze Project" as UC_Analyze
  usecase "AI Feature Identification" as UC_AI
  usecase "Review and Modify Features" as UC_Review
  usecase "Generate UML Class Diagram" as UC_GenClass
  usecase "Generate UML Sequence Diagram" as UC_GenSeq
  usecase "View UML Diagrams" as UC_View
  usecase "Interactive Diagram Exploration" as UC_Explore
  usecase "Generate Diagram-as-Code" as UC_DaC
  usecase "Export and Download Diagrams" as UC_Export
  usecase "View Diagram Versions" as UC_Versions
  usecase "Manage Users and Perms" as UC_AdminUsers
  usecase "Auth User" as UC_Auth
}

Dev --> UC_Manage
Dev --> UC_Upload
Dev --> UC_Analyze
Dev --> UC_Review
Dev --> UC_GenClass
Dev --> UC_GenSeq
Dev --> UC_View
Dev --> UC_Explore
Dev --> UC_DaC
Dev --> UC_Export
Dev --> UC_Auth

UC_Analyze ..> UC_Review : <<include>>
UC_AI ..> UC_Review : <<include>>
UC_Analyze ..> UC_AI : <<include>>

PM --> UC_Manage
PM --> UC_View
PM --> UC_Versions
PM --> UC_Auth

Arch --> UC_Manage
Arch --> UC_View
Arch --> UC_Explore
Arch --> UC_Versions
Arch --> UC_Auth

NewMember --> UC_View
NewMember --> UC_Explore
NewMember --> UC_Auth

QA --> UC_View
QA --> UC_Explore
QA --> UC_Auth

Admin --> UC_AdminUsers
Admin --> UC_Auth
@enduml
```

---

## 2. Activity Diagram (Exp 4)
- **Primary Sources:** [Activity Diagram UMLRev.mdj](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/Activity%20Diagram%20UMLRev.mdj), [ActivityDiagram UMLRev.jpg](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/ActivityDiagram%20UMLRev.jpg), [B124_B129_Exp4.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp4.pdf)

### Process Description
The activity diagram tracks the end-to-end lifecycle of analyzing a codebase:
1. User logs in and is authenticated.
2. The dashboard opens, allowing the user to create or select a project.
3. The user uploads a ZIP archive or connects a Git repository URL.
4. **Repository Validation Decision:**
   - If invalid -> Displays Repository Error and terminates.
   - If valid -> Proceeds to Project Analysis.
5. Codebase analysis triggers the **AI Feature Identification** engine.
6. The system displays identified features in the UI for developer inspection.
7. **Developer Review Decision ("Features Correct?"):**
   - If No -> Developer modifies/splits features, then re-verifies.
   - If Yes -> Advances to diagram generation.
8. **Parallel Generation (FORK):**
   - Branch A: Generate Class Diagram.
   - Branch B: Generate Sequence Diagram.
9. **Synchronization (JOIN):** Both diagrams merge into "UML Generation Complete", leading to the Final State.

### Mermaid Flowchart
```mermaid
flowchart TD
    Start((●)) --> Login[Login]
    Login --> Auth[Authenticate User]
    Auth --> Dashboard[Open Dashboard]
    Dashboard --> SelectProj[Create or Select Project]
    SelectProj --> UploadRepo[Upload or Connect Repository]
    UploadRepo --> ValidateRepo[Validate Repository]
    
    ValidateRepo --> CheckValid{Repository Valid?}
    CheckValid -- No --> DispErr[Display Repository Error]
    DispErr --> Stop((◉))
    
    CheckValid -- Yes --> Analyze[Analyze Project]
    Analyze --> AIFeature[AI Feature Identification]
    AIFeature --> DispFeat[Display Identified Features]
    DispFeat --> ReviewFeat[Review Identified Features]
    
    ReviewFeat --> CheckFeat{Features Correct?}
    CheckFeat -- No --> ModFeat[Modify Features]
    ModFeat --> DispFeat
    
    CheckFeat -- Yes --> ForkNode[=== FORK ===]
    ForkNode --> GenClass[Generate Class Diagram]
    ForkNode --> GenSeq[Generate Sequence Diagram]
    
    GenClass --> JoinNode[=== JOIN ===]
    GenSeq --> JoinNode
    
    JoinNode --> Complete[UML Generation Complete]
    Complete --> Final((◉))
```

---

## 3. Class Diagram (Exp 5)
- **Primary Sources:** [B124_B129_Exp5.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp5.pdf), [B124_B129_Exp5.docx](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp5.docx)

### Mermaid Class Diagram
```mermaid
classDiagram
    namespace model {
        class Project {
            -String name
            -String folderPath
            +analyse() void
        }
        class SourceFile {
            -String path
            +readContent() String
        }
        class ClassSymbol {
            -String name
            -String packageName
            +getImports() List~String~
        }
        class Feature {
            -String name
            -String description
            -Float confidence
            +memberCount() int
        }
        class FeatureMembership {
            -Float score
            +isPrimary() boolean
        }
        class Diagram {
            -String kind
            -String umlText
            +export() File
        }
    }

    namespace pipeline {
        class SymbolExtractor {
            +extract(file SourceFile) List~ClassSymbol~
        }
        class ClusterEngine {
            +cluster(classes List~ClassSymbol~) List~Cluster~
        }
        class Cluster {
            +size() int
            +classNames() List~String~
        }
        class FeatureLabeller {
            +label(cluster Cluster) Feature
        }
        class LLMClient {
            -String model
            +ask(prompt String) String
        }
    }

    namespace diagram {
        class DiagramEngine {
            +generate(feature Feature) List~Diagram~
        }
        class DiagramStrategy {
            <<interface>>
            +generate(feature Feature) Diagram
        }
        class ClassDiagramStrategy {
            +generate(feature Feature) Diagram
        }
        class SequenceDiagramStrategy {
            +generate(feature Feature) Diagram
        }
    }

    namespace evaluation {
        class GroundTruth {
            -String repoName
            +classesFor(name String) List~String~
        }
        class EvaluationService {
            +evaluate(expected GroundTruth, found List~Feature~) EvaluationMetrics
        }
    }

    Project "1" *-- "1..*" SourceFile
    SourceFile "1" *-- "0..*" ClassSymbol
    Project "1" --> "0..*" Feature : produces
    Feature "1..*" -- "1..*" ClassSymbol
    (Feature, ClassSymbol) .. FeatureMembership
    Feature "1" *-- "1..2" Diagram

    SymbolExtractor ..> SourceFile : reads
    SymbolExtractor ..> ClassSymbol : creates
    ClusterEngine ..> ClassSymbol : groups
    ClusterEngine "1" --> "0..*" Cluster
    FeatureLabeller ..> Cluster : names
    FeatureLabeller ..> Feature : creates
    FeatureLabeller "1" --> "1" LLMClient

    DiagramEngine "1" --> "1..*" DiagramStrategy
    ClassDiagramStrategy ..|> DiagramStrategy
    SequenceDiagramStrategy ..|> DiagramStrategy
    DiagramEngine ..> Diagram : creates

    EvaluationService ..> GroundTruth : reads
    EvaluationService ..> Feature : compares
```

---

## 4. Sequence Diagram (Exp 6)
- **Primary Sources:** [exp6 diagram.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/exp6%20diagram.png), [B124_B129_Exp6.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp6.pdf), [B124_B129_Exp6.docx](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp6.docx)

### Lifelines & Participants
- `actor Developer as Software Developer`
- `boundary Dashboard as Web Dashboard`
- `control Controller as Project Controller`
- `entity Repository as Repository Service`
- `entity Analyzer as Project Analyzer`
- `entity AI as AI Feature Identifier`
- `entity UML as UML Generator`

### Sequence Diagram PlantUML
```plantuml
@startuml
autonumber
actor "Software Developer" as Developer
boundary "Web Dashboard" as Dashboard
control "Project Controller" as Controller
entity "Repository Service" as Repository
entity "Project Analyzer" as Analyzer
entity "AI Feature Identifier" as AI
entity "UML Generator" as UML

== User Login ==
Developer -> Dashboard: login()
activate Dashboard
Dashboard -> Controller: authenticateUser()
activate Controller
Controller --> Dashboard: authenticationSuccess()
deactivate Controller
Dashboard --> Developer: showDashboard()
deactivate Dashboard

== Project Setup ==
Developer -> Dashboard: createOrSelectProject()
activate Dashboard
Dashboard -> Controller: createOrSelectProject()
activate Controller
Controller --> Dashboard: projectReady()
deactivate Controller
Dashboard --> Developer: showProject()
deactivate Dashboard

== Repository Processing ==
Developer -> Dashboard: uploadRepository()
activate Dashboard
Dashboard -> Controller: validateRepository()
activate Controller
Controller -> Repository: validateRepository()
activate Repository
Repository --> Controller: repositoryValid()
deactivate Repository

alt Repository Invalid
    Controller --> Dashboard: displayError()
    Dashboard --> Developer: showRepositoryError()
    Developer -> Dashboard: uploadRepository()
    Dashboard -> Controller: validateRepository()
else Repository Valid
    Controller --> Dashboard: repositoryValid()
    Dashboard --> Developer: repositoryAccepted()
end
deactivate Controller
deactivate Dashboard

== Project Analysis ==
Developer -> Dashboard: analyzeProject()
activate Dashboard
Dashboard -> Controller: analyzeProject()
activate Controller
Controller -> Analyzer: getSourceCode()
activate Analyzer
Analyzer -> Repository: getSourceCode()
activate Repository
Repository --> Analyzer: sourceCode()
deactivate Repository
Analyzer -> AI: identifyFeatures()
activate AI
AI --> Analyzer: featureSuggestions()
deactivate AI
Analyzer --> Controller: identifiedFeatures()
deactivate Analyzer
Controller --> Dashboard: displayFeatures()
deactivate Controller
Dashboard --> Developer: displayFeatures()
deactivate Dashboard

== Feature Review ==
Developer -> Dashboard: reviewFeatures()
activate Dashboard
Dashboard -> Controller: reviewFeatures()
activate Controller

alt Modify Features
    Developer -> Dashboard: modifyFeatures()
    Dashboard -> Controller: updateFeatures()
    Controller --> Dashboard: updatedFeatures()
    Dashboard --> Developer: showUpdatedFeatures()
else Approve Features
    Developer -> Dashboard: approveFeatures()
    Dashboard -> Controller: confirmFeatures()
    Controller --> Dashboard: featuresApproved()
    Dashboard --> Developer: approvalConfirmed()
end
deactivate Controller
deactivate Dashboard

== UML Generation ==
Developer -> Dashboard: generateUML()
activate Dashboard
Dashboard -> Controller: generateUML()
activate Controller
Controller -> UML: generateClassDiagram()
activate UML
UML --> Controller: classDiagramReady()
Controller -> UML: generateSequenceDiagram()
UML --> Controller: sequenceDiagramReady()
deactivate UML
Controller --> Dashboard: UMLDiagramsReady()
deactivate Controller
Dashboard --> Developer: displayUMLDiagrams()
Developer -> Dashboard: viewGeneratedDiagrams()
Dashboard --> Developer: showClassAndSequenceDiagrams()
deactivate Dashboard
@enduml
```

---

## 5. Collaboration / Communication Diagram (Exp 7)
- **Primary Source:** [B124_B129_Exp7.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp7.pdf)

### Object Links & Numbered Interactions
```plantuml
@startuml
title UMLRev - Collaboration (Communication) Diagram
object "developer : Software Developer" as Developer
object "dashboard : Web Dashboard" as Dashboard
object "controller : Project Controller" as Controller
object "repository : Repository Service" as Repository
object "analyzer : Project Analyzer" as Analyzer
object "ai : AI Feature Identifier" as AI
object "uml : UML Generator" as UML

Developer -- Dashboard : 1. login()\n2. uploadRepository()\n11. reviewFeatures()\n12. approveOrModifyFeatures()
Dashboard -- Controller : 3. authenticateUser()\n4. validateRepository()\n10. displayFeatures()\n13. generateUML()\n17. displayUMLDiagrams()
Controller -- Repository : 5. validateRepository()\n5.1 repositoryValid()
Controller -- Analyzer : 6. analyzeProject()
Analyzer -- Repository : 7. getSourceCode()
Analyzer -- AI : 8. identifyFeatures()\n9. featureSuggestions()
Controller -- UML : 14. generateClassDiagram()\n15. generateSequenceDiagram()
UML -- Controller : 16. UMLDiagramsReady()
Dashboard -- Developer : 18. viewGeneratedDiagrams()
@enduml
```

---

## 6. Data Flow Diagrams (Exp 8)
- **Primary Sources:** [umlrev_level0_dfd.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/umlrev_level0_dfd.png), [umlrev_level1_dfd.png](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/umlrev_level1_dfd.png), [B124_B129_Exp8.pdf](file:///c:/Users/Aditya%20Rane/OneDrive/Desktop/aditya/College%20MPSTME/sem5/SE/Project/B124_B129_Exp8.pdf)

### Level 0 DFD (Context Diagram)
- **External Entity 1:** `SOFTWARE DEVELOPER`
- **Process 0:** `AI-ASSISTED UML GENERATION SYSTEM`
- **External Entity 2:** `SOURCE CODE REPOSITORY`

```mermaid
flowchart LR
    Dev[SOFTWARE DEVELOPER]
    Sys((0.0<br/>AI-ASSISTED UML<br/>GENERATION SYSTEM))
    Repo[SOURCE CODE REPOSITORY]

    Dev -- "Project details, repository URL /<br/>uploaded source code, analysis request" --> Sys
    Sys -- "Feature suggestions, analysis status,<br/>review feedback and UML diagrams" --> Dev

    Sys -- "Repository access request /<br/>source-code retrieval" --> Repo
    Repo -- "Source files and project structure" --> Sys
```

### Level 1 DFD (Subsystem Decomposition)
The Level 1 diagram expands Process 0 into 6 modular processes interacting with 3 centralized data stores:

#### Processes
- **1.0 User & Project:** Handles authentication, dashboard initialization, and project creation.
- **2.0 Repository Check:** Validates repository formats (ZIP or remote Git URL) and verifies branch access.
- **3.0 Code Analysis:** Parses files, extracts symbol tables, builds dependencies.
- **4.0 AI Feature ID:** Invokes semantic clustering and LLM feature identification.
- **5.0 Feature Review:** Ingests user adjustments, approves feature sets, and locks feature scopes.
- **6.0 UML Generation:** Invokes diagram strategies to produce Class and Sequence diagrams.

#### Data Stores
- **D1: User / Project Data:** Stores user profiles, credentials, project metadata, and session status.
- **D2: Repo / Analysis Data:** Stores cloned repository files, AST caches, symbol graphs, and analysis logs.
- **D3: Features / UML:** Stores identified feature boundaries, approved feature sets, generated SVG/PNG diagrams, and PlantUML text files.

```mermaid
flowchart TD
    Dev[DEVELOPER]
    Repo[CODE REPOSITORY]

    P1((1.0<br/>User & Project))
    P2((2.0<br/>Repository Check))
    P3((3.0<br/>Code Analysis))
    P4((4.0<br/>AI Feature ID))
    P5((5.0<br/>Feature Review))
    P6((6.0<br/>UML Generation))

    D1[[(D1) User / Project Data]]
    D2[[(D2) Repo / Analysis Data]]
    D3[[(D3) Features / UML]]

    Dev <-->|Login / project / Status| P1
    Dev -->|Repo URL / source| P2
    Dev <-->|Edits / approval| P5
    P6 -->|Class & Sequence diagrams| Dev

    P1 -->|Project info| P2
    P1 -->|Save / read| D1
    
    P2 -->|Access request| Repo
    Repo -->|Source files| P3
    P2 -->|Valid code| P3
    P2 -->|Validation / status| Dev
    P2 -->|Repo metadata| D2

    P3 -->|Code context| P4
    P4 -->|Suggestions| P5
    P4 <-->|Save / read| D2
    P4 -->|Suggestions / status| Dev

    P5 -->|Approved features| P6
    P5 -->|Approved metadata| D2
    
    P6 <-->|Save / read UML| D3
```
