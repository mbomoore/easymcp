# Installation Guide

This guide covers different methods for installing easymcp.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Using uvx (Recommended)

The easiest way to install and run easymcp is using [uvx](https://docs.astral.sh/uv/):

```bash
# Run directly without installation
uvx easymcp --help

# Initialize a config
uvx easymcp init

# Start servers
uvx easymcp start --all
```

### Method 2: Using pip

Install globally with pip:

```bash
pip install easymcp
```

Or install in a virtual environment:

```bash
# Create a virtual environment
python -m venv easymcp-env

# Activate it
source easymcp-env/bin/activate  # On Linux/macOS
# or
easymcp-env\Scripts\activate  # On Windows

# Install easymcp
pip install easymcp
```

### Method 3: Using pipx

Install with [pipx](https://pipx.pypa.io/) for isolated environment:

```bash
pipx install easymcp
```

### Method 4: From Source

For development or the latest features:

```bash
# Clone the repository
git clone https://github.com/mbomoore/easymcp.git
cd easymcp

# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Verify Installation

Check that easymcp is installed correctly:

```bash
easymcp --version
```

You should see the version number printed.

## Next Steps

1. **Initialize configuration**: Create a new configuration file
   ```bash
   easymcp init
   ```

2. **Edit configuration**: Open `easymcp.yaml` and add your MCP servers

3. **Start servers**: Launch your configured servers
   ```bash
   easymcp start --all
   ```

4. **Check status**: Verify servers are running
   ```bash
   easymcp status
   ```

## Updating

### If installed with uvx

uvx automatically uses the latest version each time you run it.

### If installed with pip

```bash
pip install --upgrade easymcp
```

### If installed with pipx

```bash
pipx upgrade easymcp
```

### If installed from source

```bash
cd easymcp
git pull
pip install -e .
```

## Uninstalling

### If installed with pip

```bash
pip uninstall easymcp
```

### If installed with pipx

```bash
pipx uninstall easymcp
```

### If installed from source

```bash
pip uninstall easymcp
```

## Troubleshooting

### Command not found

If you get a "command not found" error, ensure that:

1. Python's bin directory is in your PATH
2. For user installs with pip, add `~/.local/bin` to PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

### Permission errors

On Linux/macOS, if you get permission errors:

```bash
# Use --user flag for user-level install
pip install --user easymcp

# Or use a virtual environment (recommended)
python -m venv easymcp-env
source easymcp-env/bin/activate
pip install easymcp
```

### Import errors

If you get import errors after installation:

1. Ensure you're using Python 3.9 or higher:
   ```bash
   python --version
   ```

2. Check that dependencies are installed:
   ```bash
   pip list | grep -E "pyyaml|textual|click|psutil"
   ```

3. Try reinstalling:
   ```bash
   pip uninstall easymcp
   pip install easymcp
   ```

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Paths use backslashes (`\`) instead of forward slashes (`/`)
- Some MCP servers may require Windows Subsystem for Linux (WSL)

### macOS

- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

### Linux

- Some distributions may require additional packages:
  ```bash
  # Debian/Ubuntu
  sudo apt-get install python3-dev

  # Fedora/RHEL
  sudo dnf install python3-devel

  # Arch
  sudo pacman -S python
  ```

## Development Setup

For contributing to easymcp:

```bash
# Clone and enter directory
git clone https://github.com/mbomoore/easymcp.git
cd easymcp

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Format code
ruff format .
```

## Getting Help

If you encounter issues:

1. Check the [documentation](../README.md)
2. Search [existing issues](https://github.com/mbomoore/easymcp/issues)
3. Create a [new issue](https://github.com/mbomoore/easymcp/issues/new) with:
   - Your operating system and version
   - Python version (`python --version`)
   - easymcp version (`easymcp --version`)
   - Full error message
   - Steps to reproduce
