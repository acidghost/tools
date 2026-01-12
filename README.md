# HTML Tools

A collection of single-file HTML+JavaScript tools. No build step, no dependencies — just open and use.

## What These Tools Are

Each tool is a self-contained HTML file that works directly in your browser. They follow [Simon Willison's patterns](https://simonwillison.net/2025/Dec/10/html-tools/) for building client-side web applications:

- **Single file**: HTML, CSS, and JavaScript all in one place
- **No build step**: No npm, no webpack, no frameworks requiring compilation
- **CDN dependencies**: External libraries loaded from CDNs when needed
- **Easy to host**: Drop on any web server or use GitHub Pages

## How to Use

### Direct Opening

Most tools can be opened directly in your browser by double-clicking the HTML file.

### Local Server (Recommended)

For tools that need to handle file URLs or make CORS requests:

```bash
make server
# or
python3 -m http.server 8080
```

Then open http://localhost:8080

## Tools

See the [index](index.html) for a complete list of available tools.

- **countdown-timer.html** — Visual countdown timer
- **github-actions-sha-converter.html** — Convert GitHub Actions tags to SHA hashes
- **list-rearranger.html** — Rearrange items in a list
- **list-tagger.html** — Tag items in a list

## Development

### Pre-commit Hooks

Install pre-commit hooks to auto-generate `index.html` before each commit:

```bash
# Install pre-commit
uv tool install pre-commit

# Install the git hooks
make hooks
```

Now `index.html` will be automatically updated before each commit.

### Manual Index Generation

```bash
# Generate or update index.html
make index
# or
python3 update_index.py

# Check if index.html is up-to-date (for CI/CD)
make check
# or
python3 update_index.py --check
```
