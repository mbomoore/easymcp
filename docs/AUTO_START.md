# Auto-Start on Login

easymcp supports automatic server startup when you log in to your system. This is useful for servers that you want to always be running.

## Configuration

To enable auto-start for a server or bundle, set the `auto_start` field to `true` in your `easymcp.yaml`:

### Server Auto-Start

```yaml
servers:
  my-server:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    auto_start: true  # This server will start automatically
```

### Bundle Auto-Start

```yaml
bundles:
  production:
    servers:
      - server1
      - server2
    auto_start: true  # All servers in this bundle will start automatically
```

## Platform-Specific Setup

### Linux (systemd)

Create a systemd user service file at `~/.config/systemd/user/easymcp.service`:

```ini
[Unit]
Description=easymcp MCP Server Manager
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/easymcp start --all
ExecStop=/usr/local/bin/easymcp stop --all
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

Then enable and start the service:

```bash
systemctl --user daemon-reload
systemctl --user enable easymcp
systemctl --user start easymcp
```

To check status:

```bash
systemctl --user status easymcp
```

### Linux (cron)

Add to your crontab (`crontab -e`):

```bash
@reboot /usr/local/bin/easymcp start --all
```

### macOS (launchd)

Create a launchd plist file at `~/Library/LaunchAgents/com.easymcp.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.easymcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/easymcp</string>
        <string>start</string>
        <string>--all</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/easymcp.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/easymcp.err</string>
</dict>
</plist>
```

Load the service:

```bash
launchctl load ~/Library/LaunchAgents/com.easymcp.plist
```

To unload:

```bash
launchctl unload ~/Library/LaunchAgents/com.easymcp.plist
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create a new Basic Task
3. Name it "easymcp Auto-Start"
4. Trigger: "When I log on"
5. Action: "Start a program"
6. Program/script: `easymcp`
7. Arguments: `start --all`
8. Finish the wizard

Alternatively, use PowerShell:

```powershell
$action = New-ScheduledTaskAction -Execute "easymcp" -Argument "start --all"
$trigger = New-ScheduledTaskTrigger -AtLogon
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "easymcp Auto-Start" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

## Starting Only Auto-Start Enabled Servers

To start only servers or bundles with `auto_start: true`:

```bash
# Start all auto-start servers
easymcp start --auto

# Start specific bundle marked for auto-start
easymcp start --bundle production
```

## Best Practices

1. **Test before enabling**: Start servers manually first to ensure they work correctly
2. **Monitor resources**: Auto-start servers consume system resources - monitor CPU and memory usage
3. **Log rotation**: Set up log rotation for long-running servers to prevent disk space issues
4. **Graceful shutdown**: Ensure your system properly stops servers on shutdown/restart
5. **Error handling**: Configure restart policies to handle temporary failures

## Troubleshooting

### Servers not starting on login

1. Check that easymcp is in your PATH
2. Verify the configuration file location is accessible
3. Check system logs for errors
4. Test manual start: `easymcp start --all`

### Permission issues

Ensure the user running easymcp has:
- Read access to configuration files
- Write access to log directories (`~/.local/state/easymcp/`)
- Execute permissions for server commands

### Checking auto-start status

```bash
# View all servers and their auto-start status
easymcp list

# Check if servers are running
easymcp status
```
