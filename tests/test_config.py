"""Tests for easymcp configuration."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from easymcp.config import BundleConfig, Config, ServerConfig


def test_server_config_from_dict():
    """Test creating ServerConfig from dictionary."""
    data = {
        "command": "node",
        "args": ["server.js"],
        "env": {"API_KEY": "test"},
        "cwd": "/tmp",
        "auto_start": True,
    }
    
    config = ServerConfig.from_dict("test-server", data)
    
    assert config.name == "test-server"
    assert config.command == "node"
    assert config.args == ["server.js"]
    assert config.env == {"API_KEY": "test"}
    assert config.cwd == "/tmp"
    assert config.auto_start is True


def test_server_config_to_dict():
    """Test converting ServerConfig to dictionary."""
    config = ServerConfig(
        name="test-server",
        command="node",
        args=["server.js"],
        env={"API_KEY": "test"},
        cwd="/tmp",
        auto_start=True,
    )
    
    result = config.to_dict()
    
    assert result["command"] == "node"
    assert result["args"] == ["server.js"]
    assert result["env"] == {"API_KEY": "test"}
    assert result["cwd"] == "/tmp"
    assert result["auto_start"] is True


def test_bundle_config_from_dict():
    """Test creating BundleConfig from dictionary."""
    data = {
        "servers": ["server1", "server2"],
        "auto_start": True,
    }
    
    config = BundleConfig.from_dict("test-bundle", data)
    
    assert config.name == "test-bundle"
    assert config.servers == ["server1", "server2"]
    assert config.auto_start is True


def test_config_load():
    """Test loading configuration from YAML file."""
    config_data = {
        "servers": {
            "test-server": {
                "command": "node",
                "args": ["server.js"],
            }
        },
        "bundles": {
            "test-bundle": {
                "servers": ["test-server"],
            }
        }
    }
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(config_data, f)
        config_path = Path(f.name)
    
    try:
        config = Config(config_path)
        
        assert "test-server" in config.servers
        assert config.servers["test-server"].command == "node"
        assert config.servers["test-server"].args == ["server.js"]
        
        assert "test-bundle" in config.bundles
        assert config.bundles["test-bundle"].servers == ["test-server"]
    finally:
        config_path.unlink()


def test_config_save():
    """Test saving configuration to YAML file."""
    config = Config()
    config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="node",
        args=["server.js"],
    )
    config.bundles["test-bundle"] = BundleConfig(
        name="test-bundle",
        servers=["test-server"],
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test.yaml"
        config.save(config_path)
        
        assert config_path.exists()
        
        with open(config_path) as f:
            data = yaml.safe_load(f)
        
        assert "test-server" in data["servers"]
        assert data["servers"]["test-server"]["command"] == "node"
        assert "test-bundle" in data["bundles"]


def test_generate_mcp_json_vscode():
    """Test generating mcp.json for VS Code."""
    config = Config()
    config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="node",
        args=["server.js"],
        env={"API_KEY": "test"},
    )
    
    result = config.generate_mcp_json("vscode")
    
    assert "mcpServers" in result
    assert "test-server" in result["mcpServers"]
    assert result["mcpServers"]["test-server"]["command"] == "node"
    assert result["mcpServers"]["test-server"]["args"] == ["server.js"]
    assert result["mcpServers"]["test-server"]["env"] == {"API_KEY": "test"}


def test_generate_mcp_json_copilot():
    """Test generating mcp.json for Copilot."""
    config = Config()
    config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="node",
        args=["server.js"],
    )
    
    result = config.generate_mcp_json("copilot")
    
    assert "mcp" in result
    assert "servers" in result["mcp"]
    assert "test-server" in result["mcp"]["servers"]


def test_export_mcp_json():
    """Test exporting mcp.json to file."""
    config = Config()
    config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="node",
        args=["server.js"],
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "mcp.json"
        result_path = config.export_mcp_json("vscode", output_path)
        
        assert result_path == output_path
        assert output_path.exists()
        
        with open(output_path) as f:
            data = json.load(f)
        
        assert "mcpServers" in data
        assert "test-server" in data["mcpServers"]
