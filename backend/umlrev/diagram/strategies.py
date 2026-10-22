import re
from abc import ABC, abstractmethod
from typing import List, Set, Optional, Dict
from ..model.feature import Feature
from ..model.project import Project
from ..model.diagram import Diagram, DiagramKind
from ..model.symbol import ClassSymbol, Relationship

def sanitize_ident(name: str) -> str:
    """Sanitizes names into valid identifiers for PlantUML and Mermaid."""
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '_', name.strip())
    if cleaned and cleaned[0].isdigit():
        cleaned = f"_{cleaned}"
    return cleaned or "Symbol"

# Identifiers Mermaid's sequence grammar claims as keywords. A participant id that
# collides with one of these is lexed as the keyword and the whole diagram fails to
# parse, so such ids are prefixed while the displayed label keeps the original name.
MERMAID_SEQ_RESERVED = {
    "activate", "actor", "alt", "and", "autonumber", "box", "break", "create",
    "critical", "deactivate", "destroy", "details", "else", "end", "link", "links",
    "loop", "note", "opt", "par", "participant", "properties", "rect",
    "sequencediagram", "title", "over",
}

# A feature cluster can hold enough classes that the cross-product of their call
# sites yields a diagram no renderer survives (observed: 201k lines from one
# 145-class cluster), so interactions are de-duplicated and both axes capped.
MAX_SEQUENCE_PARTICIPANTS = 20
MAX_SEQUENCE_MESSAGES = 60

def sanitize_mermaid_actor(name: str) -> str:
    """Returns a participant id that Mermaid will not mistake for a grammar keyword."""
    ident = sanitize_ident(name)
    return f"p_{ident}" if ident.lower() in MERMAID_SEQ_RESERVED else ident

def sanitize_mermaid_type(type_name: str) -> str:
    """Converts complex types to valid Mermaid syntax (e.g. List<T> -> List~T~)."""
    if not type_name:
        return "Any"
    t = type_name.strip()
    # Replace generics < > with ~ ~ for Mermaid
    t = t.replace("<", "~").replace(">", "~")
    # Remove unsupported characters
    t = re.sub(r'[^a-zA-Z0-9_~]', '', t)
    return t or "Any"

class DiagramStrategy(ABC):
    """Abstract Strategy interface for diagram generation (Strategy Pattern)."""

    @abstractmethod
    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> Diagram:
        pass

class ClassDiagramStrategy(DiagramStrategy):
    """Synthesizes structural UML Class Diagrams in PlantUML and Mermaid formats."""

    def generate(self, feature: Feature, project: Project, modified_classes: Optional[Set[str]] = None) -> Diagram:
        feature_classes: Set[str] = set(feature.class_names)
        relevant_symbols = [project.classes[c] for c in feature.class_names if c in project.classes]
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
            safe_id = sanitize_ident(sym.name)
            kind_str = "interface" if sym.is_interface else "class"
            mod_tag = " <<Modified>>" if sym.name in mods else ""
            if safe_id != sym.name:
                lines.append(f'{kind_str} "{sym.name}" as {safe_id}{mod_tag} {{')
            else:
                lines.append(f"{kind_str} {safe_id}{mod_tag} {{")

            for f in sym.fields[:10]:
                vis_sym = "-" if f.visibility == "private" else ("#" if f.visibility == "protected" else "+")
                clean_fname = sanitize_ident(f.name)
                lines.append(f"  {vis_sym} {clean_fname}: {f.type_name}")

            for m in sym.methods[:12]:
                vis_sym = "-" if m.visibility == "private" else ("#" if m.visibility == "protected" else "+")
                clean_mname = sanitize_ident(m.name)
                clean_params = ", ".join([sanitize_ident(p) for p in m.parameters[:4]])
                lines.append(f"  {vis_sym} {clean_mname}({clean_params}): {m.return_type}")

            lines.append("}")

        # Add relationships
        for rel in project.relationships:
            if rel.source_class in feature_classes and rel.target_class in feature_classes:
                src_id = sanitize_ident(rel.source_class)
                tgt_id = sanitize_ident(rel.target_class)
                if rel.rel_type == "inheritance":
                    lines.append(f"{tgt_id} <|-- {src_id}")
                elif rel.rel_type == "realization":
                    lines.append(f"{tgt_id} <|.. {src_id}")
                elif rel.rel_type == "association":
                    label_str = f" : {sanitize_ident(rel.label)}" if rel.label else ""
                    lines.append(f"{src_id} --> {tgt_id}{label_str}")
                elif rel.rel_type == "dependency":
                    label_str = f" : <<use>>" if not rel.label else f" : {sanitize_ident(rel.label)}"
                    lines.append(f"{src_id} ..> {tgt_id}{label_str}")

        lines.append("@enduml")
        plantuml_text = "\n".join(lines)

        # 2. Generate Mermaid Class Diagram
        m_lines = ["classDiagram", f"    %% Feature: {feature.name}"]
        if not relevant_symbols:
            safe_name = sanitize_ident(feature.name) or "CoreModule"
            m_lines.append(f"    class {safe_name} {{")
            m_lines.append("        +execute() void")
            m_lines.append("    }")
        else:
            for sym in relevant_symbols:
                safe_id = sanitize_ident(sym.name)
                m_lines.append(f"    class {safe_id} {{")
                for f in sym.fields[:8]:
                    c_type = sanitize_mermaid_type(f.type_name)
                    c_name = sanitize_ident(f.name)
                    m_lines.append(f"        +{c_type} {c_name}")
                for m in sym.methods[:8]:
                    c_ret = sanitize_mermaid_type(m.return_type)
                    c_name = sanitize_ident(m.name)
                    m_lines.append(f"        +{c_name}() {c_ret}")
                m_lines.append("    }")

        for rel in project.relationships:
            if rel.source_class in feature_classes and rel.target_class in feature_classes:
                src_id = sanitize_ident(rel.source_class)
                tgt_id = sanitize_ident(rel.target_class)
                if rel.rel_type == "inheritance":
                    m_lines.append(f"    {tgt_id} <|-- {src_id}")
                elif rel.rel_type == "realization":
                    m_lines.append(f"    {tgt_id} <|.. {src_id}")
                elif rel.rel_type in ("association", "dependency"):
                    m_lines.append(f"    {src_id} --> {tgt_id}")

        if mods:
            m_lines.append("    classDef modified fill:#064e3b,stroke:#10b981,stroke-width:2px,color:#fff;")
            for m_cls in mods:
                if m_cls in feature_classes:
                    m_lines.append(f'    cssClass "{sanitize_ident(m_cls)}" modified')

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
        relevant_symbols = [project.classes[c] for c in feature.class_names if c in project.classes]
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
                                    "method": sanitize_ident(target_method),
                                    "caller_method": sanitize_ident(method.name)
                                })

        # Heuristic fallback if no explicit calls detected
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
                    "method": sanitize_ident(m_name),
                    "caller_method": "handle"
                })
        elif not messages and len(relevant_symbols) == 1:
            # Single class self-activation
            s_name = relevant_symbols[0].name
            m_name = relevant_symbols[0].methods[0].name if relevant_symbols[0].methods else "process"
            messages.append({
                "sender": s_name,
                "receiver": s_name,
                "method": sanitize_ident(m_name),
                "caller_method": "init"
            })

        # Collapse repeated call sites: the same sender/receiver/method pair adds no
        # behavioural information, and that repetition is what drives the blow-up.
        seen = set()
        unique_messages = []
        for msg in messages:
            key = (msg["sender"], msg["receiver"], msg["method"])
            if key not in seen:
                seen.add(key)
                unique_messages.append(msg)

        truncated = len(unique_messages) > MAX_SEQUENCE_MESSAGES
        messages = unique_messages[:MAX_SEQUENCE_MESSAGES]

        # Draw lifelines only for classes the retained messages actually involve.
        participants = []
        for msg in messages:
            for role in (msg["sender"], msg["receiver"]):
                if role not in participants:
                    participants.append(role)
        if not participants:
            participants = list(feature.class_names)
        if len(participants) > MAX_SEQUENCE_PARTICIPANTS:
            participants = participants[:MAX_SEQUENCE_PARTICIPANTS]
            truncated = True
        kept = set(participants)
        messages = [m for m in messages if m["sender"] in kept and m["receiver"] in kept]

        # 1. Generate PlantUML Sequence Diagram
        p_lines = [
            f"@startuml",
            f"title Feature: {feature.name} - Sequence Diagram",
            f"autonumber"
        ]
        for c in participants:
            c_id = sanitize_ident(c)
            color_tag = " #E8F5E9" if c in mods else ""
            if c_id != c:
                p_lines.append(f'participant "{c}" as {c_id}{color_tag}')
            else:
                p_lines.append(f"participant {c_id}{color_tag}")

        if not messages:
            p_lines.append("participant System")
            p_lines.append("System -> System: execute()")
            p_lines.append("activate System")
            p_lines.append("System --> System: completed")
            p_lines.append("deactivate System")
        else:
            for msg in messages:
                s_id = sanitize_ident(msg['sender'])
                r_id = sanitize_ident(msg['receiver'])
                p_lines.append(f"{s_id} -> {r_id}: {msg['method']}()")
                p_lines.append(f"activate {r_id}")
                p_lines.append(f"{r_id} --> {s_id}: return")
                p_lines.append(f"deactivate {r_id}")

        if truncated and participants:
            p_lines.append(f"note over {sanitize_ident(participants[0])}: View truncated to the {len(messages)} most representative interactions")
        p_lines.append("@enduml")
        plantuml_text = "\n".join(p_lines)

        # 2. Generate Mermaid Sequence Diagram
        m_lines = ["sequenceDiagram", f"    %% Feature: {feature.name}"]
        for c in participants:
            c_id = sanitize_mermaid_actor(c)
            m_lines.append(f'    participant {c_id} as "{c}"')

        if not messages:
            if not feature.class_names:
                m_lines.append('    participant System as "System"')
            m_lines.append("    System->>+System: execute()")
            m_lines.append("    System-->>-System: result")
        else:
            for msg in messages:
                s_id = sanitize_mermaid_actor(msg['sender'])
                r_id = sanitize_mermaid_actor(msg['receiver'])
                m_lines.append(f"    {s_id}->>+{r_id}: {msg['method']}()")
                m_lines.append(f"    {r_id}-->>-{s_id}: result")
        if truncated:
            m_lines.append(f"    %% View truncated to the {len(messages)} most representative interactions")

        mermaid_text = "\n".join(m_lines)

        return Diagram(
            kind=DiagramKind.SEQUENCE,
            feature_name=feature.name,
            uml_text=plantuml_text,
            svg_content=mermaid_text
        )
