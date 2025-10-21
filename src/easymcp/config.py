"""Configuration management for easymcp."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class ServerConfig:
    """Configuration for a single MCP server."""

    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    cwd: Optional[str] = None
    auto_start: bool = False
    
    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "ServerConfig":
        """Create ServerConfig from dictionary."""
        return cls(
            name=name,
            command=data.get("command", ""),
            args=data.get("args", []),
            env=data.get("env", {}),
            cwd=data.get("cwd"),
            auto_start=data.get("auto_start", False),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ServerConfig to dictionary."""
        result = {
            "command": self.command,
            "args": self.args,
        }
        if self.env:
            result["env"] = self.env
        if self.cwd:
            result["cwd"] = self.cwd
        if self.auto_start:
            result["auto_start"] = self.auto_start
        return result


@dataclass
class BundleConfig:
    """Configuration for a bundle of MCP servers."""

    name: str
    servers: List[str] = field(default_factory=list)
    auto_start: bool = False
    
    @classmethod
    def from_dict(cls, name: str, data: Dict[str, Any]) -> "BundleConfig":
        """Create BundleConfig from dictionary."""
        return cls(
            name=name,
            servers=data.get("servers", []),
            auto_start=data.get("auto_start", False),
        )


class Config:
    """Main configuration class for easymcp."""
    
    DEFAULT_CONFIG_NAME = "easymcp.yaml"
    DEFAULT_CONFIG_LOCATIONS = [
        Path.home() / ".config" / "easymcp" / DEFAULT_CONFIG_NAME,
        Path.cwd() / DEFAULT_CONFIG_NAME,
    ]
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration file. If None, searches default locations.
        """
        self.config_path = config_path or self._find_config()
        self.servers: Dict[str, ServerConfig] = {}
        self.bundles: Dict[str, BundleConfig] = {}
        
        if self.config_path and self.config_path.exists():
            self.load()
    
    def _find_config(self) -> Optional[Path]:
        """Find configuration file in default locations."""
        for location in self.DEFAULT_CONFIG_LOCATIONS:
            if location.exists():
                return location
        return None
    
    def load(self) -> None:
        """Load configuration from file."""
        if not self.config_path:
            return
        
        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f) or {}
        
        # Load servers
        servers_data = data.get("servers", {})
        for name, server_data in servers_data.items():
            self.servers[name] = ServerConfig.from_dict(name, server_data)
        
        # Load bundles
        bundles_data = data.get("bundles", {})
        for name, bundle_data in bundles_data.items():
            self.bundles[name] = BundleConfig.from_dict(name, bundle_data)
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to file.
        
        Args:
            path: Path to save to. If None, uses current config_path.
        """
        save_path = path or self.config_path
        if not save_path:
            raise ValueError("No configuration path specified")
        
        # Ensure directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "servers": {name: server.to_dict() for name, server in self.servers.items()},
            "bundles": {
                name: {"servers": bundle.servers, "auto_start": bundle.auto_start}
                for name, bundle in self.bundles.items()
            },
        }
        
        with open(save_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        
        self.config_path = save_path
    
    def generate_mcp_json(self, target: str = "vscode") -> Dict[str, Any]:
        """Generate mcp.json configuration for various tools.
        
        Args:
            target: Target tool ('vscode', 'claude', or 'copilot')
        
        Returns:
            Dictionary containing the mcp.json configuration
        """
        mcp_servers = {}
        
        for name, server in self.servers.items():
            server_config = {
                "command": server.command,
            }
            if server.args:
                server_config["args"] = server.args
            if server.env:
                server_config["env"] = server.env
            if server.cwd:
                server_config["cwd"] = server.cwd
            
            mcp_servers[name] = server_config
        
        if target == "vscode":
            return {
                "mcpServers": mcp_servers
            }
        elif target == "claude":
            return {
                "mcpServers": mcp_servers
            }
        elif target == "copilot":
            return {
                "mcp": {
                    "servers": mcp_servers
                }
            }
        else:
            return {"mcpServers": mcp_servers}
    
    def export_mcp_json(self, target: str = "vscode", output_path: Optional[Path] = None) -> Path:
        """Export mcp.json configuration to file.
        
        Args:
            target: Target tool ('vscode', 'claude', or 'copilot')
            output_path: Path to save to. If None, uses default location for target.
        
        Returns:
            Path where configuration was saved
        """
        config = self.generate_mcp_json(target)
        
        if not output_path:
            if target == "vscode":
                output_path = Path.home() / ".vscode" / "mcp.json"
            elif target == "claude":
                output_path = Path.home() / ".claude" / "mcp.json"
            elif target == "copilot":
                output_path = Path.home() / ".copilot" / "mcp.json"
            else:
                output_path = Path.cwd() / "mcp.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(config, f, indent=2)
        
        return output_path
