#!/usr/bin/env python3
"""
Run all chapter exercise files and report results.

Usage:
    python run_all.py           # Run all chapters
    python run_all.py 1 5 10    # Run specific chapters
    python run_all.py --list    # List available chapters
"""

import subprocess
import sys
import re
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def find_exercise_files() -> list[Path]:
    """Find all chapter exercise files."""
    pattern = re.compile(r"chapter(\d{2})_.*\.py$")
    files = []

    for path in sorted(Path(".").glob("chapter*.py")):
        match = pattern.match(path.name)
        if match:
            # Skip example files (they don't have exercises)
            if "_examples.py" in path.name:
                continue
            files.append(path)

    return files


def get_chapter_number(path: Path) -> int:
    """Extract chapter number from filename."""
    match = re.match(r"chapter(\d{2})", path.name)
    return int(match.group(1)) if match else 0


def run_exercise_file(path: Path) -> tuple[bool, str]:
    """Run an exercise file and return (success, output)."""
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0 and "Congratulations!" in output
        return success, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: Exercise took too long"
    except Exception as e:
        return False, f"ERROR: {e}"


def count_exercises(output: str) -> tuple[int, int]:
    """Count passed and total exercises from output."""
    passed = len(re.findall(r"Exercise \d+ passed", output))
    # Try to find total from the congratulations message or count exercise headers
    return passed, passed  # Assume all found passed


def main():
    args = sys.argv[1:]

    # List mode
    if "--list" in args:
        print(f"{BOLD}Available chapters:{RESET}\n")
        for path in find_exercise_files():
            ch_num = get_chapter_number(path)
            name = path.stem.replace(f"chapter{ch_num:02d}_", "").replace("_", " ").title()
            print(f"  {BLUE}{ch_num:2d}{RESET}. {name}")
        return

    # Find files
    all_files = find_exercise_files()

    # Filter by chapter numbers if specified
    if args:
        try:
            chapters = {int(x) for x in args}
            files = [f for f in all_files if get_chapter_number(f) in chapters]
        except ValueError:
            print(f"{RED}Error: Invalid chapter number{RESET}")
            sys.exit(1)
    else:
        files = all_files

    if not files:
        print(f"{YELLOW}No exercise files found{RESET}")
        return

    print(f"{BOLD}Running {len(files)} exercise file(s)...{RESET}\n")
    print("=" * 60)

    results = []
    total_passed = 0
    total_failed = 0

    for path in files:
        ch_num = get_chapter_number(path)
        name = path.stem.replace(f"chapter{ch_num:02d}_", "").replace("_", " ")

        print(f"\n{BLUE}Chapter {ch_num}{RESET}: {name}")
        print("-" * 40)

        success, output = run_exercise_file(path)
        passed, _ = count_exercises(output)

        if success:
            print(f"{GREEN}PASSED{RESET} ({passed} exercises)")
            total_passed += 1
        else:
            print(f"{RED}FAILED{RESET}")
            # Show error details
            if "Error" in output or "Traceback" in output:
                # Find the relevant error
                lines = output.split("\n")
                for i, line in enumerate(lines):
                    if "Error" in line or "assert" in line.lower():
                        print(f"  {YELLOW}{line.strip()}{RESET}")
                        break
            total_failed += 1

        results.append((ch_num, name, success))

    # Summary
    print("\n" + "=" * 60)
    print(f"{BOLD}SUMMARY{RESET}")
    print("=" * 60)

    for ch_num, name, success in results:
        status = f"{GREEN}PASS{RESET}" if success else f"{RED}FAIL{RESET}"
        print(f"  Chapter {ch_num:2d}: [{status}] {name}")

    print("-" * 60)
    total = total_passed + total_failed
    print(f"  {GREEN}Passed: {total_passed}/{total}{RESET}")
    if total_failed:
        print(f"  {RED}Failed: {total_failed}/{total}{RESET}")

    if total_failed == 0 and total_passed > 0:
        print(f"\n{GREEN}{BOLD}All exercises passed!{RESET}")

    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
