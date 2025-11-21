# UTM Scripture Tagger – Phase 2
# Adds theme detection, keyword tagging, and export formats.

from pathlib import Path
import json


THEME_KEYWORDS = {
    "identity": ["chosen", "people", "israel", "yah", "tribe", "nation"],
    "covenant": ["law", "commandments", "statutes", "covenant", "keep", "obey"],
    "judgment": ["punish", "destruction", "wrath", "judge", "scatter"],
    "prophecy": ["shall come", "in that day", "behold", "prophesy", "future"],
    "truth": ["truth", "light", "wisdom", "knowledge", "word"],
    "warning": ["beware", "take heed", "lest", "danger", "turn away"],
}


def detect_themes(verse_text: str):
    """Return a list of detected themes based on keywords."""
    lower = verse_text.lower()
    found = []

    for theme, keywords in THEME_KEYWORDS.items():
        if any(k in lower for k in keywords):
            found.append(theme)

    return found or ["uncategorized"]


def tag_verse(reference: str, text: str):
    """Return a structured dictionary for the tagged verse."""
    themes = detect_themes(text)

    return {
        "reference": reference,
        "text": text.strip(),
        "themes": themes,
    }


def export_markdown(tagged_data, output_file: Path):
    with output_file.open("w", encoding="utf-8") as f:
        f.write("# UTM Tagged Scripture Output (Phase 2)\n\n")
        for entry in tagged_data:
            f.write(f"## {entry['reference']}\n")
            f.write(f"{entry['text']}\n\n")
            f.write(f"**Themes:** {', '.join(entry['themes'])}\n\n---\n\n")


def export_json(tagged_data, output_file: Path):
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(tagged_data, f, indent=4, ensure_ascii=False)


def process_scripture_file(input_file: Path):
    """Reads a text file where each line is formatted:
       Book Chapter:Verse | Scripture text
    """
    tagged = []

    with input_file.open("r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue

            ref, text = line.split("|", 1)
            tagged.append(tag_verse(ref.strip(), text.strip()))

    return tagged


if __name__ == "__main__":
    base = Path(__file__).resolve().parent

    input_file = base / "verses_input.txt"  # <-- YOU CREATE THIS FILE
    md_output = base / "tagged_output_v2.md"
    json_output = base / "tagged_output_v2.json"

    tagged_verses = process_scripture_file(input_file)

    export_markdown(tagged_verses, md_output)
    export_json(tagged_verses, json_output)

    print("✔ Phase 2 tagging completed.")
    print("Markdown output:", md_output)
    print("JSON output:", json_output)
