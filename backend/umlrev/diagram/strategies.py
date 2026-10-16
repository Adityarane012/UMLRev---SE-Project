from abc import ABC, abstractmethod
from typing import List, Set, Optional
from ..model.feature import Feature
from ..model.project import Project
from ..model.diagram import Diagram, DiagramKind
from ..model.symbol import ClassSymbol, Relationship

class DiagramStrategy(ABC):
    """Abstract Strategy interface for diagram generation (Strategy Pattern)."""

    @abstractmethod
    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> Diagram:
        pass

class ClassDiagramStrategy(DiagramStrategy):
    """Synthesizes structural UML Class Diagrams in PlantUML and Mermaid formats."""

    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> Diagram:
        feature_classes: Set[str] = set(feature.class_names)
        relevant_symbols = [project.classes[c] for c in feature_classes if c in project.classes]
        mods = modified_classes or set()

        # 1. Generate PlantUML
        lines = [
            f"@startuml",
            f"title Feature: {feature.name} - Class Diagram",
            f"skinparam classAttributeIconSize 0",
            f"skinparam roundcorner 5",
            f"skinparam packageStyle rectangle"
        ]

        if mods:
            lines.append("skinparam class<<Modified>> {")
            lines.append("  BackgroundColor #E8F5E9")
            lines.append("  BorderColor #2E7D32")
            lines.append("}")

        for sym in relevant_symbols:
            kind_str = "interface" if sym.is_interface else "class"
            mod_tag = " <<Modified>>" if sym.name in mods else ""
            lines.append(f"{kind_str} {sym.name}{mod_tag} {{")
            for f in sym.fields[:10]:
                vis_sym = "-" if f.visibility == "private" else ("#" if f.visibility == "protected" else "+")
                lines.append(f"  {vis_sym} {f.name}: {f.type_name}")
            for m in sym.methods[:12]:
                vis_sym = "-" if m.visibility == "private" else ("#" if m.visibility == "protected" else "+")
                param_str = ", ".join(m.parameters[:4])
                lines.append(f"  {vis_sym} {m.name}({param_str}): {m.return_type}")
            lines.append("}")

        # Add relationships involving feature classes
        for rel in project.relationships:
            if rel.source_class in feature_classes and rel.target_class in feature_classes:
                if rel.rel_type == "inheritance":
                    lines.append(f"{rel.target_class} <|-- {rel.source_class}")
                elif rel.rel_type == "realization":
                    lines.append(f"{rel.target_class} <|.. {rel.source_class}")
                elif rel.rel_type == "association":
                    label_str = f" : {rel.label}" if rel.label else ""
                    lines.append(f"{rel.source_class} --> {rel.target_class}{label_str}")
                elif rel.rel_type == "dependency":
                    label_str = f" : <<use>>" if not rel.label else f" : {rel.label}"
                    lines.append(f"{rel.source_class} ..> {rel.target_class}{label_str}")

        lines.append("@enduml")
        plantuml_text = "\n".join(lines)

        # 2. Generate Mermaid Class Diagram for web rendering / copy-paste
        m_lines = ["classDiagram", f"    %% Feature: {feature.name}"]
        for sym in relevant_symbols:
            m_lines.append(f"    class {sym.name} {{")
            for f in sym.fields[:6]:
                m_lines.append(f"        +{f.type_name} {f.name}")
            for m in sym.methods[:6]:
                m_lines.append(f"        +{m.name}() {m.return_type}")
            m_lines.append("    }")

        for rel in project.relationships:
            if rel.source_class in feature_classes and rel.target_class in feature_classes:
                if rel.rel_type == "inheritance":
                    m_lines.append(f"    {rel.target_class} <|-- {rel.source_class}")
                elif rel.rel_type == "realization":
                    m_lines.append(f"    {rel.target_class} <|.. {rel.source_class}")
                elif rel.rel_type in ("association", "dependency"):
                    m_lines.append(f"    {rel.source_class} --> {rel.target_class}")

        if mods:
            m_lines.append("    classDef modified fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff;")
            for m_cls in mods:
                if m_cls in feature_classes:
                    m_lines.append(f"    class {m_cls} modified;")

        mermaid_text = "\n".join(m_lines)

        return Diagram(
            kind=DiagramKind.CLASS,
            feature_name=feature.name,
            uml_text=plantuml_text,
            svg_content=mermaid_text
        )

class SequenceDiagramStrategy(DiagramStrategy):
    """Synthesizes dynamic behavioral UML Sequence Diagrams in PlantUML and Mermaid formats."""

    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> Diagram:
        feature_classes = set(feature.class_names)
        relevant_symbols = [project.classes[c] for c in feature_classes if c in project.classes]
        mods = modified_classes or set()

        # Extract message sequences from method call interactions
        messages = []
        for sym in relevant_symbols:
            for method in sym.methods:
                for call in method.called_methods:
                    if "." in call:
                        target_class, target_method = call.split(".", 1)
                        for fc in feature_classes:
                            if target_class.lower() == fc.lower() and fc != sym.name:
                                messages.append({
                                    "sender": sym.name,
                                    "receiver": fc,
                                    "method": target_method,
                                    "caller_method": method.name
                                })

        if not messages and len(relevant_symbols) >= 2:
            names = [s.name for s in relevant_symbols]
            for i in range(len(names) - 1):
                src = names[i]
                tgt = names[i+1]
                target_sym = project.classes.get(tgt)
                m_name = target_sym.methods[0].name if (target_sym and target_sym.methods) else "execute"
                messages.append({
                    "sender": src,
                    "receiver": tgt,
                    "method": m_name,
                    "caller_method": "handle"
                })

        # 1. Generate PlantUML Sequence Diagram
        p_lines = [
            f"@startuml",
            f"title Feature: {feature.name} - Sequence Diagram",
            f"autonumber"
        ]
        for c in feature.class_names:
            color_tag = " #E8F5E9" if c in mods else ""
            p_lines.append(f"participant {c}{color_tag}")

        for msg in messages:
            p_lines.append(f"{msg['sender']} -> {msg['receiver']}: {msg['method']}()")
            p_lines.append(f"activate {msg['receiver']}")
            p_lines.append(f"{msg['receiver']} --> {msg['sender']}: return")
            p_lines.append(f"deactivate {msg['receiver']}")

        p_lines.append("@enduml")
        plantuml_text = "\n".join(p_lines)

        # 2. Generate Mermaid Sequence Diagram
        m_lines = ["sequenceDiagram", f"    %% Feature: {feature.name}"]
        for c in feature.class_names:
            m_lines.append(f"    participant {c}")

        for msg in messages:
            m_lines.append(f"    {msg['sender']}->>+{msg['receiver']}: {msg['method']}()")
            m_lines.append(f"    {msg['receiver']}-->>-{msg['sender']}: result")

        mermaid_text = "\n".join(m_lines)

        return Diagram(
            kind=DiagramKind.SEQUENCE,
            feature_name=feature.name,
            uml_text=plantuml_text,
            svg_content=mermaid_text
        )
