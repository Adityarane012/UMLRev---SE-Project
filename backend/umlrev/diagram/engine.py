from typing import List, Set, Optional
from .strategies import DiagramStrategy, ClassDiagramStrategy, SequenceDiagramStrategy
from ..model.feature import Feature
from ..model.project import Project
from ..model.diagram import Diagram

class DiagramEngine:
    """
    Central hub orchestrating diagram generation strategies (Strategy Pattern).
    Matches DiagramEngine specified in Exp 5 Class Diagram.
    """

    def __init__(self, strategies: List[DiagramStrategy] = None):
        self.strategies: List[DiagramStrategy] = strategies or [
            ClassDiagramStrategy(),
            SequenceDiagramStrategy()
        ]

    def add_strategy(self, strategy: DiagramStrategy):
        self.strategies.append(strategy)

    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> List[Diagram]:
        diagrams: List[Diagram] = []
        for strat in self.strategies:
            diagram = strat.generate(feature, project, modified_classes=modified_classes)
            diagrams.append(diagram)
        return diagrams

    def generate_for_project(self, project: Project, modified_classes: Optional[Set[str]] = None) -> List[Diagram]:
        all_diagrams: List[Diagram] = []
        for feature in project.features:
            feature_diagrams = self.generate(feature, project, modified_classes=modified_classes)
            all_diagrams.extend(feature_diagrams)
        project.diagrams = all_diagrams
        return all_diagrams
