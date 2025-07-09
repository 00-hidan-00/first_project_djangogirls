
# 🧰 Code Quality & Linting Guide

This project uses a set of automated tools to ensure code quality, security, and consistency across the codebase.

---
## 🛠 Tools Overview
| Tool                    | Purpose                                                                  |
|-------------------------|--------------------------------------------------------------------------|
| pyupgrade               | Automatically upgrades Python syntax to match the target version (3.12+) |
| black                   | Formats Python code according to strict PEP8-compatible rules            |
| isort                   | Sorts and groups imports in a consistent order (aligned with black)      |
| flake8                  | Lints code for syntax issues and style violations                        |
| mypy                    | Performs static type checking using Python type hints                    |
| prospector              | Runs multiple linters in one pass (e.g., flake8, mccabe, docstyle, etc.) |
| detect-secrets          | Scans for hardcoded secrets like API keys, tokens, passwords             |
| trufflehog              | Detects high-entropy strings that may indicate secrets                   |
| check-merge-conflict    | Prevents commits with unresolved merge conflict markers                  |
| check-added-large-files | Blocks committing files larger than 500KB                                |

---
## ⚙️ Configuration Files

| File                            | Description                                             |
|---------------------------------|---------------------------------------------------------|
| `.pre-commit-config.yaml`       | Defines all pre-commit hooks and their versions         |
| `.prospector.yaml`              | Configuration for meta-linter prospector                |
| `.flake8`                       | Custom rules for flake8 (if used separately)            |
| `.mypy.ini` or `pyproject.toml` | Config file for mypy                                    |
| `Makefile`                      | Commands to run linting, formatting, and cleanup        |
| `.editorconfig`                 | Basic editor formatting rules (tabs, indentation, etc.) |


---
## ✅ Usage
To install and run all checks locally:

## 1. Install pre-commit and dependencies

```shell
pip install pre-commit
```

### 2. Initialize hooks

```shell
pre-commit install
```

### 3. Run all hooks on staged files

```shell
pre-commit run
```

### 4. Run all hooks on entire project

```shell
pre-commit run --all-files
```
### Or use Makefile shortcuts:

```shell
make pre-commit-init      # Install hooks
```

```shell
make pre-commit-run-all   # Run all hooks
```

```shell
make pre-commit-clean     # Clear hook cache
```

---
## 📦 CI Integration

All pre-commit hooks are automatically run in GitHub Actions CI pipeline via:
- `.github/workflows/ci.yml`
- Python versions: `3.12`
- Linting, formatting, typing, and secrets scanning are performed on push / pull requests.

---
## ⚠️ Notes
- Tools like `flake8` and `black` should not be duplicated between `.prospector.yaml` and `.pre-commit-config.yaml`.
- If a tool is disabled in one place, it should only run where intended.
- `noqa` comments (`# noqa: F401`) can be used to skip linting on specific lines.
- You can temporarily disable a hook by commenting it out in `.pre-commit-config.yaml`.
---