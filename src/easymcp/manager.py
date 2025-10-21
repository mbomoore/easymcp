"""Server management for easymcp."""

import json
import os
import signal
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import psutil

from .config import Config, ServerConfig


@dataclass
class ServerStatus:
    """Status information for a server."""

    name: str
    running: bool
    pid: Optional[int] = None
    uptime: Optional[float] = None
    memory_mb: Optional[float] = None
    cpu_percent: Optional[float] = None
    start_time: Optional[datetime] = None


class ServerManager:
    """Manager for MCP servers."""
    
    STATE_DIR = Path.home() / ".local" / "state" / "easymcp"
    
    def __init__(self, config: Config):
        """Initialize server manager.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.state_dir = self.STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_pid_file(self, server_name: str) -> Path:
        """Get path to PID file for server."""
        return self.state_dir / f"{server_name}.pid"
    
    def _get_log_file(self, server_name: str) -> Path:
        """Get path to log file for server."""
        return self.state_dir / f"{server_name}.log"
    
    def _save_pid(self, server_name: str, pid: int) -> None:
        """Save PID to file."""
        pid_file = self._get_pid_file(server_name)
        with open(pid_file, "w") as f:
            json.dump({"pid": pid, "start_time": datetime.now().isoformat()}, f)
    
    def _load_pid(self, server_name: str) -> Optional[Dict]:
        """Load PID from file."""
        pid_file = self._get_pid_file(server_name)
        if not pid_file.exists():
            return None
        
        try:
            with open(pid_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def _remove_pid(self, server_name: str) -> None:
        """Remove PID file."""
        pid_file = self._get_pid_file(server_name)
        if pid_file.exists():
            pid_file.unlink()
    
    def start(self, server_name: str) -> bool:
        """Start a server.
        
        Args:
            server_name: Name of server to start
        
        Returns:
            True if server was started, False otherwise
        """
        if server_name not in self.config.servers:
            raise ValueError(f"Server '{server_name}' not found in configuration")
        
        # Check if already running
        if self.is_running(server_name):
            return False
        
        server = self.config.servers[server_name]
        log_file = self._get_log_file(server_name)
        
        # Build command
        cmd = [server.command] + server.args
        
        # Build environment
        env = os.environ.copy()
        env.update(server.env)
        
        # Start process
        try:
            with open(log_file, "a") as log:
                process = subprocess.Popen(
                    cmd,
                    env=env,
                    cwd=server.cwd,
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
            
            self._save_pid(server_name, process.pid)
            return True
        except Exception as e:
            with open(log_file, "a") as log:
                log.write(f"\nError starting server: {e}\n")
            return False
    
    def stop(self, server_name: str, timeout: int = 10) -> bool:
        """Stop a server.
        
        Args:
            server_name: Name of server to stop
            timeout: Timeout in seconds for graceful shutdown
        
        Returns:
            True if server was stopped, False otherwise
        """
        pid_data = self._load_pid(server_name)
        if not pid_data:
            return False
        
        pid = pid_data["pid"]
        
        try:
            process = psutil.Process(pid)
            
            # Try graceful shutdown first
            process.terminate()
            
            # Wait for process to exit
            try:
                process.wait(timeout=timeout)
            except psutil.TimeoutExpired:
                # Force kill if timeout exceeded
                process.kill()
                process.wait(timeout=5)
            
            self._remove_pid(server_name)
            return True
        except psutil.NoSuchProcess:
            # Process already dead
            self._remove_pid(server_name)
            return True
        except Exception:
            return False
    
    def restart(self, server_name: str) -> bool:
        """Restart a server.
        
        Args:
            server_name: Name of server to restart
        
        Returns:
            True if server was restarted, False otherwise
        """
        if self.is_running(server_name):
            self.stop(server_name)
        
        # Give it a moment
        time.sleep(0.5)
        
        return self.start(server_name)
    
    def is_running(self, server_name: str) -> bool:
        """Check if a server is running.
        
        Args:
            server_name: Name of server to check
        
        Returns:
            True if server is running, False otherwise
        """
        pid_data = self._load_pid(server_name)
        if not pid_data:
            return False
        
        try:
            process = psutil.Process(pid_data["pid"])
            return process.is_running()
        except psutil.NoSuchProcess:
            self._remove_pid(server_name)
            return False
    
    def get_status(self, server_name: str) -> ServerStatus:
        """Get status of a server.
        
        Args:
            server_name: Name of server
        
        Returns:
            ServerStatus object
        """
        pid_data = self._load_pid(server_name)
        
        if not pid_data:
            return ServerStatus(name=server_name, running=False)
        
        try:
            process = psutil.Process(pid_data["pid"])
            
            if not process.is_running():
                self._remove_pid(server_name)
                return ServerStatus(name=server_name, running=False)
            
            # Get process info
            create_time = datetime.fromtimestamp(process.create_time())
            uptime = (datetime.now() - create_time).total_seconds()
            
            # Get memory info (in MB)
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024
            
            # Get CPU percent
            cpu_percent = process.cpu_percent(interval=0.1)
            
            return ServerStatus(
                name=server_name,
                running=True,
                pid=pid_data["pid"],
                uptime=uptime,
                memory_mb=memory_mb,
                cpu_percent=cpu_percent,
                start_time=create_time,
            )
        except psutil.NoSuchProcess:
            self._remove_pid(server_name)
            return ServerStatus(name=server_name, running=False)
    
    def get_all_statuses(self) -> List[ServerStatus]:
        """Get status of all servers.
        
        Returns:
            List of ServerStatus objects
        """
        return [self.get_status(name) for name in self.config.servers.keys()]
    
    def start_bundle(self, bundle_name: str) -> Dict[str, bool]:
        """Start all servers in a bundle.
        
        Args:
            bundle_name: Name of bundle to start
        
        Returns:
            Dictionary mapping server names to start success status
        """
        if bundle_name not in self.config.bundles:
            raise ValueError(f"Bundle '{bundle_name}' not found in configuration")
        
        bundle = self.config.bundles[bundle_name]
        results = {}
        
        for server_name in bundle.servers:
            if server_name in self.config.servers:
                results[server_name] = self.start(server_name)
            else:
                results[server_name] = False
        
        return results
    
    def stop_bundle(self, bundle_name: str) -> Dict[str, bool]:
        """Stop all servers in a bundle.
        
        Args:
            bundle_name: Name of bundle to stop
        
        Returns:
            Dictionary mapping server names to stop success status
        """
        if bundle_name not in self.config.bundles:
            raise ValueError(f"Bundle '{bundle_name}' not found in configuration")
        
        bundle = self.config.bundles[bundle_name]
        results = {}
        
        for server_name in bundle.servers:
            if server_name in self.config.servers:
                results[server_name] = self.stop(server_name)
            else:
                results[server_name] = False
        
        return results
    
    def start_all(self) -> Dict[str, bool]:
        """Start all servers.
        
        Returns:
            Dictionary mapping server names to start success status
        """
        results = {}
        for server_name in self.config.servers.keys():
            results[server_name] = self.start(server_name)
        return results
    
    def stop_all(self) -> Dict[str, bool]:
        """Stop all servers.
        
        Returns:
            Dictionary mapping server names to stop success status
        """
        results = {}
        for server_name in self.config.servers.keys():
            results[server_name] = self.stop(server_name)
        return results
    
    def get_logs(self, server_name: str, lines: int = 50) -> str:
        """Get recent logs for a server.
        
        Args:
            server_name: Name of server
            lines: Number of lines to return
        
        Returns:
            Log content
        """
        log_file = self._get_log_file(server_name)
        
        if not log_file.exists():
            return ""
        
        try:
            with open(log_file, "r") as f:
                all_lines = f.readlines()
                return "".join(all_lines[-lines:])
        except IOError:
            return ""
