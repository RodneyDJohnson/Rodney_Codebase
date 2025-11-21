"""
UTM Study Pack Builder – Phase 6
Builds themed study packs from previously tagged scripture JSON.

Usage example:

    cd ~/Rodney_Codebase/utm_teachings/generators
    python3 study_pack_builder.py \
        --source tagged_output_v3.json \
        --themes identity,covenant \
        --max-per-theme 5 \
        --title "Identity & Covenant Study Session"

"""


from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Dict, Set


def load_tagged_verses(source: Path) -> List[Dict]:
    """Load tagged verse data from a JSON file."""
    if not source.exists():
        raise FileNotFoundError(f"Source JSON not found: {source}")

    with source.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected list of verse entries in JSON.")

    return data


def list_themes(tagged_data: List[Dict]) -> Set[str]:
    """Return a set of all themes present in the tagged data."""
    themes: Set[str] = set()

    for entry in tagged_data:
        entry_themes = entry.get("themes", [])
        for t in entry_themes:
            themes.add(str(t).strip())

    return themes


def filter_by_themes(
    tagged_data: List[Dict],
    target_themes: List[str],
    max_per_theme: int | None = None,
) -> List[Dict]:
    """
    Filter verses that match any of the requested themes.
    If max_per_theme is given, cap number of verses per theme.
    """

    normalized_targets = [t.strip().lower() for t in target_themes if t.strip()]
    if not normalized_targets:
        return []

    per_theme_count = {t: 0 for t in normalized_targets}
    results: List[Dict] = []

    for entry in tagged_data:
        entry_themes = [str(t).lower() for t in entry.get("themes", [])]
        matched = [t for t in normalized_targets if t in entry_themes]

        if not matched:
            continue

        # Respect max_per_theme if set
        for theme in matched:
            if max_per_theme is not None and per_theme_count[theme] >= max_per_theme:
                continue  # skip if this theme has hit its cap

            per_theme_count[theme] += 1
            results.append(entry)
            break  # avoid duplicating same entry multiple times

    return results


def export_study_pack_markdown(
    verses: List[Dict],
    output_file: Path,
    title: str,
    session_notes: str | None = None,
    themes_used: List[str] | None = None,
) -> None:
    """Write a markdown study pack file from selected verses."""
    with output_file.open("w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")

        if themes_used:
            f.write(f"**Themes:** {', '.join(themes_used)}\n\n")

        if session_notes:
            f.write(f"> {session_notes}\n\n")

        f.write("---\n\n")

        for entry in verses:
            ref = entry.get("reference", "Unknown reference")
            text = entry.get("text", "").strip()
            themes = entry.get("themes", [])

            f.write(f"## {ref}\n\n")
            f.write(f"{text}\n\n")
            if themes:
                f.write(f"_Tags:_ {', '.join(themes)}\n\n")
            f.write("---\n\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="UTM Phase 6 – Build themed study packs from tagged scripture JSON."
    )

    parser.add_argument(
        "--source",
        type=str,
        default="tagged_output_v3.json",
        help="Path to tagged JSON file (default: tagged_output_v3.json)",
    )

    parser.add_argument(
        "--themes",
        type=str,
        default="",
        help="Comma-separated list of themes to include (e.g. identity,covenant,truth).",
    )

    parser.add_argument(
        "--max-per-theme",
        type=int,
        default=None,
        help="Maximum number of verses per theme (optional).",
    )

    parser.add_argument(
        "--title",
        type=str,
        default="UTM Study Pack",
        help="Title for the study pack.",
    )

    parser.add_argument(
        "--notes",
        type=str,
        default="",
        help="Short session notes or purpose statement for the pack.",
    )

    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="Only list available themes from the source JSON and exit.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    base_dir = Path(__file__).resolve().parent
    source_path = (base_dir / args.source).resolve()

    tagged_data = load_tagged_verses(source_path)

    if args.list_themes:
        themes = list_themes(tagged_data)
        print("Available themes:")
        for t in sorted(themes):
            print(f" - {t}")
        return

    raw_themes = [t.strip() for t in args.themes.split(",") if t.strip()]
    if not raw_themes:
        print("No themes specified. Use --themes or --list-themes to inspect options.")
        return

    filtered = filter_by_themes(
        tagged_data=tagged_data,
        target_themes=raw_themes,
        max_per_theme=args.max_per_theme,
    )

    if not filtered:
        print("No verses matched the requested themes.")
        return

    output_file = base_dir / "study_pack_phase6.md"

    session_notes = args.notes.strip() or None

    export_study_pack_markdown(
        verses=filtered,
        output_file=output_file,
        title=args.title,
        session_notes=session_notes,
        themes_used=raw_themes,
    )

    print("✔ Study pack generated.")
    print("File:", output_file)


if __name__ == "__main__":
    main()
