"""Tests for easymcp server manager."""

import os
import tempfile
import time
from pathlib import Path

import pytest

from easymcp.config import Config, ServerConfig
from easymcp.manager import ServerManager


@pytest.fixture
def config():
    """Create a test configuration."""
    config = Config()
    config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="python",
        args=["-c", "import time; time.sleep(10)"],
    )
    return config


@pytest.fixture
def manager(config):
    """Create a test server manager."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ServerManager(config)
        manager.state_dir = Path(tmpdir)
        yield manager
        # Clean up any running processes
        manager.stop_all()


def test_start_server(manager):
    """Test starting a server."""
    result = manager.start("test-server")
    
    assert result is True
    assert manager.is_running("test-server")
    
    # Clean up
    manager.stop("test-server")


def test_start_server_already_running(manager):
    """Test starting a server that's already running."""
    manager.start("test-server")
    
    # Try to start again
    result = manager.start("test-server")
    assert result is False
    
    # Clean up
    manager.stop("test-server")


def test_stop_server(manager):
    """Test stopping a server."""
    manager.start("test-server")
    time.sleep(0.5)
    
    result = manager.stop("test-server")
    
    assert result is True
    assert not manager.is_running("test-server")


def test_stop_server_not_running(manager):
    """Test stopping a server that's not running."""
    result = manager.stop("test-server")
    assert result is False


def test_restart_server(manager):
    """Test restarting a server."""
    manager.start("test-server")
    time.sleep(0.5)
    
    old_status = manager.get_status("test-server")
    old_pid = old_status.pid
    
    result = manager.restart("test-server")
    time.sleep(0.5)
    
    new_status = manager.get_status("test-server")
    
    assert result is True
    assert manager.is_running("test-server")
    assert new_status.pid != old_pid
    
    # Clean up
    manager.stop("test-server")


def test_get_status_running(manager):
    """Test getting status of a running server."""
    manager.start("test-server")
    time.sleep(0.5)
    
    status = manager.get_status("test-server")
    
    assert status.name == "test-server"
    assert status.running is True
    assert status.pid is not None
    assert status.uptime is not None
    assert status.memory_mb is not None
    
    # Clean up
    manager.stop("test-server")


def test_get_status_stopped(manager):
    """Test getting status of a stopped server."""
    status = manager.get_status("test-server")
    
    assert status.name == "test-server"
    assert status.running is False
    assert status.pid is None


def test_get_all_statuses(manager):
    """Test getting status of all servers."""
    statuses = manager.get_all_statuses()
    
    assert len(statuses) == 1
    assert statuses[0].name == "test-server"


def test_is_running(manager):
    """Test checking if a server is running."""
    assert not manager.is_running("test-server")
    
    manager.start("test-server")
    time.sleep(0.5)
    assert manager.is_running("test-server")
    
    manager.stop("test-server")
    time.sleep(0.5)
    assert not manager.is_running("test-server")


def test_get_logs(manager):
    """Test getting server logs."""
    # Start server that writes output
    manager.config.servers["test-server"] = ServerConfig(
        name="test-server",
        command="python",
        args=["-c", "print('test output'); import time; time.sleep(1)"],
    )
    
    manager.start("test-server")
    time.sleep(1.5)
    
    logs = manager.get_logs("test-server")
    
    assert "test output" in logs
    
    # Clean up
    manager.stop("test-server")
