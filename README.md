
# fairtool - Computational Materials Data Processing made FAIR

<img width="800" alt="Fairtool" src="./documentation/docs/assets/images/fairtool.png"/>

FAIR Tool is a command-line interface for processing, analyzing, and visualizing computational materials data.
It is designed to work with various calculation output files and provides a streamlined workflow.

#### Project Lead: Dr. Ravindra Shinde
#### Email : r.l.shinde@utwente.nl

#### Contributor: Konstantinos Kontogiannis
#### Email : k.kontogiannis@student.utwente.nl

## Funding: 4TU Research Data Fund 4th Edition

# Installing fairtool with uv

This guide explains how to install the `fairtool` package and its dependencies using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

## Prerequisites
- [uv](https://github.com/astral-sh/uv) installed (see below)
- Git (optional, for cloning the repository)

## 1. Clone the Repository (if needed)
```bash
git clone https://github.com/neelravi/fairtool.git
cd fairtool
```

## 2. Install uv
If you don't have `uv` installed, run:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

This will install `uv` to `~/.local/bin/uv` by default. Make sure this directory is in your `PATH`.

You may install Python using uv quickly with:

```bash
uv python install 3.9
```

## 3. Create a Virtual Environment with uv
It's recommended to use a virtual environment. You can create one using uv:

```bash
uv venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies with uv
From the project root directory, run:

```bash
uv pip install -r requirements.txt
```

This will install all required dependencies quickly using uv's resolver.

## 5. Install fairtool (Editable/Development Mode)
To install the package in editable mode (recommended for development):

```bash
uv pip install -e .
```

## 6. Run the CLI
You can now run the CLI using:

```bash
fair
```

## Troubleshooting
- Ensure you are using Python 3.9 for best compatibility.
- If you see `ModuleNotFoundError: No module named 'fairtool'`, make sure your `PYTHONPATH` includes the project root.
- If `uv` is not found, ensure `~/.local/bin` is in your `PATH`.

## References
- [uv documentation](https://github.com/astral-sh/uv)
- [fairtool repository](https://github.com/neelravi/fairtool)

