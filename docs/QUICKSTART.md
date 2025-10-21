# Quick Start Guide

Get up and running with easymcp in 5 minutes!

## 1. Install easymcp

Choose your preferred installation method:

**Option A: Using uvx (fastest, no installation)**
```bash
uvx easymcp --help
```

**Option B: Using pip**
```bash
pip install easymcp
```

## 2. Create Your First Configuration

Initialize a configuration file in your current directory:

```bash
easymcp init
```

This creates `easymcp.yaml` with example configuration.

## 3. Configure Your Servers

Edit `easymcp.yaml` to add your MCP servers. Here's a simple example:

```yaml
servers:
  # Filesystem server - provides file access
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    
  # GitHub server - provides GitHub integration
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN: "your-github-personal-access-token"

bundles:
  # Group servers for easy management
  development:
    servers:
      - filesystem
      - github
```

## 4. Start Your Servers

Start all configured servers:

```bash
easymcp start --all
```

Or start specific servers:

```bash
easymcp start filesystem
```

Or start a bundle:

```bash
easymcp start --bundle development
```

## 5. Check Server Status

View the status of your servers:

```bash
easymcp status
```

Output:
```
Server Status:
--------------------------------------------------------------------------------
  filesystem           ✓ Running  PID:  12345  Uptime: 2m 30s     Mem: 45.2MB    CPU: 1.2%
  github               ✓ Running  PID:  12346  Uptime: 2m 30s     Mem: 52.1MB    CPU: 0.8%
```

## 6. (Optional) Try the TUI

Launch the interactive terminal UI:

```bash
easymcp tui
```

Features:
- Real-time server status
- Start/stop servers with keyboard shortcuts
- View detailed information
- Export configurations

## Common Commands

```bash
# List all configured servers and bundles
easymcp list

# View logs for a server
easymcp logs filesystem

# Follow logs in real-time
easymcp logs filesystem --follow

# Stop a server
easymcp stop filesystem

# Stop all servers
easymcp stop --all

# Restart a server
easymcp restart filesystem

# Export configuration for VS Code
easymcp export --target vscode

# Export for Claude or Copilot
easymcp export --target claude
easymcp export --target copilot
```

## Example Configurations

### Minimal Configuration

```yaml
servers:
  myserver:
    command: "node"
    args: ["server.js"]
```

### With Environment Variables

```yaml
servers:
  api:
    command: "python"
    args: ["-m", "api_server"]
    env:
      API_KEY: "your-api-key"
      DEBUG: "true"
```

### With Working Directory

```yaml
servers:
  webapp:
    command: "npm"
    args: ["start"]
    cwd: "/path/to/webapp"
```

### With Auto-Start

```yaml
servers:
  daemon:
    command: "python"
    args: ["-m", "daemon"]
    auto_start: true
```

### Multiple Servers with Bundles

```yaml
servers:
  frontend:
    command: "npm"
    args: ["run", "dev"]
    cwd: "/projects/frontend"
    
  backend:
    command: "python"
    args: ["-m", "backend"]
    cwd: "/projects/backend"
    env:
      DATABASE_URL: "postgresql://localhost/db"
    
  database:
    command: "docker"
    args: ["start", "postgres"]

bundles:
  fullstack:
    servers:
      - database
      - backend
      - frontend
```

## IDE Integration

Export your configuration for your preferred IDE:

### VS Code

```bash
easymcp export --target vscode
```

This creates `~/.vscode/mcp.json` with your server configuration.

### Claude Code

```bash
easymcp export --target claude
```

Creates `~/.claude/mcp.json`.

### GitHub Copilot

```bash
easymcp export --target copilot
```

Creates `~/.copilot/mcp.json`.

## Troubleshooting

### Servers won't start

1. Check configuration syntax:
   ```bash
   easymcp list
   ```

2. Verify command is correct:
   ```bash
   # Test the command manually
   node server.js
   ```

3. Check logs:
   ```bash
   easymcp logs myserver
   ```

### Can't find easymcp command

Add Python's bin directory to PATH:

```bash
# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"

# Or use full path
python -m easymcp.cli --help
```

### Configuration file not found

easymcp looks for configuration in:
1. Current directory: `./easymcp.yaml`
2. User config: `~/.config/easymcp/easymcp.yaml`

Or specify a custom location:
```bash
easymcp --config /path/to/config.yaml start
```

## Next Steps

- Read the full [README](../README.md)
- Check [example configurations](../examples/)
- Set up [auto-start on login](AUTO_START.md)
- Learn about [advanced features](../README.md#features-in-detail)

## Getting Help

- [Documentation](../README.md)
- [GitHub Issues](https://github.com/mbomoore/easymcp/issues)
- [GitHub Discussions](https://github.com/mbomoore/easymcp/discussions)

Happy MCP server managing! 🚀
