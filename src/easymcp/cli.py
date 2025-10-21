"""CLI interface for easymcp."""

import sys
from pathlib import Path
from typing import Optional

import click

from . import __version__
from .config import Config
from .manager import ServerManager


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
@click.pass_context
def cli(ctx, config: Optional[Path]):
    """easymcp - Lightweight manager for Model Context Protocol servers.
    
    Manage multiple MCP servers from a single YAML file, auto-generate
    mcp.json configs for VS Code, Claude Code, and Copilot, and register
    bundles to auto-launch on login.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config(config)
    ctx.obj["manager"] = ServerManager(ctx.obj["config"])


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize a new easymcp configuration file."""
    config_path = Path.cwd() / "easymcp.yaml"
    
    if config_path.exists():
        click.echo(f"Configuration file already exists: {config_path}")
        return
    
    # Create example configuration
    example_config = """# easymcp configuration file
# Define your MCP servers and bundles here

servers:
  # Example server configuration
  example-server:
    command: "node"
    args: ["path/to/server.js"]
    env:
      API_KEY: "your-api-key"
    cwd: null
    auto_start: false

bundles:
  # Example bundle configuration
  development:
    servers:
      - example-server
    auto_start: false
"""
    
    with open(config_path, "w") as f:
        f.write(example_config)
    
    click.echo(f"Created configuration file: {config_path}")
    click.echo("\nEdit the file to add your MCP servers and run 'easymcp start' to begin.")


@cli.command()
@click.argument("server_name", required=False)
@click.option("--all", "-a", is_flag=True, help="Start all servers")
@click.option("--bundle", "-b", help="Start all servers in a bundle")
@click.pass_context
def start(ctx, server_name: Optional[str], all: bool, bundle: Optional[str]):
    """Start one or more MCP servers."""
    manager: ServerManager = ctx.obj["manager"]
    config: Config = ctx.obj["config"]
    
    if not config.servers and not bundle:
        click.echo("No servers configured. Run 'easymcp init' to create a configuration file.")
        sys.exit(1)
    
    if all:
        click.echo("Starting all servers...")
        results = manager.start_all()
        for name, success in results.items():
            if success:
                click.echo(f"  ✓ {name} started")
            else:
                click.echo(f"  ✗ {name} failed to start or already running")
    elif bundle:
        click.echo(f"Starting bundle '{bundle}'...")
        try:
            results = manager.start_bundle(bundle)
            for name, success in results.items():
                if success:
                    click.echo(f"  ✓ {name} started")
                else:
                    click.echo(f"  ✗ {name} failed to start or already running")
        except ValueError as e:
            click.echo(f"Error: {e}")
            sys.exit(1)
    elif server_name:
        if manager.start(server_name):
            click.echo(f"Started server: {server_name}")
        else:
            click.echo(f"Failed to start server: {server_name} (may already be running)")
    else:
        click.echo("Please specify a server name, --all, or --bundle")
        sys.exit(1)


@cli.command()
@click.argument("server_name", required=False)
@click.option("--all", "-a", is_flag=True, help="Stop all servers")
@click.option("--bundle", "-b", help="Stop all servers in a bundle")
@click.pass_context
def stop(ctx, server_name: Optional[str], all: bool, bundle: Optional[str]):
    """Stop one or more MCP servers."""
    manager: ServerManager = ctx.obj["manager"]
    config: Config = ctx.obj["config"]
    
    if all:
        click.echo("Stopping all servers...")
        results = manager.stop_all()
        for name, success in results.items():
            if success:
                click.echo(f"  ✓ {name} stopped")
            else:
                click.echo(f"  ✗ {name} not running or failed to stop")
    elif bundle:
        click.echo(f"Stopping bundle '{bundle}'...")
        try:
            results = manager.stop_bundle(bundle)
            for name, success in results.items():
                if success:
                    click.echo(f"  ✓ {name} stopped")
                else:
                    click.echo(f"  ✗ {name} not running or failed to stop")
        except ValueError as e:
            click.echo(f"Error: {e}")
            sys.exit(1)
    elif server_name:
        if manager.stop(server_name):
            click.echo(f"Stopped server: {server_name}")
        else:
            click.echo(f"Server not running: {server_name}")
    else:
        click.echo("Please specify a server name, --all, or --bundle")
        sys.exit(1)


@cli.command()
@click.argument("server_name")
@click.pass_context
def restart(ctx, server_name: str):
    """Restart an MCP server."""
    manager: ServerManager = ctx.obj["manager"]
    
    if manager.restart(server_name):
        click.echo(f"Restarted server: {server_name}")
    else:
        click.echo(f"Failed to restart server: {server_name}")
        sys.exit(1)


@cli.command()
@click.argument("server_name", required=False)
@click.pass_context
def status(ctx, server_name: Optional[str]):
    """Show status of MCP servers."""
    manager: ServerManager = ctx.obj["manager"]
    config: Config = ctx.obj["config"]
    
    if not config.servers:
        click.echo("No servers configured.")
        return
    
    if server_name:
        status = manager.get_status(server_name)
        _print_server_status(status)
    else:
        statuses = manager.get_all_statuses()
        if not statuses:
            click.echo("No servers configured.")
            return
        
        click.echo("Server Status:")
        click.echo("-" * 80)
        for status in statuses:
            _print_server_status(status, compact=True)


def _print_server_status(status, compact=False):
    """Print server status."""
    if compact:
        if status.running:
            uptime_str = _format_uptime(status.uptime) if status.uptime else "N/A"
            mem_str = f"{status.memory_mb:.1f}MB" if status.memory_mb else "N/A"
            cpu_str = f"{status.cpu_percent:.1f}%" if status.cpu_percent else "N/A"
            click.echo(
                f"  {status.name:20s} ✓ Running  PID: {status.pid:6d}  "
                f"Uptime: {uptime_str:10s}  Mem: {mem_str:8s}  CPU: {cpu_str}"
            )
        else:
            click.echo(f"  {status.name:20s} ✗ Stopped")
    else:
        click.echo(f"\nServer: {status.name}")
        click.echo(f"  Status: {'✓ Running' if status.running else '✗ Stopped'}")
        if status.running:
            click.echo(f"  PID: {status.pid}")
            if status.uptime:
                click.echo(f"  Uptime: {_format_uptime(status.uptime)}")
            if status.memory_mb:
                click.echo(f"  Memory: {status.memory_mb:.1f} MB")
            if status.cpu_percent:
                click.echo(f"  CPU: {status.cpu_percent:.1f}%")


def _format_uptime(seconds: float) -> str:
    """Format uptime in human-readable format."""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


@cli.command()
@click.pass_context
def list(ctx):
    """List configured servers and bundles."""
    config: Config = ctx.obj["config"]
    
    if config.servers:
        click.echo("Configured Servers:")
        for name, server in config.servers.items():
            auto_start = " (auto-start)" if server.auto_start else ""
            click.echo(f"  - {name}{auto_start}")
            click.echo(f"    Command: {server.command} {' '.join(server.args)}")
    else:
        click.echo("No servers configured.")
    
    click.echo()
    
    if config.bundles:
        click.echo("Configured Bundles:")
        for name, bundle in config.bundles.items():
            auto_start = " (auto-start)" if bundle.auto_start else ""
            click.echo(f"  - {name}{auto_start}")
            click.echo(f"    Servers: {', '.join(bundle.servers)}")
    else:
        click.echo("No bundles configured.")


@cli.command()
@click.argument("server_name")
@click.option("--lines", "-n", default=50, help="Number of lines to show")
@click.option("--follow", "-f", is_flag=True, help="Follow log output")
@click.pass_context
def logs(ctx, server_name: str, lines: int, follow: bool):
    """Show logs for an MCP server."""
    manager: ServerManager = ctx.obj["manager"]
    
    if follow:
        click.echo(f"Following logs for {server_name} (Ctrl+C to exit)...")
        log_file = manager._get_log_file(server_name)
        
        if not log_file.exists():
            click.echo("No logs available.")
            return
        
        # Show existing logs first
        log_content = manager.get_logs(server_name, lines)
        if log_content:
            click.echo(log_content, nl=False)
        
        # Follow new logs
        try:
            import time
            with open(log_file, "r") as f:
                # Go to end of file
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        click.echo(line, nl=False)
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            click.echo("\nStopped following logs.")
    else:
        log_content = manager.get_logs(server_name, lines)
        if log_content:
            click.echo(log_content, nl=False)
        else:
            click.echo("No logs available.")


@cli.command()
@click.option(
    "--target",
    "-t",
    type=click.Choice(["vscode", "claude", "copilot"]),
    default="vscode",
    help="Target tool for mcp.json",
)
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
@click.pass_context
def export(ctx, target: str, output: Optional[Path]):
    """Export mcp.json configuration for VS Code, Claude, or Copilot."""
    config: Config = ctx.obj["config"]
    
    if not config.servers:
        click.echo("No servers configured.")
        sys.exit(1)
    
    try:
        output_path = config.export_mcp_json(target, output)
        click.echo(f"Exported {target} configuration to: {output_path}")
    except Exception as e:
        click.echo(f"Error exporting configuration: {e}")
        sys.exit(1)


@cli.command()
@click.pass_context
def tui(ctx):
    """Launch the interactive Text User Interface."""
    try:
        from .tui import EasyMCPApp
        
        config: Config = ctx.obj["config"]
        app = EasyMCPApp(config)
        app.run()
    except ImportError:
        click.echo("TUI dependencies not available. Please install textual.")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error launching TUI: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    cli(obj={})


if __name__ == "__main__":
    main()
