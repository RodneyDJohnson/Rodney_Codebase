# UTM Scripture Tagger – Phase 4
# Output Engine: JSON, Markdown, CSV, Pretty Text
# Adds --json, --md, --csv, --all switches

import json
import csv
import argparse
from pathlib import Path
from datetime import datetime
from scripture_tagger_v3 import tag_verse, process_scripture_file


def ensure_dirs(base: Path):
    """Create output directories if missing."""
    (base / "json").mkdir(parents=True, exist_ok=True)
    (base / "markdown").mkdir(parents=True, exist_ok=True)
    (base / "csv").mkdir(parents=True, exist_ok=True)
    (base / "text").mkdir(parents=True, exist_ok=True)


def save_json(data, output_path: Path, meta):
    bundle = {"metadata": meta, "verses": data}
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=4, ensure_ascii=False)


def save_markdown(data, output_path: Path, meta):
    with output_path.open("w", encoding="utf-8") as f:
        f.write("# UTM Tagged Scripture Output – Phase 4\n")
        f.write(f"Generated: {meta['timestamp']}\n")
        f.write(f"Script Version: {meta['version']}\n")
        f.write(f"Total Verses: {meta['total']}\n\n")

        for entry in data:
            f.write(f"## {entry['reference']}\n")
            f.write(f"{entry['text']}\n\n")
            f.write(f"**Themes:** {', '.join(entry['themes'])}\n\n---\n\n")


def save_csv(data, output_path: Path):
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["reference", "text", "themes"])

        for e in data:
            writer.writerow([e["reference"], e["text"], ", ".join(e["themes"])])


def save_text(data, output_path: Path):
    with output_path.open("w", encoding="utf-8") as f:
        for e in data:
            f.write(f"{e['reference']} :: {', '.join(e['themes'])}\n")
            f.write(f"{e['text']}\n")
            f.write("-" * 40 + "\n")


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    export_base = base / "../exports/v3"
    export_base.mkdir(parents=True, exist_ok=True)
    ensure_dirs(export_base)

    parser = argparse.ArgumentParser(description="UTM Scripture Tagger – Phase 4 Output Engine")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--md", action="store_true")
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--all", action="store_true")

    args = parser.parse_args()

    input_file = base / "verses_input.txt"
    tagged = process_scripture_file(input_file)

    meta = {
        "version": "3.0",
        "timestamp": datetime.now().isoformat(),
        "total": len(tagged),
    }

    if args.all or args.json:
        save_json(tagged, export_base / "json/tagged_output_v3.json", meta)

    if args.all or args.md:
        save_markdown(tagged, export_base / "markdown/tagged_output_v3.md", meta)

    if args.all or args.csv:
        save_csv(tagged, export_base / "csv/tagged_output_v3.csv")

    if args.all or args.text:
        save_text(tagged, export_base / "text/tagged_output_v3.txt")

    print("✔ Phase 4 outputs generated successfully.")
