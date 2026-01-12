# AGENTS.md - Guide to Building HTML Tools

This guide summarizes patterns from [Simon Willison's guide](https://simonwillison.net/2025/Dec/10/html-tools/) for building HTML tools - single-file HTML applications combining HTML, JavaScript, and CSS.

## What Are HTML Tools?

Single-file web applications that:

- Combine HTML, CSS, and JavaScript in one file
- Provide useful functionality without a build step
- Can be easily copied, pasted, and self-hosted
- Are typically a few hundred lines of code

## Core Principles

### 1. Single File Structure

- Inline JavaScript and CSS in a single HTML file
- Easiest for hosting and distribution
- Can be copied and pasted directly from LLM responses

### 2. No React / No Build Step

- **Avoid React** - JSX requires a build step
- **Avoid anything with a build step** (npm, webpack, vite, etc.)
- Always specify "No React" in prompts when asking LLMs to build tools
- Use vanilla JavaScript or load libraries from CDNs

### 3. Load Dependencies from CDNs

- Use cdnjs, jsdelivr, or similar for dependencies
- Include version numbers in CDN URLs for stability
- Fewer dependencies is better

### 4. Keep Them Small

- Aim for a few hundred lines of code
- Makes the code maintainable and easily understood by LLMs
- Rewriting from scratch with an LLM takes just minutes

## Repository Requirements

### 1. Required Meta Tags

All tools MUST include a `<meta name="description">` tag in the HTML `<head>`:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="A clear, concise description of what the tool does.">
  <title>Tool Name</title>
</head>
```

The description is used in the auto-generated index page and helps users understand the tool's purpose at a glance.

### 2. Auto-Generated Index

This repository uses `update_index.py` to automatically generate `index.html` from the template file (`index.template.html`). The script:

- Extracts title and description from each tool's HTML
- Requires a description meta tag (will fail if missing)
- Runs automatically via pre-commit hooks

## Development Workflow

### Prototyping Phase

Use LLM "Canvas" or "Artifacts" features:

- **Claude**: Has "Artifacts" enabled by default
- **ChatGPT**: Has "Canvas" (may need to toggle in tools menu)
- **Gemini**: Has "Canvas" (may need to toggle in tools menu)

**Example prompts:**

- Claude: "Build an artifact that lets me paste in JSON and converts it to YAML. No React."
- ChatGPT/Gemini: "Build a canvas that lets me paste in JSON and converts it to YAML. No React."

Always add "No React" to prompts!

### For Complex Projects

Switch to coding agents like:

- **Claude Code** - Can test code with Playwright
- **Codex CLI** - Can run tests and deploy via PRs

These agents can work against a git repository and publish tools without manual copy-paste.

## Hosting

### Recommended: GitHub Pages

- Create a GitHub repo with GitHub Pages enabled
- Settings → Pages → Source → Deploy from a branch → main
- Paste HTML files and get permanent URLs instantly

### Why Not LLM Platform Hosting?

- LLM platforms run tools in sandboxes with restrictions
- Cannot load data/images from external URLs
- Show warning messages to users
- Less reliable during outages
- Self-hosting gives you full control

## Key Patterns

### Copy and Paste

- Accept pasted content, transform it, let users copy it back
- Include "Copy to clipboard" buttons for mobile usability
- Use clipboard paste events to access rich data formats

**Examples:**

- JSON to YAML converters
- Rich text extractors
- Thread export tools

### Debugging Tools

Build tools to explore what's possible:

- **clipboard-viewer** - Shows all paste data types available
- **keyboard-debug** - Shows key codes being pressed
- **cors-fetch** - Reveals if a URL supports CORS
- **exif** - Displays EXIF data from photos

### Persist State in URL

- Store state directly in URL parameters
- Great for bookmarkable and shareable tools
- Good for smaller state that fits in URL length limits

### Use localStorage

- For larger state that doesn't fit in URLs
- For secrets like API keys (never expose keys in HTML)
- Use `prompt()` to get API key, store in `localStorage`
- Saves work from accidental tab closes

**Examples:**

- Word counters that save as you type
- Markdown editors with auto-save
- LLM demo tools that store API keys

### CORS-Enabled APIs

Collect APIs with open CORS headers - these are goldmines:

**Useful CORS APIs:**

- **iNaturalist** - Animal sightings with photo URLs
- **PyPI** - Python package details
- **GitHub** - Public repo content via `raw.githubusercontent.com`
- **Bluesky** - Full API with CORS
- **Mastodon** - Generous CORS policies
- **GitHub Gists** - Persist state via API

**Example tools:**

- Species observation maps using iNaturalist
- Python package explorers using PyPI
- Issue-to-Markdown converters using GitHub API
- Terminal session savers using Gists

### LLM APIs via CORS

OpenAI, Anthropic, and Gemini all support CORS:

- Requires API key stored in `localStorage` (user experience friction but works)
- Users must create their own API keys
- Never bake keys into visible HTML

### File Handling

Use `<input type="file">` without server upload:

- JavaScript can access file content directly
- No server needed for processing

**Examples:**

- PDF to image conversion using PDF.js
- Image cropping for social media
- Video cropping (generates ffmpeg command)

### Downloadable Files

Generate files for download without a server:

- Use JavaScript libraries for file generation
- Create PNG, JPEG, ICS, etc. in browser

**Libraries:**

- File-saver.js for downloads
- Various format-specific libraries

### Python in Browser: Pyodide

- Python compiled to WebAssembly
- Loads from CDN
- Can use micropip to install pure-Python packages from PyPI

**Use cases:**

- Running pandas/matplotlib in browser
- Interactive tutorials
- SQLite query analysis

### WebAssembly

Opens many possibilities:

- **Tesseract.js** - OCR in browser
- Image compression libraries (like Squoosh.app)
- Ported C/Perl utilities (SLOCCount)
- MicroPython for smaller Python runtime

## Remix Existing Tools

When building new tools:

1. Reference existing tools by name when working with coding agents
2. Copy/paste source code of similar tools as context
3. Source code serves as documentation of patterns
4. LLMs with 1-2 example tools are more likely to produce working code

**Example workflow:**

1. "Look at the pypi package explorer tool"
2. "Build a new tool that uses similar patterns but does X differently"

## Documentation Practices

### Record Prompts and Transcripts

- Keep records of LLM interactions to improve skills
- For LLM platform tools: use "share" feature
- For coding agents: copy transcript to terminal-to-html tool
- Include links in commit messages when saving to repository

### Add "View Source" Links

Include links in tool footers to:

- View source on GitHub
- See the prompt used to create it
- Read the full transcript

## Example Tools Reference

Simon maintains a collection at **tools.simonwillison.net** with 150+ tools including:

- **svg-render** - SVG to JPEG/PNG
- **pypi-changelog** - PyPI release diffs
- **bluesky-thread** - Nested thread viewer
- **hacker-news-thread-export** - Condensed thread export
- **paste-rich-text** - Rich text HTML extractor
- **alt-text-extractor** - Image alt text extraction
- **word-counter** - Writing with word count limits
- **render-markdown** - Markdown editor
- **haiku** - Webcam haiku generator using Claude API
- **ocr** - PDF/image OCR in browser
- **social-media-cropper** - Image cropping for social platforms
- **ffmpeg-crop** - Video cropping command generator

## Quick Start Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My HTML Tool</title>
    <style>
        /* Inline CSS here */
        body {
            font-family: system-ui, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
    </style>
</head>
<body>
    <h1>My HTML Tool</h1>
    <!-- Tool interface here -->

    <script>
        // Inline JavaScript here
        // No React, no build step
        // Load any dependencies from CDN if needed
    </script>
</body>
</html>
```

## When to Use This Approach

**Good for:**

- Single-purpose utilities
- Data transformation tools
- Debugging/diagnostic tools
- Prototypes and demos
- Tools that benefit from client-side processing
- Educational examples

**Not ideal for:**

- Complex multi-page applications
- Apps requiring server-side processing
- Large team projects
- Applications with complex state management

## Further Reading

- [Original article](https://simonwillison.net/2025/Dec/10/html-tools/)
- [tools.simonwillison.net](https://tools.simonwillison.net/) - Browse by month for full collection
- GitHub: simonw/tools repository
