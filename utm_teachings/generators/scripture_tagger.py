# UTM Scripture Tagger – Phase 1
# Loads a list of verses, applies simple themes, exports tagged results.

from pathlib import Path


def load_verses(file_path: str) -> list:
    """
    Loads a list of verses from a text file.
    Each line should contain one verse reference.
    Example:
        Genesis 1:1
        Exodus 20:2
    """
    path = Path(file_path)

    if not path.exists():
        print(f"[ERROR] Verse list not found: {path}")
        return []

    verses = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    return verses


def tag_verse(verse: str) -> str:
    """
    Applies simple theme tags.
    Later versions will be AI-assisted.
    """

    v = verse.lower()

    if any(word in v for word in ["judgment", "wrath", "destroy"]):
        return "Judgment"
    if any(word in v for word in ["covenant", "law", "command"]):
        return "Covenant"
    if any(word in v for word in ["truth", "light"]):
        return "Truth"
    if any(word in v for word in ["prophet", "vision"]):
        return "Prophecy"
    if any(word in v for word in ["israel", "tribe", "hebrew"]):
        return "Identity"

    return "General"


def tag_verses(verse_list: list) -> list:
    """
    Returns a list of dictionaries:
    [
      {'verse': 'Genesis 1:1', 'theme': 'Covenant'},
      ...
    ]
    """
    tagged = []
    for v in verse_list:
        tagged.append({"verse": v, "theme": tag_verse(v)})
    return tagged


def export_tagged(data: list, export_path: str) -> None:
    """
    Writes tagged results to a markdown report for teaching.
    """
    lines = ["# Tagged Scriptures\n"]
    for item in data:
        lines.append(f"- **{item['verse']}** → *{item['theme']}*")
    Path(export_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Exported tagged list to {export_path}")


if __name__ == "__main__":
    # Example test (later you will replace these):
    verse_list = ["Genesis 1:1", "Exodus 20:2", "Isaiah 1:3", "John 8:32"]

    tagged = tag_verses(verse_list)
    export_tagged(tagged, "tagged_output.md")

