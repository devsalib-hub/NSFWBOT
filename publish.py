#!/usr/bin/env python3
"""Build the NSFWBot executable with PyInstaller."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
SPEC_FILE = ROOT / "NSFWBot.spec"


def run_command(command: list[str]) -> None:
    subprocess.run(command, check=True)


def ensure_pyinstaller() -> None:
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])


def clean_artifacts() -> None:
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    shutil.rmtree(BUILD_DIR, ignore_errors=True)


def build_executable(skip_clean: bool) -> Path:
    ensure_pyinstaller()
    if not skip_clean:
        clean_artifacts()

    if not SPEC_FILE.exists():
        raise FileNotFoundError(f"Missing spec file: {SPEC_FILE}")

    run_command([sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", str(SPEC_FILE)])

    exe_path = DIST_DIR / "NSFWBot.exe"
    if not exe_path.exists():
        raise RuntimeError("PyInstaller finished but dist/NSFWBot.exe was not created")

    return exe_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the NSFWBot executable using PyInstaller")
    parser.add_argument("--skip-clean", action="store_true", help="Skip removing build/dist before running PyInstaller")
    args = parser.parse_args()

    exe_path = build_executable(skip_clean=args.skip_clean)
    print(f"Build completed successfully. Executable: {exe_path}")


if __name__ == "__main__":
    main()
