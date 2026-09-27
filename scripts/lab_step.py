#!/usr/bin/env python3
"""Show and apply the small, readable patches used by course labs."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
STEP_DIRECTORY = REPOSITORY_ROOT / "labs" / "01-metrics-foundations" / "steps"


def available_steps() -> list[Path]:
    return sorted(STEP_DIRECTORY.glob("*.patch"))


def resolve_step(value: str) -> Path:
    candidates = [
        path
        for path in available_steps()
        if path.stem == value or path.name == value or path.stem.startswith(f"{value}-")
    ]
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        choices = ", ".join(path.stem for path in available_steps())
        raise ValueError(f"unknown step {value!r}; available steps: {choices}")
    matches = ", ".join(path.stem for path in candidates)
    raise ValueError(f"step {value!r} is ambiguous; matches: {matches}")


def run_git(repo: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def ensure_repository(repo: Path) -> None:
    result = run_git(repo, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise ValueError(f"{repo} is not inside a Git repository")
    actual_root = Path(result.stdout.strip()).resolve()
    if actual_root != repo:
        raise ValueError(f"--repo must be the repository root: {actual_root}")


def show_step(step: Path) -> None:
    print(f"Step: {step.stem}\n")
    print(step.read_text(encoding="utf-8"), end="")


def apply_step(step: Path, repo: Path, assume_yes: bool) -> int:
    ensure_repository(repo)
    patch = str(step)
    check = run_git(repo, "apply", "--check", patch)
    if check.returncode != 0:
        reverse_check = run_git(repo, "apply", "--reverse", "--check", patch)
        if reverse_check.returncode == 0:
            print(f"Step {step.stem} is already applied.", file=sys.stderr)
        else:
            detail = check.stderr.strip() or check.stdout.strip()
            print(
                f"Cannot apply {step.stem}. Apply earlier numbered steps first and "
                f"check for overlapping local edits.\n{detail}",
                file=sys.stderr,
            )
        return 1

    show_step(step)
    if not assume_yes:
        answer = input("\nApply this patch? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("No files changed.")
            return 0

    result = run_git(repo, "apply", patch)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        print(f"git apply failed: {detail}", file=sys.stderr)
        return 1

    print(f"\nApplied {step.stem}. Review with: git diff -- application/main.py")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Show or apply transparent course step patches."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=REPOSITORY_ROOT,
        help="repository root to update (default: the repository containing this script)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="list available Lab 01 steps")

    show_parser = subparsers.add_parser("show", help="print a step's complete patch")
    show_parser.add_argument("step", help="step number or filename")

    apply_parser = subparsers.add_parser("apply", help="check and apply a step patch")
    apply_parser.add_argument("step", help="step number or filename")
    apply_parser.add_argument(
        "--yes", action="store_true", help="apply without the interactive confirmation"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "list":
            for step in available_steps():
                print(step.stem)
            return 0

        step = resolve_step(args.step)
        if args.command == "show":
            show_step(step)
            return 0
        return apply_step(step, args.repo.resolve(), args.yes)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
