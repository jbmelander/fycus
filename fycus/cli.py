"""Command-line interface for Fycus"""

import sys
from .config import init_config_interactive, show_current_config


def print_usage():
    """Print CLI usage information."""
    print("Usage: fygaro <command>")
    print("\nCommands:")
    print("  init       - Run interactive configuration setup")
    print("  config     - Show current configuration")
    print("  --version  - Show version information")
    print("  --help     - Show this help message")


def main():
    """Main CLI entry point for fygaro commands."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        init_config_interactive()
    elif command == 'config':
        show_current_config()
    elif command == '--version':
        from . import __version__
        print(f"fygaro {__version__}")
    elif command == '--help' or command == '-h':
        print_usage()
    else:
        print(f"Unknown command: {command}")
        print()
        print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
