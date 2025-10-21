"""Textual TUI interface for easymcp."""

from datetime import datetime
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Label, Static
from textual.timer import Timer

from .config import Config
from .manager import ServerManager, ServerStatus


class ServerStatusWidget(Static):
    """Widget displaying server status information."""

    def __init__(self, status: ServerStatus) -> None:
        super().__init__()
        self.status = status

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        status_icon = "✓" if self.status.running else "✗"
        status_text = "Running" if self.status.running else "Stopped"
        status_class = "running" if self.status.running else "stopped"

        yield Label(f"{status_icon} {self.status.name}", classes="server-name")
        yield Label(status_text, classes=f"status {status_class}")

        if self.status.running:
            if self.status.pid:
                yield Label(f"PID: {self.status.pid}")
            if self.status.uptime:
                uptime_str = self._format_uptime(self.status.uptime)
                yield Label(f"Uptime: {uptime_str}")
            if self.status.memory_mb:
                yield Label(f"Memory: {self.status.memory_mb:.1f} MB")
            if self.status.cpu_percent:
                yield Label(f"CPU: {self.status.cpu_percent:.1f}%")

    @staticmethod
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


class EasyMCPApp(App):
    """Textual TUI application for easymcp."""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #server-table {
        width: 100%;
        height: 100%;
        border: solid $primary;
    }

    #controls {
        height: auto;
        padding: 1;
        background: $panel;
    }

    Button {
        margin: 0 1;
    }

    .running {
        color: $success;
    }

    .stopped {
        color: $error;
    }

    DataTable {
        height: 100%;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("s", "start", "Start"),
        ("t", "stop", "Stop"),
        ("a", "start_all", "Start All"),
        ("z", "stop_all", "Stop All"),
    ]

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.manager = ServerManager(config)
        self.selected_server: Optional[str] = None
        self.update_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        with Container(id="main-container"):
            yield DataTable(id="server-table")
            with Horizontal(id="controls"):
                yield Button("Start", id="btn-start", variant="success")
                yield Button("Stop", id="btn-stop", variant="error")
                yield Button("Restart", id="btn-restart", variant="warning")
                yield Button("Start All", id="btn-start-all", variant="primary")
                yield Button("Stop All", id="btn-stop-all", variant="primary")
                yield Button("Refresh", id="btn-refresh")
                yield Button("Export Config", id="btn-export")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the table when the app starts."""
        table = self.query_one("#server-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True

        # Add columns
        table.add_column("Server", width=20)
        table.add_column("Status", width=10)
        table.add_column("PID", width=10)
        table.add_column("Uptime", width=15)
        table.add_column("Memory", width=12)
        table.add_column("CPU", width=10)

        # Load initial data
        self.refresh_table()

        # Set up auto-refresh timer (every 2 seconds)
        self.update_timer = self.set_interval(2.0, self.refresh_table)

    def refresh_table(self) -> None:
        """Refresh the server status table."""
        table = self.query_one("#server-table", DataTable)
        table.clear()

        statuses = self.manager.get_all_statuses()

        for status in statuses:
            status_icon = "✓" if status.running else "✗"
            status_text = f"{status_icon} {'Running' if status.running else 'Stopped'}"

            pid_text = str(status.pid) if status.pid else "-"
            uptime_text = self._format_uptime(status.uptime) if status.uptime else "-"
            memory_text = f"{status.memory_mb:.1f} MB" if status.memory_mb else "-"
            cpu_text = f"{status.cpu_percent:.1f}%" if status.cpu_percent else "-"

            table.add_row(
                status.name,
                status_text,
                pid_text,
                uptime_text,
                memory_text,
                cpu_text,
            )

    @staticmethod
    def _format_uptime(seconds: float) -> str:
        """Format uptime in human-readable format."""
        if seconds is None:
            return "-"

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

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        table = self.query_one("#server-table", DataTable)
        row_key = event.row_key
        row = table.get_row(row_key)
        if row:
            self.selected_server = str(row[0])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "btn-start":
            self.action_start()
        elif button_id == "btn-stop":
            self.action_stop()
        elif button_id == "btn-restart":
            self.action_restart()
        elif button_id == "btn-start-all":
            self.action_start_all()
        elif button_id == "btn-stop-all":
            self.action_stop_all()
        elif button_id == "btn-refresh":
            self.action_refresh()
        elif button_id == "btn-export":
            self.action_export()

    def action_start(self) -> None:
        """Start selected server."""
        if self.selected_server:
            self.manager.start(self.selected_server)
            self.refresh_table()

    def action_stop(self) -> None:
        """Stop selected server."""
        if self.selected_server:
            self.manager.stop(self.selected_server)
            self.refresh_table()

    def action_restart(self) -> None:
        """Restart selected server."""
        if self.selected_server:
            self.manager.restart(self.selected_server)
            self.refresh_table()

    def action_start_all(self) -> None:
        """Start all servers."""
        self.manager.start_all()
        self.refresh_table()

    def action_stop_all(self) -> None:
        """Stop all servers."""
        self.manager.stop_all()
        self.refresh_table()

    def action_refresh(self) -> None:
        """Refresh the table."""
        self.refresh_table()

    def action_export(self) -> None:
        """Export configuration."""
        try:
            output_path = self.config.export_mcp_json("vscode")
            self.notify(f"Exported configuration to: {output_path}")
        except Exception as e:
            self.notify(f"Error exporting: {e}", severity="error")
