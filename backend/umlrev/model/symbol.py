from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FieldSymbol:
    name: str
    type_name: str
    visibility: str = "private"  # public, private, protected

@dataclass
class MethodSymbol:
    name: str
    return_type: str = "void"
    parameters: List[str] = field(default_factory=list)
    visibility: str = "public"
    called_methods: List[str] = field(default_factory=list)  # Callee names (e.g. TargetClass.methodName)

@dataclass
class Relationship:
    source_class: str
    target_class: str
    rel_type: str  # association, inheritance, dependency, aggregation, composition
    label: str = ""

@dataclass
class ClassSymbol:
    name: str
    package_name: str = ""
    is_interface: bool = False
    super_classes: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    fields: List[FieldSymbol] = field(default_factory=list)
    methods: List[MethodSymbol] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    file_path: str = ""
    docstring: str = ""

    def get_imports(self) -> List[str]:
        return self.imports

    @property
    def qualified_name(self) -> str:
        return f"{self.package_name}.{self.name}" if self.package_name else self.name
