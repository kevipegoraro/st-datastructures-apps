"""
documentation.py

Streamlit documentation page for this project.

This page scans all Python files in the same directory, reads module
comments/docstrings, extracts functions/classes, and renders a simple
project documentation view inside the app.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import streamlit as st


@dataclass
class CodeNode:
    """Represents one class or function found in a Python file."""

    name: str
    kind: str
    line: int
    signature: str = ""
    docstring: str = ""
    children: list["CodeNode"] = field(default_factory=list)


@dataclass
class FileDocumentation:
    """Stores extracted documentation for one Python file."""

    file_name: str
    file_path: str
    module_docstring: str | None
    block_comments: list[str]
    imports: list[str]
    structure: list[CodeNode]
    syntax_error: str | None = None


def _get_source_directory() -> Path:
    """Return the directory that contains this documentation.py file."""
    return Path(__file__).resolve().parent


def _read_text(path: Path) -> str:
    """Read a Python file with UTF-8 fallback protection."""
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_block_comments(source: str) -> list[str]:
    """
    Extract contiguous groups of # comments.

    These are treated as block comments because Python does not have an
    official block-comment syntax. Triple-quoted text is handled separately
    as a docstring by the AST parser.
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
    """Convert a function annotation AST node into readable text."""
    if annotation is None:
        return ""

    try:
        return ast.unparse(annotation)
    except Exception:
        return ""


def _format_function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Build a readable function signature from an AST function node."""
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
    """Extract import statements from a parsed Python module."""
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


def _node_to_code_node(node: ast.AST) -> CodeNode | None:
    """Convert a function/class AST node into a CodeNode tree."""
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
        )

    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        code_node = CodeNode(
            name=node.name,
            kind="function",
            line=node.lineno,
            signature=_format_function_signature(node),
            docstring=ast.get_docstring(node) or "",
        )

    else:
        return None

    for child in node.body:  # type: ignore[attr-defined]
        child_node = _node_to_code_node(child)
        if child_node is not None:
            code_node.children.append(child_node)

    return code_node


def _extract_structure(tree: ast.AST) -> list[CodeNode]:
    """Extract top-level classes/functions and their nested children."""
    if not isinstance(tree, ast.Module):
        return []

    structure: list[CodeNode] = []
    for node in tree.body:
        code_node = _node_to_code_node(node)
        if code_node is not None:
            structure.append(code_node)

    return structure


def _scan_python_file(path: Path) -> FileDocumentation:
    """Analyze one Python file and return its documentation model."""
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
        structure=_extract_structure(tree),
    )


def _iter_python_files(directory: Path) -> Iterable[Path]:
    """Yield visible .py files from the project directory."""
    ignored_prefixes = (".", "__")

    for path in sorted(directory.glob("*.py")):
        if path.name.startswith(ignored_prefixes):
            continue
        yield path


@st.cache_data(show_spinner=False)
def build_project_documentation(directory_text: str) -> list[FileDocumentation]:
    """Build documentation for all Python files in the selected directory."""
    directory = Path(directory_text)
    return [_scan_python_file(path) for path in _iter_python_files(directory)]


def _render_code_node(node: CodeNode, level: int = 0) -> None:
    """Render one CodeNode and its children as a simple markdown tree."""
    indent = "&nbsp;" * (level * 4)
    icon = "C" if node.kind == "class" else "F"

    st.markdown(
        f"{indent}- `{icon}` **{node.name}** — line `{node.line}`  "
        f"<br>{indent}&nbsp;&nbsp;`{node.signature}`",
        unsafe_allow_html=True,
    )

    if node.docstring:
        with st.expander(f"Docstring: {node.name}"):
            st.markdown(node.docstring)

    for child in node.children:
        _render_code_node(child, level + 1)


def _count_nodes(nodes: list[CodeNode]) -> int:
    """Count all functions/classes in a structure tree."""
    return sum(1 + _count_nodes(node.children) for node in nodes)


def render() -> None:
    """Render the automatic project documentation page."""
    st.title("Project Documentation")

    st.markdown(
        "This page reads all `.py` files in the project directory and builds "
        "simple documentation from docstrings, block comments, imports, "
        "classes, and functions."
    )

    project_dir = _get_source_directory()

    col1, col2 = st.columns([2, 1])
    col1.code(str(project_dir), language="text")

    if col2.button("Refresh documentation", key="btn_refresh_documentation"):
        build_project_documentation.clear()

    docs = build_project_documentation(str(project_dir))

    total_files = len(docs)
    total_blocks = sum(len(doc.block_comments) for doc in docs)
    total_nodes = sum(_count_nodes(doc.structure) for doc in docs)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Python files", total_files)
    metric_col2.metric("Comment blocks", total_blocks)
    metric_col3.metric("Functions/classes", total_nodes)

    selected_files = st.multiselect(
        "Files to show",
        options=[doc.file_name for doc in docs],
        default=[doc.file_name for doc in docs],
        key="documentation_selected_files",
    )

    for doc in docs:
        if doc.file_name not in selected_files:
            continue

        with st.expander(doc.file_name, expanded=True):
            if doc.syntax_error:
                st.error(f"Syntax error: {doc.syntax_error}")
                continue

            st.subheader("Module docstring")
            if doc.module_docstring:
                st.markdown(doc.module_docstring)
            else:
                st.caption("No module docstring found.")

            st.subheader("Block comments")
            if doc.block_comments:
                for index, block in enumerate(doc.block_comments, start=1):
                    with st.expander(f"Comment block {index}"):
                        st.markdown(block)
            else:
                st.caption("No block comments found.")

            st.subheader("Imports")
            if doc.imports:
                st.code("\n".join(doc.imports), language="python")
            else:
                st.caption("No imports found.")

            st.subheader("Structure tree")
            if doc.structure:
                for node in doc.structure:
                    _render_code_node(node)
            else:
                st.caption("No classes or functions found.")
