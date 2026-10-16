import re
from difflib import SequenceMatcher
from typing import Dict, List, Set, Tuple

WEIGHTS = {
    "category": 30,
    "item_name": 25,
    "color": 15,
    "location": 15,
    "description": 15,
}

GENERIC_WORDS = {
    "item", "found", "lost", "thing", "object", "the", "a", "an",
    "and", "or", "near", "at", "in", "with", "my", "was", "is",
    "this", "that", "college", "student"
}


def normalize_text(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> Set[str]:
    words = set(normalize_text(text).split())
    return {word for word in words if len(word) > 1 and word not in GENERIC_WORDS}


def similarity(a: str, b: str) -> float:
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)
    if not a_norm or not b_norm:
        return 0.0
    return SequenceMatcher(None, a_norm, b_norm).ratio()


def exact_nonempty_match(a: str, b: str) -> bool:
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)
    return bool(a_norm and b_norm and a_norm == b_norm)


def location_score(a: str, b: str) -> float:
    """Return 0..1 using exact, token overlap, or substring similarity."""
    a_norm = normalize_text(a)
    b_norm = normalize_text(b)
    if not a_norm or not b_norm:
        return 0.0
    if a_norm == b_norm:
        return 1.0
    if a_norm in b_norm or b_norm in a_norm:
        return 0.9

    a_words = tokenize(a_norm)
    b_words = tokenize(b_norm)
    if a_words and b_words:
        overlap = len(a_words & b_words) / len(a_words | b_words)
        if overlap > 0:
            return overlap

    return similarity(a_norm, b_norm)


def keyword_overlap(a: str, b: str) -> Tuple[float, Set[str]]:
    a_words = tokenize(a)
    b_words = tokenize(b)
    if not a_words or not b_words:
        return 0.0, set()
    shared = a_words & b_words
    ratio = len(shared) / len(a_words | b_words)
    return ratio, shared


def match_strength(score: float) -> str:
    if score >= 75:
        return "Strong possible match"
    if score >= 45:
        return "Possible match"
    return "Weak match"


def calculate_match(lost: Dict, found: Dict) -> Dict:
    points = 0.0
    reasons: List[str] = []

    if exact_nonempty_match(lost.get("category", ""), found.get("category", "")):
        points += WEIGHTS["category"]
        reasons.append("Category matches")

    name_sim = similarity(lost.get("item_name", ""), found.get("item_name", ""))
    name_points = name_sim * WEIGHTS["item_name"]
    points += name_points
    if name_sim >= 0.75:
        reasons.append(f"Item name is very similar ({name_sim:.0%})")
    elif name_sim >= 0.45:
        reasons.append(f"Item name is partly similar ({name_sim:.0%})")

    if exact_nonempty_match(lost.get("color", ""), found.get("color", "")):
        points += WEIGHTS["color"]
        reasons.append("Color matches")

    loc_sim = location_score(lost.get("location", ""), found.get("location", ""))
    loc_points = loc_sim * WEIGHTS["location"]
    points += loc_points
    if loc_sim >= 0.75:
        reasons.append("Location is very similar")
    elif loc_sim >= 0.45:
        reasons.append("Location is partly similar")

    desc_ratio, shared = keyword_overlap(
        lost.get("description", ""), found.get("description", "")
    )
    desc_points = desc_ratio * WEIGHTS["description"]
    points += desc_points
    if shared:
        reasons.append("Shared description keywords: " + ", ".join(sorted(shared)[:6]))

    score = round(min(points, 100), 1)
    if not reasons:
        reasons.append("No strong attributes matched")

    return {
        "score": score,
        "strength": match_strength(score),
        "reasons": reasons,
    }


def rank_matches(lost_report: Dict, found_reports: List[Dict]) -> List[Dict]:
    results = []
    for found in found_reports:
        result = calculate_match(lost_report, found)
        result["report"] = found
        results.append(result)

    results.sort(key=lambda item: item["score"], reverse=True)
    return results
