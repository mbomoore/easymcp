#!/usr/bin/env python3
"""
Demo script for easymcp functionality.

This script demonstrates the core features of easymcp without requiring
full installation of dependencies.
"""

import sys
import tempfile
from pathlib import Path

# Add src to path for demo
sys.path.insert(0, str(Path(__file__).parent / "src"))

from easymcp.config import Config, ServerConfig, BundleConfig


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_config_creation():
    """Demonstrate configuration creation."""
    print_section("Configuration Creation")
    
    config = Config()
    
    # Add servers
    config.servers["web-server"] = ServerConfig(
        name="web-server",
        command="python",
        args=["-m", "http.server", "8000"],
        cwd="/tmp",
        auto_start=False
    )
    
    config.servers["api-server"] = ServerConfig(
        name="api-server",
        command="node",
        args=["api.js"],
        env={"PORT": "3000", "NODE_ENV": "development"},
        auto_start=True
    )
    
    # Add bundles
    config.bundles["development"] = BundleConfig(
        name="development",
        servers=["web-server", "api-server"],
        auto_start=False
    )
    
    print("✓ Created configuration with:")
    print(f"  - {len(config.servers)} servers")
    print(f"  - {len(config.bundles)} bundles")
    
    return config


def demo_config_save_load():
    """Demonstrate saving and loading configuration."""
    print_section("Save and Load Configuration")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test.yaml"
        
        # Create and save
        config = Config()
        config.servers["test-server"] = ServerConfig(
            name="test-server",
            command="echo",
            args=["hello"]
        )
        config.save(config_path)
        print(f"✓ Saved configuration to {config_path}")
        
        # Load back
        loaded_config = Config(config_path)
        print(f"✓ Loaded configuration with {len(loaded_config.servers)} server(s)")
        print(f"  - Server: {list(loaded_config.servers.keys())[0]}")


def demo_mcp_json_generation():
    """Demonstrate mcp.json generation."""
    print_section("MCP JSON Generation")
    
    config = Config()
    config.servers["filesystem"] = ServerConfig(
        name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
        env={"NODE_ENV": "production"}
    )
    
    # Generate for different targets
    for target in ["vscode", "claude", "copilot"]:
        mcp_json = config.generate_mcp_json(target)
        print(f"\n✓ Generated mcp.json for {target}:")
        
        if target == "copilot":
            servers = mcp_json.get("mcp", {}).get("servers", {})
        else:
            servers = mcp_json.get("mcpServers", {})
        
        print(f"  - Format: {'mcp.servers' if target == 'copilot' else 'mcpServers'}")
        print(f"  - Servers: {', '.join(servers.keys())}")


def demo_server_config():
    """Demonstrate server configuration options."""
    print_section("Server Configuration Options")
    
    # Basic server
    basic = ServerConfig(
        name="basic-server",
        command="python",
        args=["-m", "myserver"]
    )
    print("✓ Basic server:")
    print(f"  - Command: {basic.command} {' '.join(basic.args)}")
    
    # Server with environment
    with_env = ServerConfig(
        name="env-server",
        command="node",
        args=["server.js"],
        env={"API_KEY": "secret", "DEBUG": "true"}
    )
    print("\n✓ Server with environment variables:")
    print(f"  - Command: {with_env.command}")
    print(f"  - Env vars: {len(with_env.env)}")
    
    # Server with working directory
    with_cwd = ServerConfig(
        name="cwd-server",
        command="npm",
        args=["start"],
        cwd="/path/to/project"
    )
    print("\n✓ Server with working directory:")
    print(f"  - Command: {with_cwd.command}")
    print(f"  - Working dir: {with_cwd.cwd}")
    
    # Auto-start server
    auto_start = ServerConfig(
        name="auto-server",
        command="python",
        args=["-m", "daemon"],
        auto_start=True
    )
    print("\n✓ Auto-start server:")
    print(f"  - Command: {auto_start.command}")
    print(f"  - Auto-start: {auto_start.auto_start}")


def demo_bundle_config():
    """Demonstrate bundle configuration."""
    print_section("Bundle Configuration")
    
    config = Config()
    
    # Add multiple servers
    for i in range(3):
        config.servers[f"server{i+1}"] = ServerConfig(
            name=f"server{i+1}",
            command="python",
            args=["-m", f"service{i+1}"]
        )
    
    # Create bundles
    config.bundles["development"] = BundleConfig(
        name="development",
        servers=["server1", "server2"],
        auto_start=False
    )
    
    config.bundles["production"] = BundleConfig(
        name="production",
        servers=["server2", "server3"],
        auto_start=True
    )
    
    print("✓ Created bundles:")
    for name, bundle in config.bundles.items():
        auto = " (auto-start)" if bundle.auto_start else ""
        print(f"\n  - {name}{auto}")
        print(f"    Servers: {', '.join(bundle.servers)}")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*20 + "easymcp Demo" + " "*26 + "║")
    print("╚" + "═"*58 + "╝")
    
    try:
        demo_config_creation()
        demo_config_save_load()
        demo_mcp_json_generation()
        demo_server_config()
        demo_bundle_config()
        
        print_section("Demo Complete")
        print("✓ All demos completed successfully!")
        print("\nNext steps:")
        print("  1. Install easymcp: pip install easymcp")
        print("  2. Initialize config: easymcp init")
        print("  3. Start servers: easymcp start --all")
        print("  4. Check status: easymcp status")
        print("  5. Launch TUI: easymcp tui")
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
