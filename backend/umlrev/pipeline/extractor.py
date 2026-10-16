import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from ..model.symbol import ClassSymbol, MethodSymbol, FieldSymbol, Relationship
from ..model.project import Project, SourceFile

class SymbolExtractor:
    """
    Multi-language AST and static symbol extractor.
    Parses Java, Python, and TypeScript/JavaScript source files to extract
    classes, methods, fields, imports, and relationships.
    """

    def __init__(self):
        # Regex patterns for Java parsing
        self.java_package_regex = re.compile(r"^\s*package\s+([\w\.]+)\s*;", re.MULTILINE)
        self.java_import_regex = re.compile(r"^\s*import\s+([\w\.\*]+)\s*;", re.MULTILINE)
        self.java_class_regex = re.compile(
            r"(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+|static\s+)*"
            r"(class|interface|enum)\s+(\w+)"
            r"(?:\s+extends\s+([\w\.]+))?"
            r"(?:\s+implements\s+([\w\.\s,]+))?",
            re.MULTILINE
        )
        self.java_method_regex = re.compile(
            r"(public|protected|private)\s+"
            r"(?:static\s+|final\s+|synchronized\s+|abstract\s+)*"
            r"([\w\<\>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+[\w\s,]+)?\s*\{",
            re.MULTILINE
        )
        self.java_field_regex = re.compile(
            r"^\s*(public|protected|private)\s+"
            r"(?:static\s+|final\s+)*"
            r"([\w\<\>\[\]]+)\s+(\w+)\s*(?:=\s*[^;]+)?\s*;",
            re.MULTILINE
        )
        self.java_call_regex = re.compile(r"(\w+)\.(\w+)\s*\(")

    def scan_directory(self, folder_path: str, project_name: str = "Project") -> Project:
        """Recursively scans a directory and extracts all class symbols."""
        project = Project(name=project_name, folder_path=folder_path)
        valid_exts = {".java", ".py", ".ts", ".js"}

        for root, _, files in os.walk(folder_path):
            # Skip build and hidden directories
            if any(part.startswith(".") or part in {"node_modules", "target", "build", "__pycache__", "dist"} for part in Path(root).parts):
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in valid_exts:
                    full_path = os.path.join(root, file)
                    sf = project.add_source_file(full_path)
                    content = sf.read_content()
                    symbols = self.extract_from_file(full_path, content, ext)
                    for sym in symbols:
                        project.add_class(sym)

        # Derive relationships across extracted classes
        project.relationships = self.resolve_relationships(project.classes)
        return project

    def extract_from_file(self, file_path: str, content: str, ext: str) -> List[ClassSymbol]:
        if ext == ".java":
            return self._extract_java(file_path, content)
        elif ext == ".py":
            return self._extract_python(file_path, content)
        elif ext in {".ts", ".js"}:
            return self._extract_js_ts(file_path, content)
        return []

    def _extract_java(self, file_path: str, content: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        pkg_match = self.java_package_regex.search(content)
        pkg_name = pkg_match.group(1) if pkg_match else ""
        imports = self.java_import_regex.findall(content)

        for match in self.java_class_regex.finditer(content):
            kind, name, extends_cls, implements_str = match.groups()
            sym = ClassSymbol(
                name=name,
                package_name=pkg_name,
                is_interface=(kind == "interface"),
                file_path=file_path,
                imports=imports
            )
            if extends_cls:
                sym.super_classes.append(extends_cls.strip())
            if implements_str:
                sym.interfaces.extend([i.strip() for i in implements_str.split(",") if i.strip()])

            # Extract fields
            for f_match in self.java_field_regex.finditer(content):
                vis, f_type, f_name = f_match.groups()
                sym.fields.append(FieldSymbol(name=f_name, type_name=f_type, visibility=vis))

            # Extract methods and method calls
            for m_match in self.java_method_regex.finditer(content):
                vis, ret_type, m_name, params = m_match.groups()
                param_list = [p.strip() for p in params.split(",") if p.strip()]
                # Extract calls inside this method roughly
                method_sym = MethodSymbol(
                    name=m_name,
                    return_type=ret_type,
                    parameters=param_list,
                    visibility=vis
                )
                sym.methods.append(method_sym)

            # Extract calls throughout class
            for c_match in self.java_call_regex.finditer(content):
                receiver, called_method = c_match.groups()
                if receiver != "this" and receiver != "System":
                    for m in sym.methods:
                        m.called_methods.append(f"{receiver}.{called_method}")

            symbols.append(sym)

        # Fallback if no explicit class keyword was found (e.g. simple record or single class)
        if not symbols and file_path.endswith(".java"):
            base_name = Path(file_path).stem
            symbols.append(ClassSymbol(name=base_name, package_name=pkg_name, file_path=file_path, imports=imports))

        return symbols

    def _extract_python(self, file_path: str, content: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        try:
            tree = ast.parse(content, filename=file_path)
        except Exception:
            base_name = Path(file_path).stem
            return [ClassSymbol(name=base_name, file_path=file_path)]

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node) or ""
                bases = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        bases.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        bases.append(f"{getattr(base.value, 'id', '')}.{base.attr}")

                sym = ClassSymbol(
                    name=node.name,
                    super_classes=bases,
                    file_path=file_path,
                    imports=imports,
                    docstring=docstring
                )

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        params = [arg.arg for arg in item.args.args if arg.arg != "self"]
                        ret_type = "Any"
                        if item.returns and isinstance(item.returns, ast.Name):
                            ret_type = item.returns.id

                        called = []
                        for call_node in ast.walk(item):
                            if isinstance(call_node, ast.Call):
                                if isinstance(call_node.func, ast.Attribute) and isinstance(call_node.func.value, ast.Name):
                                    called.append(f"{call_node.func.value.id}.{call_node.func.attr}")
                                elif isinstance(call_node.func, ast.Name):
                                    called.append(call_node.func.id)

                        vis = "private" if item.name.startswith("__") else ("protected" if item.name.startswith("_") else "public")
                        sym.methods.append(MethodSymbol(
                            name=item.name,
                            return_type=ret_type,
                            parameters=params,
                            visibility=vis,
                            called_methods=called
                        ))
                    elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        f_type = item.annotation.id if isinstance(item.annotation, ast.Name) else "Any"
                        sym.fields.append(FieldSymbol(name=item.target.id, type_name=f_type))

                symbols.append(sym)

        if not symbols:
            # Module-level symbol
            symbols.append(ClassSymbol(name=Path(file_path).stem, file_path=file_path, imports=imports))

        return symbols

    def _extract_js_ts(self, file_path: str, content: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        base_name = Path(file_path).stem
        imports = re.findall(r"import\s+.*?from\s+['\"](.*?)['\"]", content)
        class_regex = re.compile(r"class\s+(\w+)(?:\s+extends\s+(\w+))?")

        for match in class_regex.finditer(content):
            c_name, extends_cls = match.groups()
            sym = ClassSymbol(name=c_name, file_path=file_path, imports=imports)
            if extends_cls:
                sym.super_classes.append(extends_cls)
            symbols.append(sym)

        if not symbols:
            symbols.append(ClassSymbol(name=base_name, file_path=file_path, imports=imports))
        return symbols

    def resolve_relationships(self, classes: Dict[str, ClassSymbol]) -> List[Relationship]:
        relationships: List[Relationship] = []
        known_class_names = set(classes.keys())

        for name, sym in classes.items():
            # Inheritance
            for parent in sym.super_classes:
                if parent in known_class_names:
                    relationships.append(Relationship(source_class=name, target_class=parent, rel_type="inheritance"))

            # Realization / Interface
            for iface in sym.interfaces:
                if iface in known_class_names:
                    relationships.append(Relationship(source_class=name, target_class=iface, rel_type="realization"))

            # Field Association / Aggregation
            for field in sym.fields:
                clean_type = field.type_name.strip("<>[]")
                if clean_type in known_class_names and clean_type != name:
                    relationships.append(Relationship(
                        source_class=name,
                        target_class=clean_type,
                        rel_type="association",
                        label=field.name
                    ))

            # Method Call Dependency
            for method in sym.methods:
                for call in method.called_methods:
                    if "." in call:
                        receiver, _ = call.split(".", 1)
                        # Check if receiver matches a known class
                        for target in known_class_names:
                            if receiver.lower() == target.lower() and target != name:
                                relationships.append(Relationship(
                                    source_class=name,
                                    target_class=target,
                                    rel_type="dependency",
                                    label=method.name
                                ))

        return relationships
