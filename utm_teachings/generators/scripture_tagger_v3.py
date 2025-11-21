"""
UTM Scripture Tagger – Phase 3
Theme scoring • Primary/Secondary Theme Detection • Cross-Reference Framework
Teaching Outline Export • Profile-Based Output • Configurable Rules
"""

from pathlib import Path
import json
from collections import Counter


# ---------------------------
# CONFIGURATION
# ---------------------------

THEME_KEYWORDS = {
    "identity": ["chosen", "people", "israel", "yah", "tribe", "nation"],
    "covenant": ["law", "commandments", "statutes", "covenant", "keep", "obey"],
    "judgment": ["punish", "destruction", "wrath", "judge", "scatter"],
    "prophecy": ["shall come", "in that day", "behold", "prophesy", "future"],
    "truth": ["truth", "light", "wisdom", "knowledge", "word"],
    "warning": ["beware", "take heed", "lest", "danger", "turn away"],
}

# Weight per theme occurrence
THEME_WEIGHTS = {
    "identity": 1.0,
    "covenant": 1.0,
    "judgment": 1.2,
    "prophecy": 1.3,
    "truth": 0.8,
    "warning": 1.1,
}

# Placeholder cross-reference map (expand in Phase 4)
CROSS_REFERENCE_MAP = {
    "identity": ["Deut 7:6", "Exo 19:5"],
    "covenant": ["Deut 4:1", "Jer 31:31"],
    "judgment": ["Lev 26:14-33", "Amos 3:2"],
    "prophecy": ["Isa 2:2", "Joel 2:28"],
    "truth": ["Psa 119:142", "John 17:17"],
    "warning": ["Deut 28:15-68", "Matt 24:4"],
}


# ---------------------------
# THEME ANALYSIS
# ---------------------------

def score_themes(text: str) -> dict:
    """
    Returns:
    - theme counts
    - weighted score
    - primary theme
    - secondary themes
    """
    lower = text.lower()
    theme_counter = Counter()

    # count occurrences
    for theme, keywords in THEME_KEYWORDS.items():
        for k in keywords:
            if k in lower:
                theme_counter[theme] += 1

    if not theme_counter:
        return {
            "themes": ["uncategorized"],
            "primary": "uncategorized",
            "secondary": [],
            "score": 0.0,
        }

    # weighted score
    score = sum(theme_counter[t] * THEME_WEIGHTS.get(t, 1.0) for t in theme_counter)

    # sort by frequency & weight
    sorted_themes = sorted(theme_counter.items(), key=lambda x: (-x[1], -THEME_WEIGHTS[x[0]]))
    primary = sorted_themes[0][0]
    secondary = [t for t, _ in sorted_themes[1:]]

    return {
        "themes": list(theme_counter.keys()),
        "primary": primary,
        "secondary": secondary,
        "score": round(float(score), 3),
    }


# ---------------------------
# CROSS-REFERENCE GENERATION
# ---------------------------

def generate_cross_references(primary_theme: str):
    return CROSS_REFERENCE_MAP.get(primary_theme, [])


# ---------------------------
# MAIN TAGGING
# ---------------------------

def tag_verse(reference: str, text: str):
    analysis = score_themes(text)
    cross_refs = generate_cross_references(analysis["primary"])

    return {
        "reference": reference,
        "text": text.strip(),
        "themes": analysis["themes"],
        "primary_theme": analysis["primary"],
        "secondary_themes": analysis["secondary"],
        "score": analysis["score"],
        "cross_references": cross_refs,
    }


# ---------------------------
# EXPORT FORMATS
# ---------------------------

def export_teaching_outline(tagged, output_file: Path):
    with output_file.open("w", encoding="utf-8") as f:
        f.write("# UTM Phase 3 – Teaching Outline\n\n")

        for entry in tagged:
            f.write(f"## {entry['reference']} — {entry['primary_theme'].upper()}\n")
            f.write(f"{entry['text']}\n\n")
            f.write(f"Primary Theme: **{entry['primary_theme']}**\n")
            f.write(f"Score: {entry['score']}\n")
            f.write(f"Secondary: {', '.join(entry['secondary_themes']) or 'None'}\n")
            f.write(f"Cross-References: {', '.join(entry['cross_references'])}\n")
            f.write("\n---\n\n")


def export_json(tagged, output_file: Path):
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(tagged, f, indent=4, ensure_ascii=False)


# ---------------------------
# PROCESSOR
# ---------------------------

def process_scripture_file(input_file: Path):
    tagged = []

    with input_file.open("r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue

            ref, text = line.split("|", 1)
            tagged.append(tag_verse(ref.strip(), text.strip()))

    return tagged


# ---------------------------
# ENTRY POINT
# ---------------------------

if __name__ == "__main__":
    base = Path(__file__).resolve().parent

    input_file = base / "verses_input.txt"
    outline_output = base / "teaching_outline_v3.md"
    json_output = base / "tagged_output_v3.json"

    tagged_verses = process_scripture_file(input_file)

    export_teaching_outline(tagged_verses, outline_output)
    export_json(tagged_verses, json_output)

    print("✔ Phase 3 tagging completed.")
    print("Outline:", outline_output)
    print("JSON:", json_output)
