from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class FeatureMembership:
    class_name: str
    score: float = 1.0  # Confidence score between 0.0 and 1.0
    primary: bool = True

    def is_primary(self) -> bool:
        return self.primary

@dataclass
class Feature:
    name: str
    description: str = ""
    confidence: float = 0.95
    memberships: List[FeatureMembership] = field(default_factory=list)

    def member_count(self) -> int:
        return len(self.memberships)

    @property
    def class_names(self) -> List[str]:
        return [m.class_name for m in self.memberships]

    def add_class(self, class_name: str, score: float = 1.0, primary: bool = True):
        self.memberships.append(FeatureMembership(class_name=class_name, score=score, primary=primary))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "confidence": round(self.confidence, 3),
            "member_count": self.member_count(),
            "classes": [
                {
                    "class_name": m.class_name,
                    "score": round(m.score, 3),
                    "is_primary": m.primary
                }
                for m in self.memberships
            ]
        }
