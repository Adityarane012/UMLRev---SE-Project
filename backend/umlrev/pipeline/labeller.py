import json
import re
from typing import Dict, List
from .clustering import Cluster
from .llm_client import LLMClient
from ..model.symbol import ClassSymbol
from ..model.feature import Feature, FeatureMembership

class FeatureLabeller:
    """
    Labels candidate Clusters by synthesizing feature context and invoking LLMClient.
    """

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    def label(self, cluster: Cluster, class_map: Dict[str, ClassSymbol]) -> Feature:
        member_classes = [class_map[c] for c in cluster.class_names() if c in class_map]

        # Construct context prompt
        class_summaries = []
        for c in member_classes:
            methods = [m.name for m in c.methods[:6]]
            fields = [f"{f.name}: {f.type_name}" for f in c.fields[:6]]
            class_summaries.append(
                f"- Class {c.name} (methods: {methods}, fields: {fields})"
            )

        prompt = f"""
You are an expert Software Architect analyzing a software system to reverse-engineer feature-level UML models.
Given the following cluster of closely collaborating classes, deduce the software feature they represent.

Classes: [{', '.join(cluster.class_names())}]

Class Details:
{chr(10).join(class_summaries)}

Respond strictly in valid JSON format with the following keys:
{{
  "feature_name": "Clear, concise business feature name (e.g., 'Tell Story', 'User Authentication')",
  "description": "1-2 sentence description of what this feature does.",
  "confidence": 0.95
}}
"""
        raw_response = self.llm.ask(prompt)
        feature_name = f"Feature {cluster.cluster_id + 1}"
        description = f"Encapsulates {', '.join(cluster.class_names())}"
        confidence = 0.90

        try:
            # Extract JSON block
            json_match = re.search(r"\{.*?\}", raw_response, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                feature_name = parsed.get("feature_name", feature_name)
                description = parsed.get("description", description)
                confidence = float(parsed.get("confidence", confidence))
        except Exception:
            pass

        feature = Feature(name=feature_name, description=description, confidence=confidence)
        for c_name in cluster.class_names():
            feature.add_class(class_name=c_name, score=confidence, primary=True)

        return feature
