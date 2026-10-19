import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
from ..model.symbol import ClassSymbol, MethodSymbol, FieldSymbol, Relationship
from ..model.project import Project, SourceFile

class SymbolExtractor:
    """
    Multi-language AST and static symbol extractor.
    Parses Python, Java, TypeScript/JavaScript (including JSX/TSX), C#, Go, C/C++, and PHP source files
    to extract classes, interfaces, structs, modules, methods, fields, imports, and relationships.
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

        # Patterns for C#
        self.cs_class_regex = re.compile(
            r"(?:public|protected|private|internal|abstract|sealed|static|\s)*\b(class|interface|struct|record)\s+(\w+)(?:\s*:\s*([\w\s,<>]+))?",
            re.MULTILINE
        )
        self.cs_method_regex = re.compile(
            r"(?:public|protected|private|internal|static|async|\s)*([\w\<\>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{",
            re.MULTILINE
        )

        # Patterns for Go
        self.go_struct_regex = re.compile(r"type\s+(\w+)\s+(struct|interface)\s*\{", re.MULTILINE)
        self.go_method_regex = re.compile(r"func\s*\(\s*\w+\s*\*?(\w+)\s*\)\s*(\w+)\s*\(([^)]*)\)", re.MULTILINE)
        self.go_func_regex = re.compile(r"func\s+(\w+)\s*\(([^)]*)\)", re.MULTILINE)

        # Patterns for C/C++
        self.cpp_class_regex = re.compile(r"(?:class|struct)\s+(\w+)(?:\s*:\s*(?:public|protected|private)\s+([\w:]+))?\s*\{", re.MULTILINE)

    def scan_directory(self, folder_path: str, project_name: str = "Project", max_files: int = 250) -> Project:
        """Recursively scans a directory and extracts all class symbols, with a safety cap for large repos."""
        project = Project(name=project_name, folder_path=folder_path)
        valid_exts = {
            ".java", ".py", ".ts", ".js", ".jsx", ".tsx",
            ".cs", ".go", ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp", ".php", ".rb"
        }
        skip_dirs = {
            ".git", ".github", "node_modules", "target", "build", "__pycache__",
            "dist", ".next", ".nuxt", "venv", ".venv", "env", "bin", "obj",
            "vendor", ".idea", ".vscode", "coverage", ".pytest_cache"
        }
        files_scanned = 0
        cap_reached = False

        for root, dirs, files in os.walk(folder_path):
            if cap_reached:
                break

            # Prune skipped directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]

            rel_dir = os.path.relpath(root, folder_path)
            if rel_dir == "." or not rel_dir:
                default_pkg = ""
            else:
                default_pkg = rel_dir.replace("\\", ".").replace("/", ".")

            for file in files:
                if files_scanned >= max_files:
                    print(f"[*] Reached maximum scan cap of {max_files} files. Synthesizing models from top {files_scanned} architectural files.")
                    cap_reached = True
                    break

                ext = os.path.splitext(file)[1].lower()
                if ext in valid_exts:
                    full_path = os.path.join(root, file)
                    # Ignore huge bundle files or minified code (> 512 KB)
                    try:
                        if os.path.getsize(full_path) > 512 * 1024:
                            continue
                    except OSError:
                        continue

                    sf = project.add_source_file(full_path)
                    content = sf.read_content()
                    symbols = self.extract_from_file(full_path, content, ext, default_pkg=default_pkg)
                    for sym in symbols:
                        project.add_class(sym)
                    files_scanned += 1

        # Derive relationships across extracted classes
        project.relationships = self.resolve_relationships(project.classes)
        return project

    def extract_from_file(self, file_path: str, content: str, ext: str, default_pkg: str = "") -> List[ClassSymbol]:
        if ext == ".java":
            return self._extract_java(file_path, content, default_pkg)
        elif ext == ".py":
            return self._extract_python(file_path, content, default_pkg)
        elif ext in {".ts", ".js", ".jsx", ".tsx"}:
            return self._extract_js_ts(file_path, content, default_pkg)
        elif ext == ".cs":
            return self._extract_csharp(file_path, content, default_pkg)
        elif ext == ".go":
            return self._extract_go(file_path, content, default_pkg)
        elif ext in {".cpp", ".cc", ".cxx", ".c", ".h", ".hpp"}:
            return self._extract_cpp(file_path, content, default_pkg)
        elif ext == ".php":
            return self._extract_php(file_path, content, default_pkg)
        return []

    def _extract_java(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        pkg_match = self.java_package_regex.search(content)
        pkg_name = pkg_match.group(1) if pkg_match else default_pkg
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

        # Fallback if no explicit class keyword was found
        if not symbols and file_path.endswith(".java"):
            base_name = Path(file_path).stem
            symbols.append(ClassSymbol(name=base_name, package_name=pkg_name, file_path=file_path, imports=imports))

        return symbols

    def _extract_python(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        try:
            tree = ast.parse(content, filename=file_path)
        except Exception:
            base_name = Path(file_path).stem
            return [ClassSymbol(name=base_name, package_name=default_pkg, file_path=file_path)]

        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                for alias in getattr(node, "names", []):
                    imports.append(alias.name)

        # Check for top-level classes
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
                    package_name=default_pkg,
                    super_classes=bases,
                    file_path=file_path,
                    imports=imports,
                    docstring=docstring
                )

                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                sym.fields.append(FieldSymbol(name=target.id, type_name="Any"))

                symbols.append(sym)

        # If no classes found, treat the module itself as a structural unit
        if not symbols:
            mod_name = Path(file_path).stem
            # Clean module name for UML
            clean_mod = "".join(part.capitalize() for part in re.split(r"[_\-]", mod_name) if part) or mod_name
            mod_sym = ClassSymbol(
                name=clean_mod,
                package_name=default_pkg,
                file_path=file_path,
                imports=imports
            )
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    params = [arg.arg for arg in node.args.args]
                    ret_type = "Any"
                    if node.returns and isinstance(node.returns, ast.Name):
                        ret_type = node.returns.id
                    vis = "private" if node.name.startswith("_") else "public"
                    called = []
                    for call_node in ast.walk(node):
                        if isinstance(call_node, ast.Call):
                            if isinstance(call_node.func, ast.Attribute) and isinstance(call_node.func.value, ast.Name):
                                called.append(f"{call_node.func.value.id}.{call_node.func.attr}")
                            elif isinstance(call_node.func, ast.Name):
                                called.append(call_node.func.id)

                    mod_sym.methods.append(MethodSymbol(
                        name=node.name,
                        return_type=ret_type,
                        parameters=params,
                        visibility=vis,
                        called_methods=called
                    ))
                elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    f_type = node.annotation.id if isinstance(node.annotation, ast.Name) else "Any"
                    mod_sym.fields.append(FieldSymbol(name=node.target.id, type_name=f_type))
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            mod_sym.fields.append(FieldSymbol(name=target.id, type_name="Any"))

            symbols.append(mod_sym)

        return symbols

    def _extract_js_ts(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        base_name = Path(file_path).stem
        clean_name = "".join(part.capitalize() for part in re.split(r"[_\-\.]", base_name) if part) or base_name
        raw_imports = re.findall(r"import\s+.*?from\s+['\"](.*?)['\"]", content)
        imports = []
        for imp in raw_imports:
            imports.append(imp)
            parts = imp.split("/")
            if parts and parts[-1] != imp:
                imports.append(parts[-1])

        class_regex = re.compile(r"(?:export\s+)?(?:default\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?")
        for match in class_regex.finditer(content):
            c_name, extends_cls, implements_str = match.groups()
            sym = ClassSymbol(name=c_name, package_name=default_pkg, file_path=file_path, imports=imports)
            if extends_cls:
                sym.super_classes.append(extends_cls)
            if implements_str:
                sym.interfaces.extend([i.strip() for i in implements_str.split(",") if i.strip()])

            # Method regex for JS/TS classes
            m_regex = re.compile(r"(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*\{")
            for m in m_regex.finditer(content):
                m_name, params = m.groups()
                if m_name not in {"if", "for", "while", "switch", "catch"}:
                    sym.methods.append(MethodSymbol(name=m_name, parameters=[p.strip() for p in params.split(",") if p.strip()]))

            symbols.append(sym)

        if not symbols:
            # React component or functional module
            mod_sym = ClassSymbol(name=clean_name, package_name=default_pkg, file_path=file_path, imports=imports)
            func_regex = re.compile(r"(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)")
            const_func_regex = re.compile(r"(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>")
            for m in func_regex.finditer(content):
                fn_name, params = m.groups()
                mod_sym.methods.append(MethodSymbol(name=fn_name, parameters=[p.strip() for p in params.split(",") if p.strip()]))
            for m in const_func_regex.finditer(content):
                fn_name, params = m.groups()
                mod_sym.methods.append(MethodSymbol(name=fn_name, parameters=[p.strip() for p in params.split(",") if p.strip()]))
            symbols.append(mod_sym)

        return symbols

    def _extract_csharp(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        ns_match = re.search(r"namespace\s+([\w\.]+)", content)
        pkg_name = ns_match.group(1) if ns_match else default_pkg
        imports = re.findall(r"using\s+([\w\.]+)\s*;", content)

        for match in self.cs_class_regex.finditer(content):
            kind, name, inheritance = match.groups()
            sym = ClassSymbol(
                name=name,
                package_name=pkg_name,
                is_interface=(kind == "interface"),
                file_path=file_path,
                imports=imports
            )
            if inheritance:
                for base in inheritance.split(","):
                    b = base.strip()
                    if b.startswith("I") and len(b) > 1 and b[1].isupper():
                        sym.interfaces.append(b)
                    else:
                        sym.super_classes.append(b)

            for m in self.cs_method_regex.finditer(content):
                ret_type, m_name, params = m.groups()
                if m_name not in {"if", "for", "while", "switch"}:
                    sym.methods.append(MethodSymbol(name=m_name, return_type=ret_type, parameters=[p.strip() for p in params.split(",") if p.strip()]))
            symbols.append(sym)

        if not symbols:
            symbols.append(ClassSymbol(name=Path(file_path).stem, package_name=pkg_name, file_path=file_path, imports=imports))
        return symbols

    def _extract_go(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        pkg_match = re.search(r"package\s+(\w+)", content)
        pkg_name = pkg_match.group(1) if pkg_match else default_pkg
        imports = re.findall(r'"([^"]+)"', content)

        for match in self.go_struct_regex.finditer(content):
            name, kind = match.groups()
            sym = ClassSymbol(name=name, package_name=pkg_name, is_interface=(kind == "interface"), file_path=file_path, imports=imports)
            symbols.append(sym)

        for m in self.go_method_regex.finditer(content):
            receiver, fn_name, params = m.groups()
            target_sym = next((s for s in symbols if s.name == receiver), None)
            if target_sym:
                target_sym.methods.append(MethodSymbol(name=fn_name, parameters=[p.strip() for p in params.split(",") if p.strip()]))

        for m in self.go_func_regex.finditer(content):
            fn_name, params = m.groups()
            if symbols:
                symbols[0].methods.append(MethodSymbol(name=fn_name, parameters=[p.strip() for p in params.split(",") if p.strip()]))

        if not symbols:
            symbols.append(ClassSymbol(name=Path(file_path).stem, package_name=pkg_name, file_path=file_path, imports=imports))
        return symbols

    def _extract_cpp(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        imports = re.findall(r'#include\s*[<"]([^>"]+)[>"]', content)
        for match in self.cpp_class_regex.finditer(content):
            name, parent = match.groups()
            sym = ClassSymbol(name=name, package_name=default_pkg, file_path=file_path, imports=imports)
            if parent:
                sym.super_classes.append(parent.strip())
            symbols.append(sym)

        if not symbols:
            symbols.append(ClassSymbol(name=Path(file_path).stem, package_name=default_pkg, file_path=file_path, imports=imports))
        return symbols

    def _extract_php(self, file_path: str, content: str, default_pkg: str) -> List[ClassSymbol]:
        symbols: List[ClassSymbol] = []
        ns_match = re.search(r"namespace\s+([\w\\]+)\s*;", content)
        pkg_name = ns_match.group(1).replace("\\", ".") if ns_match else default_pkg
        imports = re.findall(r"use\s+([\w\\]+)\s*;", content)

        class_regex = re.compile(r"(?:abstract\s+|final\s+)?(class|interface|trait)\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?")
        for match in class_regex.finditer(content):
            kind, name, extends_cls, implements_str = match.groups()
            sym = ClassSymbol(name=name, package_name=pkg_name, is_interface=(kind == "interface"), file_path=file_path, imports=imports)
            if extends_cls:
                sym.super_classes.append(extends_cls)
            if implements_str:
                sym.interfaces.extend([i.strip() for i in implements_str.split(",") if i.strip()])
            symbols.append(sym)

        if not symbols:
            symbols.append(ClassSymbol(name=Path(file_path).stem, package_name=pkg_name, file_path=file_path, imports=imports))
        return symbols

    def resolve_relationships(self, classes: Dict[str, ClassSymbol]) -> List[Relationship]:
        relationships: List[Relationship] = []
        known_class_names = set(classes.keys())
        known_lower_map = {k.lower(): k for k in known_class_names}
        existing_pairs: Set[Tuple[str, str, str]] = set()

        def add_rel(src: str, tgt: str, rtype: str, lbl: str = ""):
            key = (src, tgt, rtype)
            if key not in existing_pairs and src != tgt:
                existing_pairs.add(key)
                relationships.append(Relationship(source_class=src, target_class=tgt, rel_type=rtype, label=lbl))

        for name, sym in classes.items():
            # Inheritance
            for parent in sym.super_classes:
                p_clean = parent.split(".")[-1]
                if p_clean in known_class_names:
                    add_rel(name, p_clean, "inheritance")

            # Realization / Interface
            for iface in sym.interfaces:
                i_clean = iface.split(".")[-1]
                if i_clean in known_class_names:
                    add_rel(name, i_clean, "realization")

            # Field Association / Aggregation
            for field in sym.fields:
                clean_type = re.sub(r"[^a-zA-Z0-9_]", "", field.type_name)
                if clean_type in known_class_names:
                    add_rel(name, clean_type, "association", field.name)

            # Method Call Dependency
            for method in sym.methods:
                for call in method.called_methods:
                    receiver = call.split(".")[0] if "." in call else call
                    target = known_lower_map.get(receiver.lower())
                    if target and target != name:
                        add_rel(name, target, "dependency", method.name)

            # Import Dependency
            for imp in sym.imports:
                clean_imp = imp.split(".")[-1].split("/")[-1]
                target = known_lower_map.get(clean_imp.lower())
                if target and target != name:
                    add_rel(name, target, "dependency", "uses")

        return relationships
