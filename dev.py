#!/usr/bin/env python3
"""
Development helper script for Procedural Human Generator
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        # Use UV to run commands in the virtual environment
        import os
        home = os.path.expanduser("~")
        uv_path = os.path.join(home, ".local", "bin", "uv")
        uv_cmd = f'"{uv_path}" run {cmd}'
        result = subprocess.run(uv_cmd, check=True, shell=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False

def format_code():
    """Format code with Black"""
    return run_command("black procedural_human --line-length 88", "Code formatting")

def lint_code():
    """Lint code with flake8"""
    return run_command("flake8 procedural_human --max-line-length 88 --ignore E203,W503", "Code linting")

def package_addon():
    """Create a zip package of the addon"""
    return run_command("python package.py", "Package addon")

def install_addon():
    """Install the addon to Blender's addons directory"""
    return run_command("python install.py", "Install addon")

def main():
    parser = argparse.ArgumentParser(description="Development tools for Procedural Human Generator")
    parser.add_argument("command", choices=["format", "lint", "package", "install", "all"], 
                       help="Command to run")
    
    args = parser.parse_args()
    
    print("🛠️  Procedural Human Generator - Development Tools")
    print("=" * 50)
    
    success = True
    
    if args.command == "format":
        success = format_code()
    elif args.command == "lint":
        success = lint_code()
    elif args.command == "package":
        success = package_addon()
    elif args.command == "install":
        success = install_addon()
    elif args.command == "all":
        success = (
            format_code() and 
            lint_code() and 
            package_addon() and
            install_addon()
        )
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All operations completed successfully!")
    else:
        print("💥 Some operations failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
