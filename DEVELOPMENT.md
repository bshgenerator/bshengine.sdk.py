## Development

### Setting Up Development Environment

**Important**: Always use a virtual environment for development to avoid conflicts with global Python packages.

#### Quick Setup (Recommended)

**Linux/macOS:**
```bash
chmod +x setup_env.sh
./setup_env.sh
```

**Windows:**
```batch
setup_env.bat
```

#### Manual Setup

1. Create virtual environment:
```bash
python3 -m venv venv
```

2. Activate virtual environment:
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Install package in development mode:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate      # Windows

# Run tests
pytest

# Run tests with coverage
pytest --cov=bshengine --cov-report=html
```

### Building

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate      # Windows

# Build the package
python -m build

# Install locally
pip install -e .
```

### Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```
