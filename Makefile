.PHONY: all init init-dev venv run lint format-check security check \
        test test-all test-unit test-network test-ui test-integration test-fast \
        coverage coverage-all coverage-network clean clean-venv \
        docstrcov rcc rcc-all help

.DEFAULT_GOAL := help
SHELL         := /bin/bash

VENV    := ~/.BlocksScreen-env
PYTHON  := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
SRC     := BlocksScreen
TESTS   := tests

PYTEST_IGNORE  := --ignore=$(TESTS)/network/test_sdbus_integration.py
PYTEST_FLAGS   ?= -vvv
NM_INTEGRATION := NM_INTEGRATION_TESTS=1

PYRCC5  := /usr/bin/pyrcc5
QRC_DIR := BlocksScreen/lib/ui/resources

# ─────────────────────────────────────────────────────────────────────────────
##@ Help
# ─────────────────────────────────────────────────────────────────────────────

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} \
	      /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2 } \
	      /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' \
	     $(MAKEFILE_LIST)

# ─────────────────────────────────────────────────────────────────────────────
##@ Environment
# ─────────────────────────────────────────────────────────────────────────────

venv: ## Print venv activation command (source manually — subshells cannot export)
	@echo "Run:  source $(VENV)/bin/activate"

init: ## Install production dependencies
	$(PIP) install -r scripts/requirements.txt

init-dev: ## Install dev + test dependencies
	$(PIP) install -r scripts/requirements-dev.txt

# ─────────────────────────────────────────────────────────────────────────────
##@ Run
# ─────────────────────────────────────────────────────────────────────────────

run: ## Launch the BlocksScreen application
	@echo "▶  Starting BlocksScreen..."
	$(PYTHON) BlocksScreen/BlocksScreen.py

# ─────────────────────────────────────────────────────────────────────────────
##@ Code Generation
# ─────────────────────────────────────────────────────────────────────────────

rcc: ## Compile git-modified .qrc files to PyQt6 Python modules (_rc.py)
	@files=$$(git diff --name-only HEAD -- '$(QRC_DIR)/*.qrc' 2>/dev/null; \
	          git ls-files --others --exclude-standard -- '$(QRC_DIR)/*.qrc' 2>/dev/null); \
	 if [ -z "$$files" ]; then echo "  No modified .qrc files."; exit 0; fi; \
	 for qrc in $$files; do \
	     out="$${qrc%.qrc}_rc.py"; \
	     echo "  $$qrc → $$out"; \
	     $(PYRCC5) "$$qrc" -o "$$out"; \
	     sed -i 's/from PyQt5 import QtCore/from PyQt6 import QtCore/' "$$out"; \
	 done

rcc-all: ## Force recompile all .qrc files
	@for qrc in $(QRC_DIR)/*.qrc; do \
	     out="$${qrc%.qrc}_rc.py"; \
	     echo "  $$qrc → $$out"; \
	     $(PYRCC5) "$$qrc" -o "$$out"; \
	     sed -i 's/from PyQt5 import QtCore/from PyQt6 import QtCore/' "$$out"; \
	 done

# ─────────────────────────────────────────────────────────────────────────────
##@ Linting & Security
# ─────────────────────────────────────────────────────────────────────────────

lint: ## Run pylint
	$(PYTHON) -m pylint $(SRC)

format-check: ## Verify formatting without modifying files (ruff-based)
	$(PYTHON) -m ruff format --check $(SRC) $(TESTS)
	$(PYTHON) -m ruff check $(SRC) $(TESTS)

security: ## Run bandit security scan
	$(PYTHON) -m bandit -c pyproject.toml -r $(SRC)

check: format-check lint security test-fast ## Full pre-push gate (mirrors CI)

# ─────────────────────────────────────────────────────────────────────────────
##@ Tests
# ─────────────────────────────────────────────────────────────────────────────

test: ## Unit + UI tests (excludes real D-Bus integration)
	$(PYTHON) -m pytest $(PYTEST_FLAGS) $(PYTEST_IGNORE) $(TESTS)

test-fast: ## Stop on first failure, quiet output
	$(PYTHON) -m pytest -x -q $(PYTEST_IGNORE) $(TESTS)

test-unit: ## Unit tests only (*_unit.py)
	$(PYTHON) -m pytest $(PYTEST_FLAGS) $(TESTS)/*/*_unit.py

test-ui: ## UI tests only (*_ui.py)
	$(PYTHON) -m pytest $(PYTEST_FLAGS) $(TESTS)/*/*_ui.py

test-network: ## Network subsystem tests (unit + UI, no D-Bus)
	$(PYTHON) -m pytest $(PYTEST_FLAGS) $(PYTEST_IGNORE) $(TESTS)/network/

test-integration: ## D-Bus integration tests (requires live NetworkManager)
	$(NM_INTEGRATION) $(PYTHON) -m pytest $(PYTEST_FLAGS) $(TESTS)/*/*_integration.py

test-all: ## All tests including D-Bus integration (requires NetworkManager)
	$(NM_INTEGRATION) $(PYTHON) -m pytest $(PYTEST_FLAGS) -m "" $(TESTS)

# ─────────────────────────────────────────────────────────────────────────────
##@ Coverage
# ─────────────────────────────────────────────────────────────────────────────

COVERAGE_FLAGS := --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=40

coverage: ## Coverage report — HTML + terminal (fail-under=40%)
	$(PYTHON) -m pytest $(PYTEST_IGNORE) --cov=$(SRC) $(COVERAGE_FLAGS) $(TESTS)
	@echo "Coverage report: htmlcov/index.html"

coverage-all: ## Coverage including integration tests
	$(NM_INTEGRATION) $(PYTHON) -m pytest -m "" --cov=$(SRC) $(COVERAGE_FLAGS) $(TESTS)
	@echo "Coverage report: htmlcov/index.html"

# ─────────────────────────────────────────────────────────────────────────────
##@ Documentation
# ─────────────────────────────────────────────────────────────────────────────

docstrcov: ## Check docstring coverage (fail-under=80%, matches CI)
	$(PYTHON) -m docstr_coverage $(SRC) \
	    --exclude '.*/$(SRC)/lib/ui/.*?$$' \
	    --fail-under 80 \
	    --skip-magic --skip-init --skip-private --skip-property



# ─────────────────────────────────────────────────────────────────────────────
##@ Cleanup
# ─────────────────────────────────────────────────────────────────────────────

clean: ## Remove build artefacts, caches, and coverage data
	rm -rf dist/ build/ *.egg-info src/*.egg-info site/ htmlcov .coverage
	find . -depth \
	     \( -type f -name '*.py[co]' \
	     -o -type d -name __pycache__ \
	     -o -type d -name .pytest_cache \) -exec rm -rf {} +

clean-venv: ## Remove the virtual environment (destructive!)
	@echo "Removing $(VENV)..."
	rm -rf $(VENV)
