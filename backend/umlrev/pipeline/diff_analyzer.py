import json
import re
from typing import Dict, List, Any
from .llm_client import LLMClient
from ..model.symbol import ClassSymbol
from ..model.feature import Feature

class DiffAnalyzer:
    """
    Analyzes Git diffs and commit changes to identify:
    1. Which classes are directly impacted or modified.
    2. Which feature or architectural capability is affected.
    3. Structural additions/modifications for focused UML diagramming.
    """

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    def analyze_diff(
        self,
        diff_text: str,
        changed_files: List[str],
        commit_message: str,
        classes: Dict[str, ClassSymbol]
    ) -> Dict[str, Any]:
        # Map changed files to ClassSymbol names
        impacted_classes = []
        for file_path in changed_files:
            file_base = file_path.replace("\\", "/").split("/")[-1].split(".")[0]
            for c_name in classes.keys():
                if c_name.lower() == file_base.lower() or file_path.endswith(f"{c_name}.java") or file_path.endswith(f"{c_name}.py"):
                    impacted_classes.append(c_name)

        impacted_classes = list(set(impacted_classes))

        # If no specific classes matched from filenames, fall back to symbols found in diff text
        if not impacted_classes:
            for c_name in classes.keys():
                if re.search(rf"\b{c_name}\b", diff_text):
                    impacted_classes.append(c_name)
            impacted_classes = list(set(impacted_classes))

        # If still none, default to all classes in project (e.g. initial commit)
        if not impacted_classes:
            impacted_classes = list(classes.keys())

        # Query LLM to identify the feature and nature of changes
        prompt = f"""
You are an expert Software Architect reviewing a GitHub commit / diff to identify the software feature being changed or introduced.

Commit Message: {commit_message or 'Latest modifications'}
Changed Files: {', '.join(changed_files)}
Impacted Classes: {', '.join(impacted_classes)}

Git Diff Snippet:
{diff_text[:3000]}

Respond strictly in valid JSON format:
{{
  "feature_name": "Concise feature name representing this change (e.g., 'Combat & Rescue Mechanism', 'User Auth Flow')",
  "change_type": "FEATURE_UPDATE" or "NEW_FEATURE" or "REFACTOR",
  "description": "2-3 sentences explaining what functionality was changed or added in this commit.",
  "confidence": 0.95
}}
"""
        raw_res = self.llm.ask(prompt)
        feature_name = "Modified Feature"
        change_type = "FEATURE_UPDATE"
        description = f"Updates affecting {', '.join(impacted_classes)}."
        confidence = 0.92

        try:
            match = re.search(r"\{.*?\}", raw_res, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                feature_name = data.get("feature_name", feature_name)
                change_type = data.get("change_type", change_type)
                description = data.get("description", description)
                confidence = float(data.get("confidence", confidence))
        except Exception:
            pass

        return {
            "feature_name": feature_name,
            "change_type": change_type,
            "description": description,
            "confidence": confidence,
            "impacted_classes": impacted_classes,
            "changed_files": changed_files,
            "commit_message": commit_message
        }
