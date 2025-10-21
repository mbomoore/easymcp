# easymcp

**A lightweight Python CLI and Textual TUI for managing Model Context Protocol servers**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

easymcp is your one-stop solution for managing Model Context Protocol (MCP) servers. It provides:

- 🚀 **Simple CLI** - Install, start, stop, and monitor multiple MCP servers
- 📋 **YAML Configuration** - Manage all servers from a single, easy-to-read file
- 🔄 **Auto-generation** - Create mcp.json configs for VS Code, Claude Code, and Copilot
- 📦 **Bundles** - Group servers together and manage them as a unit
- 🖥️ **Interactive TUI** - Beautiful terminal UI built with Textual
- ⚡ **Auto-launch** - Register bundles to start on login
- 🔓 **Open Source** - MIT licensed, portable, and community-driven

## Installation

Install easymcp as a tool with [uvx](https://docs.astral.sh/uv/):

```bash
uvx easymcp
```

Or install with pip:

```bash
pip install easymcp
```

Or install from source:

```bash
git clone https://github.com/mbomoore/easymcp.git
cd easymcp
pip install -e .
```

For detailed installation instructions, see [INSTALLATION.md](docs/INSTALLATION.md).

## Quick Start

1. **Initialize a configuration file:**

```bash
easymcp init
```

2. **Edit `easymcp.yaml` to add your MCP servers:**

```yaml
servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN: "your-token"

bundles:
  development:
    servers:
      - filesystem
      - github
```

3. **Start your servers:**

```bash
# Start a single server
easymcp start filesystem

# Start a bundle
easymcp start --bundle development

# Start all servers
easymcp start --all
```

4. **Monitor your servers:**

```bash
# Check status
easymcp status

# View logs
easymcp logs filesystem

# Launch the TUI
easymcp tui
```

For more details, see the [Quick Start Guide](docs/QUICKSTART.md).

## Commands

### `easymcp init`

Create a new configuration file with example servers and bundles.

### `easymcp start [SERVER_NAME]`

Start one or more servers:

```bash
easymcp start filesystem          # Start a specific server
easymcp start --bundle dev        # Start all servers in a bundle
easymcp start --all               # Start all configured servers
```

### `easymcp stop [SERVER_NAME]`

Stop one or more servers:

```bash
easymcp stop filesystem           # Stop a specific server
easymcp stop --bundle dev         # Stop all servers in a bundle
easymcp stop --all                # Stop all running servers
```

### `easymcp restart SERVER_NAME`

Restart a server:

```bash
easymcp restart filesystem
```

### `easymcp status [SERVER_NAME]`

Show status of servers:

```bash
easymcp status                    # Show all servers
easymcp status filesystem         # Show specific server
```

### `easymcp list`

List all configured servers and bundles.

### `easymcp logs SERVER_NAME`

View server logs:

```bash
easymcp logs filesystem           # Show last 50 lines
easymcp logs filesystem -n 100    # Show last 100 lines
easymcp logs filesystem --follow  # Follow logs in real-time
```

### `easymcp export`

Export mcp.json configuration for IDE integration:

```bash
easymcp export --target vscode    # Export for VS Code
easymcp export --target claude    # Export for Claude Code
easymcp export --target copilot   # Export for GitHub Copilot
easymcp export -o custom.json     # Export to custom path
```

### `easymcp tui`

Launch the interactive Text User Interface for visual server management.

## Auto-Start on Login

easymcp supports automatic server startup when you log in. Configure servers or bundles with `auto_start: true` and set up platform-specific integration.

For detailed setup instructions, see [AUTO_START.md](docs/AUTO_START.md).

## Configuration

The configuration file (`easymcp.yaml`) defines your servers and bundles:

### Server Configuration

```yaml
servers:
  server-name:
    command: "command-to-run"       # Required: Command to execute
    args: ["arg1", "arg2"]          # Optional: Command arguments
    env:                             # Optional: Environment variables
      KEY: "value"
    cwd: "/working/directory"        # Optional: Working directory
    auto_start: false                # Optional: Auto-start on login
```

### Bundle Configuration

```yaml
bundles:
  bundle-name:
    servers:                         # List of servers in this bundle
      - server1
      - server2
    auto_start: false                # Optional: Auto-start on login
```

## Configuration File Locations

easymcp looks for configuration files in the following locations (in order):

1. Current directory: `./easymcp.yaml`
2. User config: `~/.config/easymcp/easymcp.yaml`

You can also specify a custom location:

```bash
easymcp --config /path/to/config.yaml start
```

## IDE Integration

easymcp can generate mcp.json configuration files for various IDEs:

### VS Code

```bash
easymcp export --target vscode
```

Generates: `~/.vscode/mcp.json`

### Claude Code

```bash
easymcp export --target claude
```

Generates: `~/.claude/mcp.json`

### GitHub Copilot

```bash
easymcp export --target copilot
```

Generates: `~/.copilot/mcp.json`

## Examples

See the [examples](examples/) directory for sample configurations:

- [easymcp.yaml](examples/easymcp.yaml) - Full-featured example
- [minimal.yaml](examples/minimal.yaml) - Minimal example

## Features in Detail

### Process Management

- Start/stop/restart servers individually or in groups
- Automatic PID tracking and process monitoring
- Graceful shutdown with configurable timeout
- Process health monitoring (CPU, memory, uptime)

### Logging

- Centralized log management for all servers
- Real-time log following with `--follow` flag
- Configurable log retention

### Bundles

- Group related servers together
- Start/stop entire bundles with one command
- Configure bundles to auto-start on system login

### TUI (Text User Interface)

Launch the interactive TUI with `easymcp tui`:

- Real-time server status updates
- Start/stop servers with keyboard shortcuts
- View server details at a glance
- Export configurations from the UI

Keyboard shortcuts:
- `s` - Start selected server
- `t` - Stop selected server
- `a` - Start all servers
- `z` - Stop all servers
- `r` - Refresh display
- `q` - Quit

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/mbomoore/easymcp.git
cd easymcp

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .
```

### Running Tests

```bash
pytest tests/
```

## Requirements

- Python 3.9 or higher
- PyYAML
- Click
- Textual
- psutil

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Report bugs and request features via [GitHub Issues](https://github.com/mbomoore/easymcp/issues)
- Join discussions on [GitHub Discussions](https://github.com/mbomoore/easymcp/discussions)

## Acknowledgments

Built with:
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [Click](https://click.palletsprojects.com/) - Command-line interface framework
- [PyYAML](https://pyyaml.org/) - YAML parser
- [psutil](https://github.com/giampaolo/psutil) - Process and system utilities

---

Made with ❤️ by the easymcp community
