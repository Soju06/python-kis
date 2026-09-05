"""
Generate API reference documentation from source code.

This script extracts docstrings and type hints from vmkis modules
and generates markdown documentation.
"""

import ast
from pathlib import Path
from typing import Any


def extract_module_info(module_path: Path) -> dict[str, Any]:
    """Extract classes, functions, and their docstrings from a Python module."""
    with open(module_path, encoding="utf-8") as f:
        tree = ast.parse(f.read())

    classes = []
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node) or "(No docstring)"
            methods = []

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    if not item.name.startswith("_"):  # Public methods only
                        method_doc = ast.get_docstring(item) or ""
                        methods.append(
                            {"name": item.name, "docstring": method_doc.split("\n")[0] if method_doc else ""}
                        )

            classes.append({"name": node.name, "docstring": docstring, "methods": methods})

        elif isinstance(node, ast.FunctionDef):
            if not node.name.startswith("_"):  # Public functions only
                docstring = ast.get_docstring(node) or "(No docstring)"
                functions.append({"name": node.name, "docstring": docstring})

    return {"classes": classes, "functions": functions}


def generate_markdown(modules: dict[str, dict[str, Any]]) -> str:
    """Generate markdown documentation from extracted module info."""
    md = ["# API Reference\n\n"]
    md.append("자동 생성된 API 레퍼런스 문서입니다.\n\n")
    md.append("---\n\n")
    md.append("## 목차\n\n")

    # Table of contents
    for module_name in sorted(modules.keys()):
        md.append(f"- [{module_name}](#{module_name.replace('.', '-')})\n")

    md.append("\n---\n\n")

    # Module details
    for module_name, info in sorted(modules.items()):
        md.append(f"## {module_name}\n\n")

        if info["classes"]:
            md.append("### Classes\n\n")
            for cls in info["classes"]:
                md.append(f"#### `{cls['name']}`\n\n")
                md.append(f"{cls['docstring']}\n\n")

                if cls["methods"]:
                    md.append("**Methods:**\n\n")
                    for method in cls["methods"]:
                        line = f"- `{method['name']}()`"
                        if method["docstring"]:
                            line += f": {method['docstring']}"
                        md.append(line + "\n")
                    md.append("\n")

        if info["functions"]:
            md.append("### Functions\n\n")
            for func in info["functions"]:
                md.append(f"#### `{func['name']}()`\n\n")
                md.append(f"{func['docstring']}\n\n")

        md.append("---\n\n")

    return "".join(md)


REPO_ROOT = Path(__file__).resolve().parent.parent
VMKIS_DIR = REPO_ROOT / "src" / "vmkis"
OUTPUT_PATH = REPO_ROOT / "docs" / "generated" / "API_REFERENCE.md"

#: 공개 API 만. 여기 없는 모듈은 레퍼런스에 안 나옵니다.
TARGET_FILES = (
    "kis.py",
    "simple.py",
    "helpers.py",
    "public_types.py",
    "client/auth.py",
)


def collect_modules() -> dict[str, dict[str, Any]]:
    """소스에서 레퍼런스에 실을 모듈 정보를 모읍니다."""
    modules: dict[str, dict[str, Any]] = {}

    for file_path in TARGET_FILES:
        full_path = VMKIS_DIR / file_path
        if full_path.exists():
            module_name = f"vmkis.{file_path.replace('.py', '').replace('/', '.')}"
            modules[module_name] = extract_module_info(full_path)

    return modules


def render() -> str:
    """커밋된 파일과 같은 문자열을 만듭니다. 검사는 이 함수를 다시 부릅니다.

    끝의 빈 줄과 메서드 줄 뒤 공백은 pre-commit 훅이 지웁니다.
    여기서 먼저 맞춰야 재생성이 훅과 싸우지 않습니다.
    """
    return generate_markdown(collect_modules()).rstrip() + "\n"


def main() -> None:
    """Main entry point for API reference generation."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"✅ API Reference generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
