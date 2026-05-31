"""
documentation.py

Streamlit documentation page for this project.

This module scans all Python files in the same directory, reads module
comments and docstrings, extracts functions and classes using the Abstract 
Syntax Tree (AST), and renders an interactive documentation view. It features
a sidebar menu, a search functionality, and a detailed view of the source code.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import streamlit as st


@dataclass
class CodeNode:
    """
    Represents a single class or function found in a Python file.

    Attributes:
        name: The name of the function or class.
        kind: The type of the node ('class' or 'function').
        line: The starting line number in the source file.
        signature: The reconstructed signature of the function/class.
        docstring: The extracted docstring.
        source_code: The raw source code of the function/class.
        children: Nested functions or classes within this node.
    """
    name: str
    kind: str
    line: int
    signature: str = ""
    docstring: str = ""
    source_code: str = ""
    children: list["CodeNode"] = field(default_factory=list)


@dataclass
class FileDocumentation:
    """
    Stores the extracted documentation and structure for a single Python file.
    """
    file_name: str
    file_path: str
    module_docstring: str | None
    block_comments: list[str]
    imports: list[str]
    structure: list[CodeNode]
    syntax_error: str | None = None


def _get_source_directory() -> Path:
    """Return the absolute path to the directory containing this script."""
    return Path(__file__).resolve().parent


def _read_text(path: Path) -> str:
    """Read a Python file safely with UTF-8 fallback protection."""
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_block_comments(source: str) -> list[str]:
    """
    Extract contiguous groups of '#' comments from the source code.

    Python lacks official block comments, so consecutive lines starting 
    with '#' are grouped together as a single block comment.
    """
    blocks: list[str] = []
    current_block: list[str] = []

    for raw_line in source.splitlines():
        stripped = raw_line.strip()

        if stripped.startswith("#"):
            comment_text = stripped.lstrip("#").strip()
            current_block.append(comment_text)
            continue

        if current_block:
            blocks.append("\n".join(current_block).strip())
            current_block = []

    if current_block:
        blocks.append("\n".join(current_block).strip())

    return [block for block in blocks if block]


def _format_annotation(annotation: ast.AST | None) -> str:
    """Convert an AST annotation node into a readable string."""
    if annotation is None:
        return ""
    try:
        return ast.unparse(annotation)
    except Exception:
        return ""


def _format_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """
    Build a readable function signature from an AST function node.

    This includes positional arguments, keyword arguments, default values,
    and return type annotations.
    """
    args: list[str] = []

    positional_args = list(node.args.posonlyargs) + list(node.args.args)
    defaults_offset = len(positional_args) - len(node.args.defaults)

    for index, arg in enumerate(positional_args):
        text = arg.arg
        annotation = _format_annotation(arg.annotation)
        if annotation:
            text += f": {annotation}"

        if index >= defaults_offset and node.args.defaults:
            default_node = node.args.defaults[index - defaults_offset]
            try:
                text += f" = {ast.unparse(default_node)}"
            except Exception:
                text += " = ..."

        args.append(text)

    if node.args.vararg:
        text = f"*{node.args.vararg.arg}"
        annotation = _format_annotation(node.args.vararg.annotation)
        if annotation:
            text += f": {annotation}"
        args.append(text)

    for index, arg in enumerate(node.args.kwonlyargs):
        text = arg.arg
        annotation = _format_annotation(arg.annotation)
        if annotation:
            text += f": {annotation}"

        default_node = node.args.kw_defaults[index]
        if default_node is not None:
            try:
                text += f" = {ast.unparse(default_node)}"
            except Exception:
                text += " = ..."

        args.append(text)

    if node.args.kwarg:
        text = f"**{node.args.kwarg.arg}"
        annotation = _format_annotation(node.args.kwarg.annotation)
        if annotation:
            text += f": {annotation}"
        args.append(text)

    return_annotation = _format_annotation(node.returns)
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    signature = f"{prefix} {node.name}({', '.join(args)})"

    if return_annotation:
        signature += f" -> {return_annotation}"

    return signature


def _extract_imports(tree: ast.AST) -> list[str]:
    """Extract and format all import statements from a parsed AST module."""
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = ", ".join(alias.name for alias in node.names)
            imports.append(f"import {names}")

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = ", ".join(alias.name for alias in node.names)
            prefix = "." * node.level + module
            imports.append(f"from {prefix} import {names}")

    return sorted(set(imports))


def _node_to_code_node(node: ast.AST, source_code: str) -> CodeNode | None:
    """
    Convert an AST class or function node into a structured CodeNode.

    Extracts the signature, docstring, and the raw source code segment.
    """
    raw_source = ast.get_source_segment(source_code, node) or ""

    if isinstance(node, ast.ClassDef):
        bases = []
        for base in node.bases:
            try:
                bases.append(ast.unparse(base))
            except Exception:
                pass

        signature = f"class {node.name}"
        if bases:
            signature += f"({', '.join(bases)})"

        code_node = CodeNode(
            name=node.name,
            kind="class",
            line=node.lineno,
            signature=signature,
            docstring=ast.get_docstring(node) or "",
            source_code=raw_source
        )

    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        code_node = CodeNode(
            name=node.name,
            kind="function",
            line=node.lineno,
            signature=_format_function_signature(node),
            docstring=ast.get_docstring(node) or "",
            source_code=raw_source
        )

    else:
        return None

    for child in node.body:  # type: ignore[attr-defined]
        child_node = _node_to_code_node(child, source_code)
        if child_node is not None:
            code_node.children.append(child_node)

    return code_node


def _extract_structure(tree: ast.AST, source_code: str) -> list[CodeNode]:
    """Extract top-level classes and functions into a list of CodeNodes."""
    if not isinstance(tree, ast.Module):
        return []

    structure: list[CodeNode] = []
    for node in tree.body:
        code_node = _node_to_code_node(node, source_code)
        if code_node is not None:
            structure.append(code_node)

    return structure


def _scan_python_file(path: Path) -> FileDocumentation:
    """Analyze a single Python file and return its documentation model."""
    source = _read_text(path)
    block_comments = _extract_block_comments(source)

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as error:
        return FileDocumentation(
            file_name=path.name,
            file_path=str(path),
            module_docstring=None,
            block_comments=block_comments,
            imports=[],
            structure=[],
            syntax_error=f"Line {error.lineno}: {error.msg}",
        )

    return FileDocumentation(
        file_name=path.name,
        file_path=str(path),
        module_docstring=ast.get_docstring(tree),
        block_comments=block_comments,
        imports=_extract_imports(tree),
        structure=_extract_structure(tree, source),
    )


def _iter_python_files(directory: Path) -> Iterable[Path]:
    """Yield visible .py files from the target directory, ignoring hidden ones."""
    ignored_prefixes = (".", "__")

    for path in sorted(directory.glob("*.py")):
        if path.name.startswith(ignored_prefixes):
            continue
        yield path


@st.cache_data(show_spinner=False)
def build_project_documentation(directory_text: str) -> list[FileDocumentation]:
    """Build and cache documentation for all Python files in the directory."""
    directory = Path(directory_text)
    return [_scan_python_file(path) for path in _iter_python_files(directory)]


def _flatten_nodes(nodes: list[CodeNode], file_name: str) -> list[dict]:
    """Flatten the nested CodeNode structure for easier searching and menu generation."""
    flat_list = []
    for node in nodes:
        flat_list.append({"file": file_name, "node": node})
        flat_list.extend(_flatten_nodes(node.children, file_name))
    return flat_list


def render() -> None:
    """
    Render the Streamlit UI for the project documentation.

    Sets up the sidebar menu, search box, and the main display area for 
    viewing code and comments.
    """
    st.set_page_config(page_title="Project Docs", layout="wide")

    # Initialize session state for selected item
    if "selected_item" not in st.session_state:
        st.session_state.selected_item = None

    project_dir = _get_source_directory()
    docs = build_project_documentation(str(project_dir))

    # --- SIDEBAR: Search and Menu ---
    with st.sidebar:
        st.title("Navigation")
        search_query = st.text_input("🔍 Search functions/classes...", "").lower()

        if st.button("Refresh Documentation"):
            build_project_documentation.clear()
            st.rerun()

        st.divider()

        # Build menu
        for doc in docs:
            if doc.syntax_error:
                continue

            flat_nodes = _flatten_nodes(doc.structure, doc.file_name)

            # Filter nodes based on search query
            if search_query:
                flat_nodes = [item for item in flat_nodes if search_query in item["node"].name.lower()]

            # Only show file expander if it has matching nodes or if there's no search query
            if flat_nodes or not search_query:
                with st.expander(f"📄 {doc.file_name}", expanded=bool(search_query)):
                    if not search_query and st.button("View File Details", key=f"file_{doc.file_name}"):
                        st.session_state.selected_item = {"type": "file", "data": doc}

                    for item in flat_nodes:
                        node = item["node"]
                        icon = "📦" if node.kind == "class" else "⚡"
                        if st.button(f"{icon} {node.name}", key=f"btn_{doc.file_name}_{node.name}_{node.line}"):
                            st.session_state.selected_item = {"type": "node", "data": node, "file": doc.file_name}

    # --- MAIN AREA: Display Content ---
    st.title("Project Documentation")

    selected = st.session_state.selected_item

    if not selected:
        st.info("👈 Select a file or function from the sidebar menu to view its documentation and source code.")
        st.markdown(f"**Scanning directory:** `{project_dir}`")
        return

    if selected["type"] == "file":
        doc: FileDocumentation = selected["data"]
        st.header(f"File: {doc.file_name}")

        if doc.module_docstring:
            st.subheader("Module Docstring")
            st.info(doc.module_docstring)

        if doc.imports:
            st.subheader("Imports")
            st.code("\n".join(doc.imports), language="python")

        if doc.block_comments:
            st.subheader("File Block Comments")
            for idx, comment in enumerate(doc.block_comments):
                st.markdown(f"**Comment {idx + 1}:**\n```text\n{comment}\n```")

    elif selected["type"] == "node":
        node: CodeNode = selected["data"]
        file_name: str = selected["file"]

        st.header(f"{node.name}")
        st.caption(f"Defined in `{file_name}` at line {node.line} | Type: **{node.kind.capitalize()}**")

        st.subheader("Signature")
        st.code(node.signature, language="python")

        st.subheader("Documentation")
        if node.docstring:
            st.success(node.docstring)
        else:
            st.warning("No docstring provided for this item.")

        st.subheader("Source Code")
        if node.source_code:
            st.code(node.source_code, language="python")
        else:
            st.error("Source code could not be extracted.")

if __name__ == "__main__":
    render()