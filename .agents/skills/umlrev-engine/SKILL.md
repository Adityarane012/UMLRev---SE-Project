---
name: umlrev-engine
description: Commands and operational guidance for running, testing, and generating continuous UML models using the AI-Assisted UMLRev reverse engineering pipeline.
---

# UMLRev Engine Skill: AI-Assisted Continuous Reverse Engineering

This skill teaches agents how to execute, test, and interact with the **AI-Assisted UMLRev** reverse engineering engine.

## Overview
The system analyzes codebases (Java, Python, TypeScript) using static AST parsing, clusters classes into candidate functional units, queries an LLM to predict software features with confidence scores, and produces feature-specific UML Class and Sequence diagrams.

## Core Workflows

### 1. Headless Reverse Engineering (CLI)
To run the automated analysis on a repository:
```bash
python -m umlrev.cli --repo "<path_to_repository>" --output "output_dir"
```
Flags:
- `--repo`: Path to local folder or unpacked ZIP containing source code.
- `--output`: Destination directory for generated diagrams (`.puml`, `.svg`, `.json`).
- `--features`: (Optional) Path to manual feature override JSON if review was conducted.

### 2. Launching the Backend REST API
The backend runs on FastAPI / Uvicorn:
```bash
python -m uvicorn umlrev.api.app:app --host 127.0.0.1 --port 8000 --reload
```
Available endpoints:
- `POST /api/projects/upload`: Ingest repository
- `POST /api/projects/analyze`: Run AST extraction & AI feature clustering
- `GET /api/projects/{id}/features`: Retrieve identified features
- `PUT /api/projects/{id}/features`: Modify/approve features (Human-in-the-Loop)
- `POST /api/projects/{id}/generate-uml`: Generate Class and Sequence diagrams
- `GET /api/projects/{id}/export`: Download PlantUML package

### 3. Launching the Interactive Frontend Dashboard
```bash
cd frontend
npm run dev
```
Runs the Vite dev server with the interactive UML Explorer (pan/zoom/search/export).

### 4. Running Benchmark Evaluations
To evaluate the clustering accuracy against Ground Truth:
```bash
python -m umlrev.evaluation.benchmark --ground-truth "ground_truth.json"
```
Reports Precision, Recall, and F1-score.
