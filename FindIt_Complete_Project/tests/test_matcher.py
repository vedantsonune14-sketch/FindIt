import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from matcher import (
    calculate_match,
    keyword_overlap,
    normalize_text,
    rank_matches,
)


class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.lost = {
            "item_name": "Casio Scientific Calculator",
            "category": "Electronics",
            "color": "Black",
            "location": "Computer Laboratory",
            "description": "Black calculator with scratch near display",
        }

    def test_normalization(self):
        self.assertEqual(normalize_text("  Black-CALCULATOR! "), "black calculator")

    def test_exact_match_scores_high(self):
        found = {
            **self.lost,
            "location": "Computer Lab",
        }
        result = calculate_match(self.lost, found)
        self.assertGreaterEqual(result["score"], 75)
        self.assertEqual(result["strength"], "Strong possible match")

    def test_partial_match(self):
        found = {
            "item_name": "Scientific Calculator",
            "category": "Electronics",
            "color": "Grey",
            "location": "Computer Lab",
            "description": "calculator near display",
        }
        result = calculate_match(self.lost, found)
        self.assertGreater(result["score"], 0)
        self.assertLess(result["score"], 100)

    def test_unrelated_item_scores_lower(self):
        found = {
            "item_name": "Black Umbrella",
            "category": "Other",
            "color": "Black",
            "location": "Parking Area",
            "description": "foldable umbrella",
        }
        result = calculate_match(self.lost, found)
        self.assertLess(result["score"], 45)

    def test_empty_fields_do_not_match(self):
        found = {
            "item_name": "",
            "category": "",
            "color": "",
            "location": "",
            "description": "",
        }
        result = calculate_match(self.lost, found)
        self.assertEqual(result["score"], 0)

    def test_keyword_overlap(self):
        ratio, shared = keyword_overlap(
            "black calculator near display",
            "calculator black with display"
        )
        self.assertGreater(ratio, 0)
        self.assertTrue({"black", "calculator", "display"} <= shared)

    def test_ranked_descending(self):
        found_reports = [
            {**self.lost, "id": 1},
            {
                "item_name": "Umbrella", "category": "Other", "color": "Red",
                "location": "Parking", "description": "foldable"
            },
        ]
        results = rank_matches(self.lost, found_reports)
        self.assertGreaterEqual(results[0]["score"], results[1]["score"])


if __name__ == "__main__":
    unittest.main()
