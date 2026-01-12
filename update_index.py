#!/usr/bin/env python3
"""Generate index.html for HTML tools repository.

Scans the current directory for *.html files (excluding index.html itself),
extracts metadata (title, description) from each, and generates an index page.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path


class MissingDescriptionError(Exception):
    """Raised when a tool is missing a required meta description."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        super().__init__(f"Tool '{filename}' is missing required <meta name='description'> tag")


@dataclass(frozen=True)
class ToolInfo:
    """Metadata about a tool extracted from its HTML file."""

    filename: str
    title: str
    description: str


def extract_title(content: str) -> str | None:
    """Extract the title from HTML content."""
    match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_description(content: str) -> str | None:
    """Extract the description from meta tag in HTML content."""
    match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        content,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    return None


def scan_tools(directory: Path, exclude: list[str] | None = None) -> list[ToolInfo]:
    """Scan directory for HTML tool files and extract metadata.

    Args:
        directory: Directory to scan for HTML files.
        exclude: Filenames to exclude from scanning.

    Returns:
        List of ToolInfo objects, sorted alphabetically by filename.

    Raises:
        MissingDescriptionError: If a tool is missing a meta description.
    """
    if exclude is None:
        exclude = ["index.html", "index.template.html"]

    tools: list[ToolInfo] = []

    for filepath in directory.glob("*.html"):
        if filepath.name.lower() in [e.lower() for e in exclude]:
            continue

        try:
            content = filepath.read_text(encoding="utf-8")
            title = extract_title(content) or filepath.stem.replace("-", " ").replace("_", " ").title()
            description = extract_description(content)

            if description is None:
                raise MissingDescriptionError(filepath.name)

            tools.append(
                ToolInfo(
                    filename=filepath.name,
                    title=title,
                    description=description,
                )
            )
        except OSError as e:
            print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)

    return sorted(tools, key=lambda t: t.filename.lower())


def _render_tools_html(tools: list[ToolInfo]) -> str:
    """Render the list of tools as HTML.

    Args:
        tools: List of ToolInfo objects to include in the index.

    Returns:
        HTML string containing all tool items.
    """

    def esc(s: str) -> str:
        return html.escape(s)

    tool_items = []
    for tool in tools:
        title_html = esc(tool.title)
        desc_html = f"<p>{esc(tool.description)}</p>"
        tool_items.append(f"""        <li class="tool-item">
            <a href="{esc(tool.filename)}" class="tool-link">
                <span class="tool-title">{title_html}</span>
            </a>{desc_html}
        </li>""")

    return "\n".join(tool_items)


def generate_index_html(tools: list[ToolInfo], template_path: Path) -> str:
    """Generate index.html by reading template and injecting tools.

    Args:
        tools: List of ToolInfo objects to include in the index.
        template_path: Path to the template file.

    Returns:
        Complete HTML document as a string.

    Raises:
        FileNotFoundError: If template file doesn't exist.
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    tools_html = _render_tools_html(tools)
    return template.replace("<!-- TOOLS_LIST -->", tools_html)


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate index.html for HTML tools repository"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check if index.html needs updating (exit 1 if out of date)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        default=True,
        help="Write index.html (default behavior, use with --dry-run to preview)",
    )

    args = parser.parse_args()

    # Disable write if dry-run is specified
    if args.dry_run:
        args.write = False

    repo_dir = Path(__file__).parent.resolve()
    index_path = repo_dir / "index.html"
    template_path = repo_dir / "index.template.html"

    # Scan for tools
    tools = scan_tools(repo_dir)

    # Generate new content
    new_content = generate_index_html(tools, template_path)

    # Check if file exists and compare content
    if index_path.exists():
        existing_content = index_path.read_text(encoding="utf-8")
        if existing_content == new_content:
            if args.dry_run or args.check:
                print("index.html is up to date.")
            return 0

    # Handle --check mode
    if args.check:
        print("index.html is out of date.", file=sys.stderr)
        return 1

    # Handle --dry-run mode
    if args.dry_run:
        print("index.html would be updated:")
        print("=" * 60)
        print(new_content)
        print("=" * 60)
        return 0

    # Write the file
    index_path.write_text(new_content, encoding="utf-8")
    print(f"Generated index.html with {len(tools)} tool(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
