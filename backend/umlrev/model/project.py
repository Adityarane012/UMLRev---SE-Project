from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from .symbol import ClassSymbol, Relationship
from .feature import Feature
from .diagram import Diagram

@dataclass
class SourceFile:
    path: str
    content: str = ""

    def read_content(self) -> str:
        if not self.content and Path(self.path).exists():
            with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
                self.content = f.read()
        return self.content

@dataclass
class Project:
    name: str
    folder_path: str
    source_files: List[SourceFile] = field(default_factory=list)
    classes: Dict[str, ClassSymbol] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)
    features: List[Feature] = field(default_factory=list)
    diagrams: List[Diagram] = field(default_factory=list)

    def add_source_file(self, file_path: str, content: str = "") -> SourceFile:
        sf = SourceFile(path=file_path, content=content)
        self.source_files.append(sf)
        return sf

    def add_class(self, symbol: ClassSymbol):
        self.classes[symbol.name] = symbol

    def get_class(self, name: str) -> Optional[ClassSymbol]:
        return self.classes.get(name)

    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "folder_path": self.folder_path,
            "file_count": len(self.source_files),
            "class_count": len(self.classes),
            "feature_count": len(self.features),
            "features": [f.to_dict() for f in self.features],
            "diagrams": [d.to_dict() for d in self.diagrams]
        }
