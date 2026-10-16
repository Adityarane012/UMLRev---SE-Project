import argparse
import os
import json
from pathlib import Path
from .pipeline.extractor import SymbolExtractor
from .pipeline.clustering import ClusterEngine
from .pipeline.labeller import FeatureLabeller
from .diagram.engine import DiagramEngine

def main():
    parser = argparse.ArgumentParser(description="AI-Assisted UMLRev: Reverse Engineering CLI")
    parser.add_argument("--repo", type=str, required=True, help="Path to repository source folder")
    parser.add_argument("--output", type=str, default="output", help="Output directory for UML diagrams")
    parser.add_argument("--project-name", type=str, default="UMLRevProject", help="Project name")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
    out_path = os.path.abspath(args.output)
    os.makedirs(out_path, exist_ok=True)

    print("=" * 70)
    print("  AI-Assisted UMLRev: Continuous Reverse Engineering Engine")
    print("  Authors: Jay Gandhi (B124) & Aditya Rane (B129)")
    print("=" * 70)
    print(f"[*] Scanning Repository: {repo_path}")

    # 1. Symbol Extraction
    extractor = SymbolExtractor()
    project = extractor.scan_directory(repo_path, project_name=args.project_name)
    print(f"[+] Discovered {len(project.source_files)} source files, {len(project.classes)} classes, {len(project.relationships)} relationships.")

    # 2. Semantic Clustering
    print("[*] Running ClusterEngine for cohesive feature discovery...")
    cluster_engine = ClusterEngine()
    clusters = cluster_engine.cluster(list(project.classes.values()), project.relationships)
    print(f"[+] Formed {len(clusters)} candidate feature clusters.")

    # 3. AI Feature Labeling
    print("[*] Querying AI FeatureLabeller for business feature synthesis...")
    labeller = FeatureLabeller()
    for c in clusters:
        feature = labeller.label(c, project.classes)
        project.features.append(feature)
        print(f"  -> Feature Identified: '{feature.name}' (Confidence: {feature.confidence*100:.1f}%) | Classes: {feature.class_names}")

    # 4. Diagram Generation
    print("[*] Synthesizing feature-specific UML Class and Sequence Diagrams...")
    diagram_engine = DiagramEngine()
    diagrams = diagram_engine.generate_for_project(project)
    print(f"[+] Generated {len(diagrams)} UML diagrams.")

    # 5. Export Files
    for d in diagrams:
        safe_name = d.feature_name.lower().replace(" ", "_")
        kind_str = d.kind.value.lower()
        puml_file = os.path.join(out_path, f"{safe_name}_{kind_str}.puml")
        with open(puml_file, "w", encoding="utf-8") as f:
            f.write(d.uml_text)
        print(f"  [Artifact] Saved PlantUML: {puml_file}")

    summary_file = os.path.join(out_path, "project_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(project.to_summary_dict(), f, indent=2)
    print(f"[+] Saved project metadata: {summary_file}")
    print("=" * 70)
    print("Reverse engineering pipeline completed successfully!")

if __name__ == "__main__":
    main()
