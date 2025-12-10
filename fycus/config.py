"""Configuration management for Fycus"""

import os
import sys
from pathlib import Path
import yaml


def get_config_dir():
    """Get platform-appropriate configuration directory.

    Returns:
        Path: Configuration directory path
            - Linux: ~/.config/fycus
            - macOS: ~/Library/Application Support/fycus
            - Windows: %APPDATA%\\fycus
    """
    if sys.platform == 'win32':
        # Windows: %APPDATA%\fycus
        base = os.getenv('APPDATA')
        if not base:
            base = Path.home() / 'AppData' / 'Roaming'
        else:
            base = Path(base)
        return base / 'fycus'
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/fycus
        return Path.home() / 'Library' / 'Application Support' / 'fycus'
    else:
        # Linux/Unix: ~/.config/fycus (XDG Base Directory spec)
        xdg_config = os.getenv('XDG_CONFIG_HOME')
        if xdg_config:
            return Path(xdg_config) / 'fycus'
        return Path.home() / '.config' / 'fycus'


def get_config_path():
    """Get full path to config.yaml file.

    Returns:
        Path: Path to config.yaml
    """
    return get_config_dir() / 'config.yaml'


def load_config():
    """Load configuration from config.yaml.

    Returns:
        dict: Configuration dictionary, empty dict if file doesn't exist or on error
    """
    config_path = get_config_path()

    if not config_path.exists():
        return {}

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}

        # Validate base_path if present
        if 'base_path' in config:
            path = Path(config['base_path'])
            if not path.exists():
                print(f"Warning: Configured base_path doesn't exist: {path}")
                print("Falling back to current directory.")
                return {}

        return config
    except Exception as e:
        print(f"Warning: Failed to load config from {config_path}: {e}")
        return {}


def save_config(config):
    """Save configuration to config.yaml.

    Args:
        config (dict): Configuration dictionary to save
    """
    config_path = get_config_path()
    config_dir = config_path.parent

    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, 'w') as f:
            yaml.safe_dump(config, f, default_flow_style=False)
    except Exception as e:
        print(f"Error: Failed to save config to {config_path}: {e}")
        raise


def get_base_path():
    """Get configured base path for figures.

    Returns:
        Path or None: Configured base path, or None if not configured
    """
    try:
        config = load_config()
        if 'base_path' in config:
            path = Path(config['base_path'])
            if path.exists():
                return path
        return None
    except Exception:
        # Fail silently - don't break user's plotting code
        return None


def init_config_interactive():
    """Run interactive configuration setup wizard."""
    print("=" * 60)
    print("Fycus Configuration Setup")
    print("=" * 60)

    # Get current config if exists
    config_path = get_config_path()
    current_config = load_config()
    current_base = current_config.get('base_path', None)

    if current_base:
        print(f"\nCurrent base path: {current_base}")
    else:
        print("\nNo base path configured (using current working directory)")

    print(f"\nConfiguration will be saved to: {config_path}")

    # Prompt user
    print("\nWhere should figures be saved by default?")
    print("  [1] Create new Fycus directory (~/Fycus)")
    print("  [2] Specify a custom directory")
    print("  [3] Use current working directory (default behavior)")
    print("  [4] Cancel")

    while True:
        choice = input("\nSelect [1-4]: ").strip()

        if choice == '1':
            # Create ~/Fycus directory and set as global default
            path = Path.home() / 'Fycus'

            # Create directory if it doesn't exist
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    print(f"\nCreated directory: {path}")
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    print("Configuration cancelled.")
                    return
            else:
                print(f"\nDirectory already exists: {path}")

            # Save config
            config = current_config.copy()
            config['base_path'] = str(path)
            save_config(config)
            print("\nConfiguration saved!")
            print(f"Figures will be saved to: {path}")
            print(f"\nYou can always override this per-project:")
            print(f"  F = Fycus('name', base_path='/custom/path')")
            break

        elif choice == '2':
            # Get custom path
            path_input = input("\nEnter full path (or use ~ for home directory): ").strip()

            # Expand and resolve path
            path = Path(path_input).expanduser().resolve()

            # Validate path
            if not path.exists():
                print(f"\nDirectory '{path}' doesn't exist.")
                create = input("Create it? [y/N]: ").strip().lower()
                if create == 'y':
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                        print(f"Created directory: {path}")
                    except Exception as e:
                        print(f"Error creating directory: {e}")
                        print("Configuration cancelled.")
                        return
                else:
                    print("Configuration cancelled.")
                    return

            # Save config
            config = current_config.copy()
            config['base_path'] = str(path)
            save_config(config)
            print("\nConfiguration saved!")
            print(f"Figures will be saved to: {path}")
            print(f"\nYou can always override this per-project:")
            print(f"  F = Fycus('name', base_path='/custom/path')")
            break

        elif choice == '3':
            # Remove base_path from config (use default cwd behavior)
            config = current_config.copy()
            config.pop('base_path', None)
            save_config(config)
            print("\nConfiguration saved!")
            print("Figures will be saved to the current working directory.")
            break

        elif choice == '4':
            print("\nConfiguration cancelled.")
            return

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


def show_current_config():
    """Display current configuration."""
    config_path = get_config_path()

    print("=" * 60)
    print("Fycus Configuration")
    print("=" * 60)
    print(f"\nConfig file: {config_path}")

    if config_path.exists():
        config = load_config()
        base_path = config.get('base_path', None)

        if base_path:
            print(f"Base path: {base_path}")

            # Check if path exists
            if not Path(base_path).exists():
                print("  [WARNING: Directory does not exist]")
        else:
            print("Base path: Not set (using current working directory)")
    else:
        print("\nNo configuration file found.")
        print("Run 'fycus init' to create one.")

    print("\nPriority order:")
    print("  1. Constructor parameter (Fycus('name', base_path='/path'))")
    print("  2. Configuration file")
    print("  3. Current working directory (default)")
