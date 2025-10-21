#!/usr/bin/env python3
"""
Verification script for easymcp installation and functionality.

Run this script to verify that easymcp is installed correctly and
all core features are working.
"""

import sys
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print a header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")


def check_python_version():
    """Check Python version."""
    print("Checking Python version...", end=' ')
    version = sys.version_info
    if version >= (3, 9):
        print(f"{GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{RESET}")
        return True
    else:
        print(f"{RED}✗ Python {version.major}.{version.minor}.{version.micro} (requires >=3.9){RESET}")
        return False


def check_package_installed():
    """Check if easymcp package is installed."""
    print("Checking easymcp package...", end=' ')
    try:
        import easymcp
        print(f"{GREEN}✓ easymcp {easymcp.__version__}{RESET}")
        return True
    except ImportError:
        print(f"{RED}✗ Not installed{RESET}")
        return False


def check_dependencies():
    """Check if all dependencies are installed."""
    deps = {
        'pyyaml': 'yaml',
        'click': 'click',
        'textual': 'textual',
        'psutil': 'psutil',
    }
    
    all_ok = True
    print("\nChecking dependencies:")
    
    for name, module in deps.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  {name:15s} {GREEN}✓ {version}{RESET}")
        except ImportError:
            print(f"  {name:15s} {RED}✗ Not installed{RESET}")
            all_ok = False
    
    return all_ok


def check_core_functionality():
    """Check core easymcp functionality."""
    print("\nChecking core functionality:")
    
    try:
        from easymcp.config import Config, ServerConfig
        print(f"  Config module     {GREEN}✓{RESET}")
        
        # Test basic config creation
        config = Config()
        config.servers['test'] = ServerConfig(name='test', command='echo', args=['hello'])
        print(f"  Config creation   {GREEN}✓{RESET}")
        
        # Test mcp.json generation
        mcp_json = config.generate_mcp_json('vscode')
        assert 'mcpServers' in mcp_json
        print(f"  MCP JSON export   {GREEN}✓{RESET}")
        
        return True
    except Exception as e:
        print(f"  {RED}✗ Error: {e}{RESET}")
        return False


def check_cli_available():
    """Check if CLI is available."""
    print("\nChecking CLI availability:")
    
    import subprocess
    
    # Try easymcp command
    try:
        result = subprocess.run(
            ['easymcp', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  easymcp command   {GREEN}✓{RESET}")
            return True
        else:
            print(f"  easymcp command   {YELLOW}⚠ Not in PATH{RESET}")
            return False
    except FileNotFoundError:
        print(f"  easymcp command   {YELLOW}⚠ Not in PATH (use: python -m easymcp.cli){RESET}")
        return False
    except Exception as e:
        print(f"  easymcp command   {RED}✗ Error: {e}{RESET}")
        return False


def check_config_locations():
    """Check configuration file locations."""
    print("\nChecking configuration locations:")
    
    locations = [
        Path.cwd() / "easymcp.yaml",
        Path.home() / ".config" / "easymcp" / "easymcp.yaml",
    ]
    
    found = False
    for loc in locations:
        if loc.exists():
            print(f"  {loc} {GREEN}✓ Found{RESET}")
            found = True
        else:
            print(f"  {loc} {YELLOW}⚠ Not found{RESET}")
    
    if not found:
        print(f"\n  {YELLOW}Run 'easymcp init' to create a configuration file{RESET}")
    
    return True


def main():
    """Run all checks."""
    print_header("easymcp Installation Verification")
    
    checks = [
        ("Python version", check_python_version),
        ("Package installation", check_package_installed),
        ("Dependencies", check_dependencies),
        ("Core functionality", check_core_functionality),
        ("CLI availability", check_cli_available),
        ("Configuration", check_config_locations),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n{RED}Error during {name}: {e}{RESET}")
            results.append(False)
    
    # Summary
    print_header("Summary")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}All checks passed! ({passed}/{total}){RESET}")
        print(f"\n{GREEN}easymcp is ready to use!{RESET}")
        print("\nNext steps:")
        print("  1. Run: easymcp init")
        print("  2. Edit: easymcp.yaml")
        print("  3. Start: easymcp start --all")
        print("  4. Status: easymcp status")
        return 0
    else:
        print(f"{YELLOW}Some checks did not pass ({passed}/{total}){RESET}")
        print("\nTo fix issues:")
        print("  1. Install easymcp: pip install easymcp")
        print("  2. Install from source: pip install -e .")
        print("  3. Check documentation: docs/INSTALLATION.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
