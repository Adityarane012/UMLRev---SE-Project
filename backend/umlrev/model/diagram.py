from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

class DiagramKind(str, Enum):
    CLASS = "CLASS"
    SEQUENCE = "SEQUENCE"

@dataclass
class Diagram:
    kind: DiagramKind
    feature_name: str
    uml_text: str  # PlantUML markup
    svg_content: str = ""  # Rendered SVG or Mermaid representation

    def export(self) -> str:
        return self.uml_text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "kind": self.kind.value,
            "feature_name": self.feature_name,
            "uml_text": self.uml_text,
            "svg_content": self.svg_content
        }
