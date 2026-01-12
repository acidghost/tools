.PHONY: server index check clean help hooks

# All HTML tool files (excluding index files)
TOOLS := $(filter-out index.html index.template.html, $(wildcard *.html))

## help: Show this help message
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /' | sort

## index: Generate index.html from template and tools
index: index.html

## index.html: Generate index.html from template and tools
index.html: index.template.html update_index.py $(TOOLS)
	python3 update_index.py

## check: Check if index.html is up to date (for CI/CD)
check:
	python3 update_index.py --check

## clean: Remove generated files and _site directory
clean:
	rm -rf _site
	rm -f index.html

## server: Create _site with symlinks and start server on port 8080
server: clean _site
	@echo "Serving http://localhost:8080"
	@python3 -m http.server 8080 -d _site

## _site: Create _site directory with symlinks to HTML files
_site: index.html
	@mkdir -p _site
	@for file in *.html; do \
		ln -sf "../$$file" "_site/$$file" 2>/dev/null || true; \
	done
	@echo "Created _site/ with symlinks to HTML files"

## hooks: Install pre-commit hooks
hooks:
	@pre-commit install
	@echo "Pre-commit hooks installed. Index will be auto-generated on commit."
