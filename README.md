# fin-doc-rag

A Retrieval-Augmented Generation (RAG) system to assist with searching and understanding accounting and financial analysis manuals.

## Setup

This project uses [Poetry](https://python-poetry.org/) for dependency and environment management.

### 1. Install Poetry

If you don’t have Poetry installed, run the following command:

**Linux/macOS:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows (PowerShell):**
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
After installation, restart your shell or run ```poetry --version``` to verify it’s available.

### 2. Create a Virtual Environment

Navigate to the project directory and set up the environment:

```bash
cd fin-doc-rag
poetry install
```
This will create a virtual environment and install all project dependencies.

If you want to activate the environment manually:

**Linux/macOS:**
```bash
source $(poetry env info --path)/bin/activate
```

**Windows (Command Prompt):**
```bash
%USERPROFILE%\.cache\pypoetry\virtualenvs\<your-env>\Scripts\activate.bat
```
**Windows (PowerShell):**
```bash
& "$env:USERPROFILE\.cache\pypoetry\virtualenvs\<your-env>\Scripts\Activate.ps1"
```


poetry env info --path