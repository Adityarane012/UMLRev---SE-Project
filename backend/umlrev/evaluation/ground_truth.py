from typing import Dict, List

class GroundTruth:
    """Represents architectural ground-truth feature mappings for benchmarking."""

    def __init__(self, repo_name: str, feature_mapping: Dict[str, List[str]] = None):
        self.repo_name = repo_name
        self.mapping: Dict[str, List[str]] = feature_mapping or {}

    def add_feature(self, feature_name: str, classes: List[str]):
        self.mapping[feature_name] = classes

    def classes_for(self, feature_name: str) -> List[str]:
        return self.mapping.get(feature_name, [])

    def get_features(self) -> List[str]:
        return list(self.mapping.keys())
