# Changelog

All notable changes to easymcp will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-21

### Added

- Initial release of easymcp
- CLI commands: `init`, `start`, `stop`, `restart`, `status`, `list`, `logs`, `export`, `tui`
- YAML-based configuration for servers and bundles
- Server process management with PID tracking
- Process monitoring (CPU, memory, uptime)
- Server logs with real-time following
- Bundle support for managing groups of servers
- Auto-generation of mcp.json for VS Code, Claude Code, and GitHub Copilot
- Interactive Textual TUI with real-time updates
- Support for environment variables and working directories
- Auto-start configuration for servers and bundles
- Graceful server shutdown with configurable timeout
- Comprehensive documentation and examples
- Example configuration files
- Unit tests for core functionality

### Features

#### CLI
- `easymcp init` - Initialize configuration file
- `easymcp start [SERVER|--all|--bundle NAME]` - Start servers
- `easymcp stop [SERVER|--all|--bundle NAME]` - Stop servers
- `easymcp restart SERVER` - Restart a server
- `easymcp status [SERVER]` - Show server status
- `easymcp list` - List configured servers and bundles
- `easymcp logs SERVER [-n LINES] [--follow]` - View server logs
- `easymcp export [--target vscode|claude|copilot]` - Export mcp.json
- `easymcp tui` - Launch interactive TUI

#### Configuration
- YAML-based server configuration
- Bundle support for grouping servers
- Environment variable support
- Custom working directory per server
- Auto-start flag for servers and bundles
- Multiple configuration file locations

#### Process Management
- Background process execution
- PID file tracking
- Graceful shutdown with timeout
- Process health monitoring
- CPU and memory usage tracking
- Uptime tracking

#### IDE Integration
- Auto-generate mcp.json for VS Code
- Auto-generate mcp.json for Claude Code
- Auto-generate mcp.json for GitHub Copilot
- Configurable output paths

#### TUI
- Real-time server status updates
- Interactive server control
- Start/stop individual or all servers
- Export configurations from UI
- Keyboard shortcuts for common actions

### Documentation
- Comprehensive README with examples
- Installation guide
- Auto-start/login integration guide
- Contributing guidelines
- Example configurations

[0.1.0]: https://github.com/mbomoore/easymcp/releases/tag/v0.1.0
