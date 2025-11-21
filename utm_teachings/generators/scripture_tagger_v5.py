"""
UTM Scripture Tagger – Phase 5
Advanced Output Publishing Engine

Features:
- Theme-based grouped output
- Full Markdown report with TOC
- Facebook/website snippet generator
- Slide deck outline (JSON + MD)
- Version stamping
"""

from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict


VERSION = "Phase 5.0"


def group_by_theme(tagged_data):
    """Group verses by their themes."""
    theme_groups = defaultdict(list)
    for entry in tagged_data:
        for theme in entry["themes"]:
            theme_groups[theme].append(entry)
    return theme_groups


def export_markdown_report(tagged_data, output_file: Path):
    groups = group_by_theme(tagged_data)

    with output_file.open("w", encoding="utf-8") as f:
        f.write(f"# UTM Tagged Scripture Report\n")
        f.write(f"### Version: {VERSION}\n")
        f.write(f"### Generated: {datetime.now()}\n\n")
        f.write("## Table of Contents\n")
        for theme in groups:
            f.write(f"- [{theme.title()}](#{theme})\n")
        f.write("\n---\n\n")

        for theme, verses in groups.items():
            f.write(f"## {theme}\n\n")
            for v in verses:
                f.write(f"### {v['reference']}\n")
                f.write(f"{v['text']}\n\n")
            f.write("\n---\n")


def export_slide_outline(tagged_data, output_json: Path, output_md: Path):
    """Creates a slide-friendly structure."""
    slides = []
    groups = group_by_theme(tagged_data)

    # Title slide
    slides.append({
        "type": "title",
        "title": "UTM Teaching – Tagged Scripture Breakdown",
        "version": VERSION
    })

    # Theme slides
    for theme, verses in groups.items():
        slides.append({
            "type": "theme",
            "theme": theme,
            "bullet_points": [f"{v['reference']}: {v['text']}" for v in verses]
        })

    # Write JSON
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(slides, f, indent=4, ensure_ascii=False)

    # Write Markdown outline
    with output_md.open("w", encoding="utf-8") as f:
        f.write("# Slide Deck Outline\n\n")
        for s in slides:
            if s["type"] == "title":
                f.write(f"# {s['title']}\n")
                f.write(f"**Version:** {VERSION}\n\n")
            else:
                f.write(f"## {s['theme'].title()}\n")
                for b in s["bullet_points"]:
                    f.write(f"- {b}\n")
                f.write("\n")


def export_social_snippets(tagged_data, output_file: Path):
    """Generates short UTM truth posts + hashtags."""
    with output_file.open("w", encoding="utf-8") as f:
        f.write("# Social Media Snippets\n\n")
        for entry in tagged_data:
            summary = entry["text"]
            themes = entry["themes"]

            hashtags = " ".join([f"#{t.lower()}" for t in themes])
            hashtags += " #unitedtruthministry #scripture #truth"

            f.write(f"**{entry['reference']}** – {summary}\n")
            f.write(f"{hashtags}\n\n---\n\n")


def process_v3_export(input_json: Path):
    """Phase 5 operates from v3 JSON output."""
    with input_json.open("r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    base = Path(__file__).resolve().parent

    v3_file = base / "tagged_output_v3.json"   # generated in Phase 3–4
    tagged = process_v3_export(v3_file)

    export_markdown_report(tagged, base / "tagged_output_v5.md")
    export_slide_outline(tagged, base / "slides_v5.json", base / "slides_v5.md")
    export_social_snippets(tagged, base / "social_snippets_v5.md")

    print("✔ PHASE 5 complete.")
    print("Generated outputs:")
    print("- Markdown Report: tagged_output_v5.md")
    print("- Slide JSON:      slides_v5.json")
    print("- Slide MD:        slides_v5.md")
    print("- Social Posts:    social_snippets_v5.md")
