"""
init_project.py
Auld Map Project - Project Initialization Script
"""

import sys
import os
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "project.yaml"
DATA_INPUT = PROJECT_ROOT / "data" / "input"


def check_directories():
    """Check and create required directories"""
    required_dirs = [
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "data" / "input",
        PROJECT_ROOT / "data" / "output",
        PROJECT_ROOT / "data" / "masks",
        PROJECT_ROOT / "data" / "tiles" / "terrain",
        PROJECT_ROOT / "web",
        PROJECT_ROOT / "docs",
    ]

    created = []
    for d in required_dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(d.relative_to(PROJECT_ROOT))
    return created


def load_config():
    """Load config file"""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_input_files():
    """Check input files"""
    terrain = DATA_INPUT / "terrain_reference.png"
    political = DATA_INPUT / "political_reference.png"
    return {
        "terrain_reference.png": terrain.exists(),
        "political_reference.png": political.exists(),
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 50)
    print("Auld Map Project - Initialization")
    print("=" * 50)
    print()

    # 1. Check directories
    print("[1/3] Checking directory structure...")
    created = check_directories()
    all_dirs = [
        "config", "scripts", "data/input", "data/output",
        "data/masks", "data/tiles/terrain", "web", "docs"
    ]
    for d in all_dirs:
        p = PROJECT_ROOT / d
        status = "[OK]" if p.exists() else "[MISSING]"
        print(f"  {status}  {d}")
    if created:
        print(f"\n  New directories: {len(created)}")
    print()

    # 2. Check config
    print("[2/3] Checking config file...")
    if CONFIG_FILE.exists():
        config = load_config()
        print(f"  [OK] config/project.yaml exists")
        if config:
            print(f"\n  Config summary:")
            for k, v in config.items():
                if isinstance(v, dict):
                    print(f"    {k}:")
                    for sub_k, sub_v in v.items():
                        print(f"      {sub_k}: {sub_v}")
                else:
                    print(f"    {k}: {v}")
    else:
        print(f"  [MISSING] config/project.yaml - please create first")
    print()

    # 3. Check input files
    print("[3/3] Checking input files...")
    input_status = check_input_files()
    for fname, exists in input_status.items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status}  data/input/{fname}")
    print()

    missing = [f for f, e in input_status.items() if not e]
    if not CONFIG_FILE.exists():
        print("TIP: Create config/project.yaml first")
    if missing:
        print(f"TIP: Place missing input files in data/input/")
    if CONFIG_FILE.exists() and all(input_status.values()):
        print("READY: Project initialized - proceed to next steps!")
    print()


if __name__ == "__main__":
    main()