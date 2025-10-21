# Contributing to easymcp

Thank you for your interest in contributing to easymcp! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/mbomoore/easymcp/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, easymcp version)
   - Any relevant logs or screenshots

### Suggesting Features

1. Check [existing feature requests](https://github.com/mbomoore/easymcp/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach (optional)

### Contributing Code

1. **Fork the repository**
   ```bash
   gh repo fork mbomoore/easymcp
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/easymcp.git
   cd easymcp
   ```

3. **Set up development environment**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

5. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

6. **Run tests and linting**
   ```bash
   # Run tests
   pytest

   # Run linter
   ruff check .

   # Format code
   ruff format .
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `test:` for tests
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Create a Pull Request**
   - Go to the [original repository](https://github.com/mbomoore/easymcp)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template
   - Link related issues

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

Example:
```python
def start_server(server_name: str, timeout: int = 30) -> bool:
    """Start a server by name.
    
    Args:
        server_name: Name of the server to start
        timeout: Maximum time to wait for startup
    
    Returns:
        True if server started successfully, False otherwise
    """
    # Implementation
    pass
```

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

Example:
```python
def test_start_server_success(manager):
    """Test successfully starting a server."""
    result = manager.start("test-server")
    assert result is True
    assert manager.is_running("test-server")
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions/classes
- Update relevant docs/ files
- Include examples in documentation
- Keep changelog updated

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for server health checks

- Implement periodic health check polling
- Add health status to server status output
- Add configuration option for check interval

Closes #123
```

## Project Structure

```
easymcp/
├── src/easymcp/          # Main package
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # CLI commands
│   ├── config.py         # Configuration management
│   ├── manager.py        # Server process management
│   └── tui.py            # Terminal UI
├── tests/                # Test files
│   ├── test_config.py
│   └── test_manager.py
├── docs/                 # Documentation
├── examples/             # Example configurations
└── pyproject.toml        # Project metadata and dependencies
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=easymcp --cov-report=html

# Run with verbose output
pytest -v
```

## Linting and Formatting

```bash
# Check code style
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

## Building Documentation

```bash
# If using mkdocs (future enhancement)
mkdocs serve
mkdocs build
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `src/easymcp/__init__.py`
2. Update CHANGELOG.md
3. Create a git tag
4. Push tag to trigger release workflow
5. Publish to PyPI

## Questions?

- Join discussions on [GitHub Discussions](https://github.com/mbomoore/easymcp/discussions)
- Ask in issue comments
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:
- CHANGELOG.md
- README.md contributors section
- Release notes

Thank you for contributing to easymcp! 🎉
