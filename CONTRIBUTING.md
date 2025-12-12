# Contributing

Thanks for your interest in contributing!

## Development setup

- Python: 3.11+

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Lint (optional)

This repo uses Ruff for a lightweight static check.

```bash
python -m pip install ruff
ruff check src tests
```
