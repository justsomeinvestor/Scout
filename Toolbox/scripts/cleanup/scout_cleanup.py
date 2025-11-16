#!/usr/bin/env python3
"""Scout pre-flight cleanup for stale research data dumps."""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Literal


ROOT = Path(__file__).resolve().parents[3]
LOG_PATH = ROOT / "logs" / "scout_cleanup.log"


RemovalKind = Literal["files", "subdirs"]


@dataclass(frozen=True)
class CleanupRule:
    """Configuration for a cleanup action."""

    name: str
    relative_path: Path
    kind: RemovalKind
    retention_days: int
    patterns: tuple[str, ...] = ("*",)
    recursive: bool = True
    reason: str = ""


CLEANUP_RULES: tuple[CleanupRule, ...] = (
    CleanupRule(
        name="Legacy RSS scraper output",
        relative_path=Path("Scraper") / "output" / "RSS",
        kind="subdirs",
        retention_days=7,
        reason="Deprecated pipeline replaced by Research/RSS; remove stale provider folders.",
    ),
    CleanupRule(
        name="Legacy X/Twitter scraper output",
        relative_path=Path("Scraper") / "output" / "X",
        kind="subdirs",
        retention_days=7,
        reason="Deprecated pipeline replaced by Research/X; remove stale list exports.",
    ),
    CleanupRule(
        name="Legacy YouTube scraper output",
        relative_path=Path("Scraper") / "output" / "YouTube",
        kind="subdirs",
        retention_days=7,
        reason="Deprecated pipeline replaced by Research/YouTube; remove stale channel dumps.",
    ),
    CleanupRule(
        name="Archived X/Twitter JSON dumps",
        relative_path=Path("Toolbox") / "archived_data" / "X_twitter_archive",
        kind="files",
        retention_days=14,
        patterns=("*.json", "*.csv"),
        reason="Legacy backups superseded by Research/X; keep a 2-week lookback only.",
    ),
    CleanupRule(
        name="Research archive snapshots (previous quarters)",
        relative_path=Path("Research") / ".archive",
        kind="files",
        retention_days=60,
        patterns=("*.md", "*.json"),
        reason="Trim long-term archives while keeping roughly two months of history.",
    ),
    CleanupRule(
        name="Research RSS provider archives",
        relative_path=Path("Research") / "RSS" / "_archives",
        kind="files",
        retention_days=30,
        patterns=("*.md", "*.json"),
        reason="Keep only the most recent month of archived RSS summaries.",
    ),
    CleanupRule(
        name="Research YouTube provider archives",
        relative_path=Path("Research") / "YouTube" / "_archives",
        kind="files",
        retention_days=30,
        patterns=("*.md", "*.json"),
        reason="Keep only the most recent month of archived YouTube summaries.",
    ),
    CleanupRule(
        name="Research YouTube monthly snapshots",
        relative_path=Path("Research") / "YouTube" / "2025-10",
        kind="subdirs",
        retention_days=0,
        reason="Remove legacy intermediate YouTube channel dumps superseded by new structure.",
    ),
    CleanupRule(
        name="Research Technicals legacy",
        relative_path=Path("Research") / "Technicals",
        kind="files",
        retention_days=0,
        patterns=(
            "RealTime/**",
            "2025-10/**",
            "*.md",
            "*.json",
            "*.html",
            "*.csv",
        ),
        reason="Clear pre-2025-10-30 technical summaries and legacy realtime captures.",
    ),
    CleanupRule(
        name="Research Technicals realtime subdirs",
        relative_path=Path("Research") / "Technicals" / "RealTime",
        kind="subdirs",
        retention_days=0,
        reason="Remove realtime documentation folders captured during early experimentation.",
    ),
    CleanupRule(
        name="Research Technicals realtime configs",
        relative_path=Path("Research") / "Technicals",
        kind="files",
        retention_days=0,
        patterns=(
            "RealTime/*.env*",
            "RealTime/*.gitignore",
            "RealTime/*.js",
        ),
        reason="Drop legacy realtime collector scripts/configs left over from deprecated tooling.",
    ),
    CleanupRule(
        name="Research X legacy summaries",
        relative_path=Path("Research") / "X",
        kind="files",
        retention_days=0,
        patterns=(
            "Crypto/x_list_posts_[0-9]*.json",
            "Macro/x_list_posts_[0-9]*.json",
            "Technicals/x_list_posts_[0-9]*.json",
            "Bookmarks/x_list_posts_[0-9]*.json",
            "_archives/**",
            "*.md",
        ),
        reason="Remove X/Twitter data files, preserving metadata (x_list_posts_last_run.json) for incremental scraping.",
    ),
    CleanupRule(
        name="Research AI inbox backlog",
        relative_path=Path("Research") / "AI",
        kind="files",
        retention_days=0,
        patterns=("Inbox/**", "*.pdf", "*.md"),
        reason="Purge older AI assistant exports, keeping only new ones if present.",
    ),
    CleanupRule(
        name="Research summary fallbacks",
        relative_path=Path("Research") / "SUMMARIES",
        kind="files",
        retention_days=0,
        patterns=("*.md",),
        reason="Remove outdated summary batches prior to today.",
    ),
    CleanupRule(
        name="Research category overviews",
        relative_path=Path("Research") / "Overviews",
        kind="files",
        retention_days=0,
        patterns=("*.md",),
        reason="Remove outdated overview batches prior to today.",
    ),
    CleanupRule(
        name="Research RSS category overviews (stale)",
        relative_path=Path("Research") / "RSS",
        kind="files",
        retention_days=1,
        patterns=("*_Category_Overview.md",),
        reason="Remove RSS category overviews older than today (keep current day only).",
    ),
    CleanupRule(
        name="Research YouTube category overviews (stale)",
        relative_path=Path("Research") / "YouTube",
        kind="files",
        retention_days=1,
        patterns=("*_Category_Overview.md",),
        reason="Remove YouTube category overviews older than today (keep current day only).",
    ),
    CleanupRule(
        name="Research Technicals category overviews (stale)",
        relative_path=Path("Research") / "Technicals",
        kind="files",
        retention_days=1,
        patterns=("*_Category_Overview.md",),
        reason="Remove Technical category overviews older than today (keep current day only).",
    ),
    CleanupRule(
        name="Research X category overviews (stale)",
        relative_path=Path("Research") / "X",
        kind="files",
        retention_days=1,
        patterns=("*_Category_Overview.md",),
        reason="Remove X/Twitter category overviews older than today (keep current day only).",
    ),
    CleanupRule(
        name="Research market sentiment archive",
        relative_path=Path("Research") / "Market Sentiment Archive",
        kind="files",
        retention_days=0,
        patterns=("*.md",),
        reason="Clear historical market sentiment reports now superseded.",
    ),
    CleanupRule(
        name="Research macro experiments",
        relative_path=Path("Research") / "Macro",
        kind="files",
        retention_days=0,
        patterns=("*.md", "*.json", "*.pdf", "*.csv"),
        reason="Remove macro study scaffolding before today.",
    ),
    CleanupRule(
        name="Research personal notes",
        relative_path=Path("Research") / "Me",
        kind="files",
        retention_days=0,
        patterns=("*.md",),
        reason="Purge personal notes prior to today.",
    ),
    CleanupRule(
        name="Toolbox archived data snapshots",
        relative_path=Path("Toolbox") / "archived_data",
        kind="subdirs",
        retention_days=0,
        reason="Remove deprecated Toolbox archived_data directories superseded by new workflows.",
    ),
    CleanupRule(
        name="Toolbox archived scrapers",
        relative_path=Path("Toolbox") / "archived_scrapers",
        kind="files",
        retention_days=0,
        patterns=("*.py", "*.md", "*.txt"),
        reason="Remove legacy scrapers kept only for reference.",
    ),
    CleanupRule(
        name="Toolbox backups",
        relative_path=Path("Toolbox") / "Backups",
        kind="subdirs",
        retention_days=0,
        reason="Clean obsolete manual backup folders once fresh runs are available.",
    ),
    CleanupRule(
        name="Toolbox backup files",
        relative_path=Path("Toolbox") / "Backups",
        kind="files",
        retention_days=0,
        patterns=("*.html", "*.md", "*.txt", "*backup*"),
        reason="Remove leftover backup artifacts sitting directly under Toolbox/Backups.",
    ),
    CleanupRule(
        name="Master-plan archive backups",
        relative_path=Path("master-plan") / "archive" / "backups",
        kind="subdirs",
        retention_days=0,
        reason="Purge historical master-plan backup folders before new dashboard generation.",
    ),
    CleanupRule(
        name="Master-plan archive monthly snapshots",
        relative_path=Path("master-plan") / "archive",
        kind="subdirs",
        retention_days=0,
        patterns=("2025-10",),
        reason="Remove legacy master-plan monthly archives prior to latest rollout.",
    ),
    CleanupRule(
        name="Master-plan root backups",
        relative_path=Path("master-plan"),
        kind="files",
        retention_days=0,
        patterns=(
            "master-plan.backup*",
            "master-plan.md.backup*",
            "master-plan.md.*backup*",
            "research-dashboard-backup*.html",
            "archive_compressed.zip",
        ),
        reason="Trim old master-plan backup files once latest dashboard is generated.",
    ),
    CleanupRule(
        name="Python bytecode caches",
        relative_path=Path("Scraper") / "__pycache__",
        kind="files",
        retention_days=0,
        patterns=("*.pyc",),
        reason="Clear stale Scraper bytecode caches so fresh builds regenerate as needed.",
    ),
    CleanupRule(
        name="Scripts bytecode caches",
        relative_path=Path("scripts") / "__pycache__",
        kind="files",
        retention_days=0,
        patterns=("*.pyc",),
        reason="Clear stale automation bytecode caches so fresh builds regenerate as needed.",
    ),
    CleanupRule(
        name="Research cache old overviews (ULTRA-AGGRESSIVE - TODAY ONLY)",
        relative_path=Path("Research") / ".cache",
        kind="files",
        retention_days=1,
        patterns=(
            "2025-*_Market_Sentiment_Overview.md",
            "signals_2025-*.json",
            "2025-*_key_themes.md",
            "*_YYYY-MM-DD.json",
        ),
        reason="Remove ALL cached overview/signals files except today's data. Ultra-aggressive cleanup prevents any token inflation from stale files. Strategy: Keep only current day, can always back off if needed.",
    ),
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Purge stale research data ahead of Wingman Recon."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without removing anything.",
    )
    parser.add_argument(
        "--rules",
        nargs="*",
        help="Optional subset of rule names (case-insensitive substring match).",
    )
    parser.add_argument(
        "--retention-override",
        type=int,
        help="Override retention (in days) for all rules. Useful for emergency deep cleans.",
    )
    parser.add_argument(
        "--keep-from",
        type=str,
        help="Keep data modified on/after this date (YYYY-MM-DD). Overrides retention calculations.",
    )
    return parser.parse_args(argv)


def configure_logging() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def collect_rules(args: argparse.Namespace) -> Iterable[CleanupRule]:
    if not args.rules:
        yield from CLEANUP_RULES
        return

    filters = tuple(rule_filter.lower() for rule_filter in args.rules)
    matched = [
        rule
        for rule in CLEANUP_RULES
        if any(filter_key in rule.name.lower() for filter_key in filters)
    ]

    if not matched:
        available = ", ".join(rule.name for rule in CLEANUP_RULES)
        raise SystemExit(f"No cleanup rules matched filters: {args.rules!r}\n{available=}")

    for rule in matched:
        yield rule


def latest_modified(path: Path) -> datetime:
    """Return the most recent modification datetime for a path."""
    newest = path.stat().st_mtime
    if path.is_file():
        return datetime.fromtimestamp(newest, tz=timezone.utc)

    for entry in path.rglob("*"):
        try:
            newest = max(newest, entry.stat().st_mtime)
        except FileNotFoundError:
            continue
    return datetime.fromtimestamp(newest, tz=timezone.utc)


def directory_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size

    total = 0
    for entry in path.rglob("*"):
        try:
            if entry.is_file():
                total += entry.stat().st_size
        except FileNotFoundError:
            continue
    return total


def remove_path(path: Path, dry_run: bool) -> int:
    freed = directory_size(path)
    if dry_run:
        return freed

    if path.is_dir():
        shutil.rmtree(path, ignore_errors=False)
    else:
        path.unlink(missing_ok=True)
    return freed


def cleanup_files(rule: CleanupRule, base_path: Path, cutoff: datetime, dry_run: bool) -> tuple[int, int]:
    total_paths = 0
    total_bytes = 0

    if not base_path.exists():
        logging.debug("Skipping %s (missing path: %s)", rule.name, base_path)
        return total_paths, total_bytes

    globber = base_path.rglob if rule.recursive else base_path.glob
    for pattern in rule.patterns:
        for candidate in globber(pattern):
            if not candidate.exists() or candidate.is_dir():
                continue
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, tz=timezone.utc)
            if modified >= cutoff:
                continue
            freed = remove_path(candidate, dry_run=dry_run)
            total_paths += 1
            total_bytes += freed
            logging.info("Removed %s (%s)", candidate.relative_to(ROOT), human_readable(freed))
    return total_paths, total_bytes


def cleanup_subdirs(rule: CleanupRule, base_path: Path, cutoff: datetime, dry_run: bool) -> tuple[int, int]:
    total_paths = 0
    total_bytes = 0

    if not base_path.exists():
        logging.debug("Skipping %s (missing path: %s)", rule.name, base_path)
        return total_paths, total_bytes

    for child in base_path.iterdir():
        if not child.is_dir():
            continue
        try:
            modified = latest_modified(child)
        except FileNotFoundError:
            continue
        if modified >= cutoff:
            continue
        freed = remove_path(child, dry_run=dry_run)
        total_paths += 1
        total_bytes += freed
        logging.info("Removed directory %s (%s)", child.relative_to(ROOT), human_readable(freed))
    return total_paths, total_bytes


def human_readable(num_bytes: int) -> str:
    suffixes = ["B", "KB", "MB", "GB", "TB"]
    value = float(num_bytes)
    for suffix in suffixes:
        if value < 1024 or suffix == suffixes[-1]:
            return f"{value:.1f}{suffix}"
        value /= 1024
    return f"{value:.1f}TB"


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    configure_logging()

    dry_run = args.dry_run
    retention_override = args.retention_override
    now = datetime.now(tz=timezone.utc)

    keep_from: datetime | None = None
    if args.keep_from:
        if retention_override is not None:
            raise SystemExit("Cannot use --keep-from together with --retention-override.")
        try:
            keep_date = datetime.strptime(args.keep_from, "%Y-%m-%d").date()
        except ValueError as exc:
            raise SystemExit(f"Invalid --keep-from value '{args.keep_from}': {exc}") from exc
        keep_from = datetime.combine(keep_date, datetime.min.time(), tzinfo=timezone.utc)

    logging.info("Wingman cleanup starting (dry_run=%s)", dry_run)
    total_removed = 0
    total_bytes = 0

    for rule in collect_rules(args):
        if keep_from is not None:
            cutoff = keep_from
            retention_days = None
        else:
            retention_days = retention_override if retention_override is not None else rule.retention_days
            cutoff = now - timedelta(days=retention_days)
        base_path = ROOT / rule.relative_path
        logging.info(
            "Applying rule: %s | target=%s | retention=%sd | kind=%s",
            rule.name,
            base_path,
            "n/a (keep_from)" if retention_days is None else retention_days,
            rule.kind,
        )
        if rule.reason:
            logging.debug("Reason: %s", rule.reason)

        if rule.kind == "files":
            removed, freed = cleanup_files(rule, base_path, cutoff, dry_run)
        else:
            removed, freed = cleanup_subdirs(rule, base_path, cutoff, dry_run)

        total_removed += removed
        total_bytes += freed
        logging.info(
            "Rule summary: %s | removed=%s | reclaimed=%s",
            rule.name,
            removed,
            human_readable(freed),
        )

    logging.info(
        "Wingman cleanup complete | paths_removed=%s | total_reclaimed=%s",
        total_removed,
        human_readable(total_bytes),
    )

    if dry_run and total_removed:
        logging.info("Dry run: re-run without --dry-run to execute deletions.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
