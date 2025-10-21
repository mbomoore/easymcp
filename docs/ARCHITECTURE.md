# Architecture Overview

This document provides an overview of easymcp's architecture and how components interact.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          easymcp CLI/TUI                            │
│                                                                     │
│  User Interfaces:                                                   │
│  ┌──────────────┐              ┌──────────────┐                    │
│  │     CLI      │              │     TUI      │                    │
│  │  (cli.py)    │              │  (tui.py)    │                    │
│  │              │              │              │                    │
│  │ - init       │              │ - Real-time  │                    │
│  │ - start/stop │              │   status     │                    │
│  │ - status     │              │ - Interactive│                    │
│  │ - logs       │              │   control    │                    │
│  │ - export     │              │ - Keyboard   │                    │
│  └──────┬───────┘              │   shortcuts  │                    │
│         │                      └──────┬───────┘                    │
│         │                             │                             │
│         └─────────────┬───────────────┘                             │
│                       │                                             │
│              ┌────────▼────────┐                                    │
│              │  Core Logic     │                                    │
│              │                 │                                    │
│              │ ┌─────────────┐ │                                    │
│              │ │   Config    │ │                                    │
│              │ │ (config.py) │ │                                    │
│              │ │             │ │                                    │
│              │ │ - YAML I/O  │ │                                    │
│              │ │ - Servers   │ │                                    │
│              │ │ - Bundles   │ │                                    │
│              │ │ - Export    │ │                                    │
│              │ └──────┬──────┘ │                                    │
│              │        │        │                                    │
│              │ ┌──────▼──────┐ │                                    │
│              │ │   Manager   │ │                                    │
│              │ │(manager.py) │ │                                    │
│              │ │             │ │                                    │
│              │ │ - Start/Stop│ │                                    │
│              │ │ - Monitor   │ │                                    │
│              │ │ - Logs      │ │                                    │
│              │ │ - PIDs      │ │                                    │
│              │ └──────┬──────┘ │                                    │
│              └─────────┼────────┘                                    │
│                        │                                             │
└────────────────────────┼─────────────────────────────────────────────┘
                         │
                         │ Process Management
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐     ┌───▼────┐     ┌───▼────┐
    │ Server  │     │ Server │     │ Server │
    │    1    │     │    2   │     │    3   │
    │         │     │        │     │        │
    │ (PID)   │     │ (PID)  │     │ (PID)  │
    └────┬────┘     └───┬────┘     └───┬────┘
         │              │              │
         └──────┬───────┴──────┬───────┘
                │              │
            ┌───▼───┐      ┌───▼───┐
            │  Logs │      │ State │
            │ Files │      │ Files │
            └───────┘      └───────┘
```

## Component Responsibilities

### CLI (`cli.py`)
- Command-line interface
- Argument parsing (Click)
- User input/output
- Help system
- Command routing

### TUI (`tui.py`)
- Interactive terminal UI (Textual)
- Real-time status updates
- Keyboard event handling
- Visual table display
- User notifications

### Config (`config.py`)
- YAML file parsing
- Server configuration management
- Bundle configuration management
- mcp.json generation
- Configuration validation

### Manager (`manager.py`)
- Process lifecycle management
- PID file tracking
- Process monitoring (psutil)
- Log file management
- Health status collection

## Data Flow

### Starting a Server

```
User Command
    │
    ▼
easymcp start <server>
    │
    ▼
CLI.start()
    │
    ▼
Manager.start(server_name)
    │
    ├──▶ Load Config
    ├──▶ Check if Running
    ├──▶ Build Command
    ├──▶ Set Environment
    ├──▶ Start Process (subprocess)
    ├──▶ Save PID
    └──▶ Return Status
```

### Monitoring Status

```
User Command
    │
    ▼
easymcp status
    │
    ▼
CLI.status()
    │
    ▼
Manager.get_all_statuses()
    │
    ├──▶ For each server:
    │   ├──▶ Load PID
    │   ├──▶ Check Process (psutil)
    │   ├──▶ Get CPU/Memory
    │   ├──▶ Calculate Uptime
    │   └──▶ Build Status Object
    │
    └──▶ Return Status List
        │
        ▼
    Display Results
```

### Exporting Configuration

```
User Command
    │
    ▼
easymcp export --target vscode
    │
    ▼
CLI.export()
    │
    ▼
Config.export_mcp_json(target)
    │
    ├──▶ Generate JSON Structure
    │   ├──▶ For each server:
    │   │   ├──▶ Build command entry
    │   │   ├──▶ Add arguments
    │   │   ├──▶ Add environment
    │   │   └──▶ Add working dir
    │   └──▶ Format for target
    │
    └──▶ Write to File
        │
        ▼
    ~/.vscode/mcp.json
```

## File System Layout

### Runtime State

```
~/.local/state/easymcp/
├── server1.pid        # PID and start time
├── server1.log        # Server logs
├── server2.pid
├── server2.log
└── ...
```

### Configuration

```
~/.config/easymcp/
└── easymcp.yaml       # Main config

OR

./easymcp.yaml         # Project-local config
```

### IDE Integration

```
~/.vscode/
└── mcp.json          # VS Code config

~/.claude/
└── mcp.json          # Claude config

~/.copilot/
└── mcp.json          # Copilot config
```

## Process Model

### Server Lifecycle

```
[Configured] ──start──▶ [Starting] ──success──▶ [Running]
     ▲                      │                       │
     │                  failure                  stop/crash
     │                      │                       │
     └──────────────────────┴───────────────────────┘
```

### Process Management

```
easymcp ──fork──▶ Server Process
   │                  │
   │                  ├──▶ STDOUT/STDERR ──▶ Log File
   │                  │
   │                  └──▶ PID ──▶ PID File
   │
   └──monitor──▶ psutil.Process(PID)
                     ├──▶ CPU usage
                     ├──▶ Memory usage
                     ├──▶ Status
                     └──▶ Uptime
```

## Key Design Decisions

### 1. Stateless CLI
- Each command loads fresh state
- No daemon process required
- Simpler architecture
- Better for automation

### 2. PID File Based
- Simple process tracking
- Survives CLI restarts
- Standard Unix pattern
- Easy to debug

### 3. YAML Configuration
- Human-readable
- Easy to version control
- Simple structure
- Extensible

### 4. Separate Logs
- Per-server log files
- Easy to follow individual servers
- No log mixing
- Simple log rotation

### 5. Background Processes
- Servers run independently
- CLI can exit
- Servers survive reboots (with auto-start)
- No process tree issues

## Extension Points

### Adding New Commands

1. Add function to `cli.py`
2. Decorate with `@cli.command()`
3. Use existing manager methods
4. Follow error handling pattern

### Adding New Features to Manager

1. Add method to `Manager` class
2. Use existing PID/log infrastructure
3. Handle errors gracefully
4. Update tests

### Supporting New IDE Formats

1. Add case to `Config.generate_mcp_json()`
2. Return appropriate JSON structure
3. Update export command
4. Add documentation

## Performance Characteristics

### Startup Time
- CLI initialization: < 100ms
- Config loading: < 50ms
- Process start: depends on server

### Memory Usage
- CLI: ~20-30 MB
- TUI: ~30-40 MB
- Per server: depends on server

### Monitoring Overhead
- Status check: ~10ms per server
- Log read: depends on log size
- Real-time TUI: updates every 2 seconds

## Security Considerations

### Process Isolation
- Each server runs in own process
- User-level permissions
- No privilege escalation
- Process containment

### Credential Management
- Environment variables per server
- Not logged
- Not exposed in process list (careful!)
- Config file permissions

### State File Security
- PID files: world-readable (process IDs are public)
- Log files: user-readable only
- Config files: user's responsibility

## Testing Strategy

### Unit Tests
- Config loading/saving
- Server configuration
- JSON generation
- Manager operations (with mocks)

### Integration Tests
- Full command execution
- Multi-server scenarios
- Bundle operations
- File system operations

### Manual Testing
- Cross-platform validation
- Real server execution
- TUI interaction
- Error scenarios

## Future Enhancements

Potential architectural changes:

1. **Optional Daemon Mode**
   - Background service
   - WebSocket API
   - Remote management

2. **Plugin System**
   - Custom commands
   - Event hooks
   - Extension points

3. **Health Checks**
   - HTTP endpoints
   - Custom scripts
   - Auto-restart on failure

4. **Metrics Collection**
   - Time-series data
   - Graphing
   - Alerting

## Summary

easymcp uses a simple, stateless architecture with:
- Clear separation of concerns
- Standard Unix patterns (PIDs, logs)
- Minimal dependencies
- Easy to understand and maintain
- Extensible design
