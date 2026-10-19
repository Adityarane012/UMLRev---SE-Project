import json
import re
import concurrent.futures
from typing import Dict, List, Optional
from .clustering import Cluster
from .llm_client import LLMClient
from ..model.symbol import ClassSymbol
from ..model.feature import Feature, FeatureMembership

class FeatureLabeller:
    """
    Labels candidate Clusters by synthesizing feature context and invoking LLMClient.
    Supports parallel batch execution and resilient JSON extraction.
    """

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or LLMClient()

    def label_all(self, clusters: List[Cluster], class_map: Dict[str, ClassSymbol]) -> List[Feature]:
        """Labels all clusters in parallel for maximum performance and responsiveness."""
        if not clusters:
            return []

        if len(clusters) == 1:
            return [self.label(clusters[0], class_map)]

        features = [None] * len(clusters)
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(clusters), 6)) as executor:
            future_to_idx = {
                executor.submit(self.label, cluster, class_map): idx
                for idx, cluster in enumerate(clusters)
            }
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    features[idx] = future.result()
                except Exception:
                    features[idx] = self._fallback_feature(clusters[idx])

        return [f for f in features if f is not None]

    def _fallback_feature(self, cluster: Cluster) -> Feature:
        names = cluster.class_names()
        primary = names[0] if names else "Core"
        clean = re.sub(r"([A-Z])", r" \1", primary).strip().title()
        feat = Feature(
            name=f"{clean} Management",
            description=f"Encapsulates domain logic and interactions for {', '.join(names[:4])}.",
            confidence=0.88
        )
        for c in names:
            feat.add_class(c, score=0.88, primary=True)
        return feat

    def label(self, cluster: Cluster, class_map: Dict[str, ClassSymbol]) -> Feature:
        member_classes = [class_map[c] for c in cluster.class_names() if c in class_map]

        # Construct concise context prompt
        class_summaries = []
        for c in member_classes[:8]:
            methods = [m.name for m in c.methods[:5]]
            fields = [f"{f.name}: {f.type_name}" for f in c.fields[:5]]
            class_summaries.append(
                f"- Class {c.name} (methods: {methods}, fields: {fields})"
            )

        prompt = f"""You are an expert Software Architect reverse-engineering UML models.
Given this cohesive cluster of classes, deduce the software feature they represent.

Classes: [{', '.join(cluster.class_names()[:12])}]

Class Details:
{chr(10).join(class_summaries)}

Respond strictly in valid JSON format:
{{
  "feature_name": "Clear, concise business feature name",
  "description": "1-2 sentence description of what this feature does.",
  "confidence": 0.95
}}
"""
        raw_response = self.llm.ask(prompt)
        feature_name = f"Feature {cluster.cluster_id + 1}"
        description = f"Encapsulates {', '.join(cluster.class_names())}"
        confidence = 0.90

        try:
            if raw_response:
                # Strip code fences if present
                clean = re.sub(r"^```(?:json)?", "", raw_response.strip(), flags=re.MULTILINE)
                clean = re.sub(r"```$", "", clean.strip(), flags=re.MULTILINE).strip()

                parsed = None
                try:
                    data = json.loads(clean)
                    if isinstance(data, dict):
                        parsed = data
                    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                        parsed = data[0]
                except Exception:
                    pass

                if not parsed:
                    # Regex search for any valid JSON object containing feature_name
                    match = re.search(r"\{[^{}]*\"feature_name\"[^{}]*\}", raw_response, re.DOTALL)
                    if match:
                        parsed = json.loads(match.group(0))

                if parsed:
                    feature_name = parsed.get("feature_name", feature_name).strip()
                    description = parsed.get("description", description).strip()
                    confidence = float(parsed.get("confidence", confidence))
        except Exception:
            pass

        feature = Feature(name=feature_name, description=description, confidence=confidence)
        for c_name in cluster.class_names():
            feature.add_class(class_name=c_name, score=confidence, primary=True)

        return feature

