# Features Overview

easymcp provides a comprehensive set of features for managing Model Context Protocol (MCP) servers.

## Core Features

### 1. **Simple CLI Interface**

Single binary with intuitive commands:
- `init` - Create configuration
- `start/stop/restart` - Control servers
- `status` - Monitor health
- `logs` - View output
- `list` - Show configuration
- `export` - Generate IDE configs
- `tui` - Launch interactive UI

### 2. **YAML Configuration**

Easy-to-read configuration format:
```yaml
servers:
  myserver:
    command: "node"
    args: ["server.js"]
    env:
      API_KEY: "secret"
    cwd: "/path/to/server"
    auto_start: true
```

### 3. **Process Management**

- Background process execution
- PID tracking and monitoring
- Graceful shutdown with timeout
- Auto-restart on failure (via systemd/launchd)
- Process health monitoring (CPU, memory, uptime)

### 4. **Bundle Management**

Group related servers together:
```yaml
bundles:
  development:
    servers:
      - frontend
      - backend
      - database
```

Start/stop entire bundles with one command.

### 5. **IDE Integration**

Auto-generate mcp.json for:
- **VS Code** - `~/.vscode/mcp.json`
- **Claude Code** - `~/.claude/mcp.json`
- **GitHub Copilot** - `~/.copilot/mcp.json`

One command syncs your configuration across all tools.

### 6. **Interactive TUI**

Beautiful terminal UI with:
- Real-time status updates
- Server control with keyboard shortcuts
- Live resource monitoring
- Log viewing
- Configuration export

### 7. **Logging**

- Centralized log management
- Real-time log following
- Configurable retention
- Per-server log files

### 8. **Auto-Start**

Configure servers to start on login:
- systemd integration (Linux)
- launchd integration (macOS)
- Task Scheduler integration (Windows)
- cron support (Unix-like)

## CLI Commands Reference

### Server Management

```bash
# Start servers
easymcp start <server>         # Start single server
easymcp start --all            # Start all servers
easymcp start --bundle <name>  # Start bundle

# Stop servers
easymcp stop <server>          # Stop single server
easymcp stop --all             # Stop all servers
easymcp stop --bundle <name>   # Stop bundle

# Restart server
easymcp restart <server>       # Restart server
```

### Monitoring

```bash
# Check status
easymcp status                 # All servers
easymcp status <server>        # Single server

# View logs
easymcp logs <server>          # Last 50 lines
easymcp logs <server> -n 100   # Last 100 lines
easymcp logs <server> --follow # Follow in real-time
```

### Configuration

```bash
# Initialize
easymcp init                   # Create config file

# List configuration
easymcp list                   # Show servers and bundles

# Export for IDEs
easymcp export --target vscode    # VS Code
easymcp export --target claude    # Claude
easymcp export --target copilot   # Copilot
easymcp export -o custom.json     # Custom path
```

### Interactive UI

```bash
easymcp tui                    # Launch TUI
```

## Configuration Options

### Server Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command` | string | Yes | Command to execute |
| `args` | list | No | Command arguments |
| `env` | dict | No | Environment variables |
| `cwd` | string | No | Working directory |
| `auto_start` | bool | No | Start on login |

### Bundle Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `servers` | list | Yes | List of server names |
| `auto_start` | bool | No | Start bundle on login |

## Advanced Features

### Environment Variables

Set per-server environment:
```yaml
servers:
  api:
    command: "python"
    args: ["-m", "api"]
    env:
      DATABASE_URL: "postgresql://localhost/db"
      API_KEY: "secret"
      DEBUG: "true"
```

### Working Directories

Run servers in specific directories:
```yaml
servers:
  webapp:
    command: "npm"
    args: ["start"]
    cwd: "/projects/webapp"
```

### Multiple Configuration Files

easymcp searches for configuration in:
1. Current directory: `./easymcp.yaml`
2. User config: `~/.config/easymcp/easymcp.yaml`

Or specify custom location:
```bash
easymcp --config /path/to/config.yaml start
```

### Custom Export Paths

Export IDE configs to custom locations:
```bash
easymcp export --target vscode -o /custom/path/mcp.json
```

## Platform Support

### Operating Systems

- **Linux** - Full support (tested on Ubuntu, Debian, Fedora, Arch)
- **macOS** - Full support (tested on macOS 10.15+)
- **Windows** - Full support (tested on Windows 10/11)

### Python Versions

- Python 3.9+
- Tested on 3.9, 3.10, 3.11, 3.12

### Shells

- bash
- zsh
- fish
- PowerShell
- Command Prompt

## Security Features

- No credentials stored in logs
- Process isolation
- User-level permissions
- Graceful shutdown to prevent data loss
- Configurable timeout for safe termination

## Performance

- Minimal resource overhead
- Fast startup (< 100ms)
- Efficient process monitoring
- Configurable polling intervals
- Low memory footprint

## Extensibility

- Plugin-ready architecture
- Custom commands via CLI
- Scriptable via Python API
- Configuration file templating
- Hook points for automation

## Use Cases

1. **Development Environment**
   - Start all development servers with one command
   - Monitor resource usage
   - Quick log access

2. **Production Deployment**
   - Reliable process management
   - Auto-restart on failure
   - Centralized monitoring

3. **CI/CD Integration**
   - Scriptable start/stop
   - Status checking
   - Log retrieval

4. **IDE Integration**
   - Auto-sync MCP configurations
   - Consistent setup across tools
   - Version-controlled config

5. **Team Collaboration**
   - Shared configuration files
   - Consistent environment setup
   - Easy onboarding

## Comparison with Alternatives

| Feature | easymcp | Manual Scripts | Docker Compose | PM2 |
|---------|---------|----------------|----------------|-----|
| Single command | ✓ | ✗ | ✓ | ✓ |
| YAML config | ✓ | ✗ | ✓ | ✓ |
| IDE integration | ✓ | ✗ | ✗ | ✗ |
| Cross-platform | ✓ | ⚠ | ✓ | ⚠ |
| No containers | ✓ | ✓ | ✗ | ✓ |
| Interactive TUI | ✓ | ✗ | ✗ | ✓ |
| Python-based | ✓ | ⚠ | ✗ | ✗ |

## Future Enhancements

Potential features for future releases:
- Web dashboard
- Health check endpoints
- Metrics collection
- Alert notifications
- Plugin system
- Multi-server orchestration
- Container support
- Remote management

## Getting Started

See [QUICKSTART.md](QUICKSTART.md) for a 5-minute introduction to easymcp.

## Documentation

- [README.md](../README.md) - Main documentation
- [INSTALLATION.md](INSTALLATION.md) - Installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [AUTO_START.md](AUTO_START.md) - Auto-start setup
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contributing guide
