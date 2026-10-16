# FindIt — Smart Lost-and-Found Matcher

## 1. Abstract

FindIt is a local desktop application for college lost-and-found management. Users can record lost and found belongings in an SQLite database. For an active lost report, FindIt compares it with active found reports and ranks possible candidates using a weighted heuristic score.

The project demonstrates practical DSA concepts including dictionaries/hash-map style lookups, sets, sorting, string similarity, tokenization and weighted scoring.

A match score is a ranking aid only. It does not prove ownership.

## 2. Problem Statement

College campuses frequently have lost belongings, but manually checking notices or asking around is slow. FindIt provides a structured local system in which lost and found reports can be searched and possible matches can be ranked automatically.

## 3. Objectives

- Store lost and found reports persistently.
- Validate basic user input.
- Search and filter reports.
- Rank active found reports against a selected lost report.
- Explain which attributes contributed to a match.
- Provide controlled access to stored contact details through a View Contact action.
- Allow reports to be edited, deleted and marked as reunited.
- Demonstrate core DSA concepts in an understandable Python application.

## 4. Scope

FindIt is designed as a college mini-project and local demonstration. It is not a campus-wide cloud service. It does not provide authentication, internet synchronization, automatic notifications, GPS, AI/ML or external APIs.

## 5. Hardware and Software Requirements

### Hardware
- Windows laptop/desktop
- 4 GB RAM or more recommended
- Normal display

### Software
- Python 3
- VS Code or another Python IDE
- Windows Terminal / PowerShell / Command Prompt

No third-party Python packages are required.

## 6. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application programming |
| Tkinter / ttk | Desktop GUI |
| SQLite / sqlite3 | Local persistent database |
| difflib | Item-name string similarity |
| unittest | Automated matcher tests |

## 7. Features

- Dashboard with live statistics
- Lost-item reporting
- Found-item reporting
- SQLite persistence
- Search and filters
- Edit/delete reports
- Reunited and Closed statuses
- Ranked matching results
- Match explanations
- View Contact dialog
- Fictional sample data
- First-run database creation
- Automated unit tests

## 8. DSA Concepts Used

### Dictionaries / hash maps

Python dictionaries are used to represent database records in the application and to map report IDs to selected match results in the GUI. Database primary-key lookup provides the persistent equivalent of an ID-based lookup.

### Sets

Description text is tokenized into sets of meaningful words. Set intersection identifies shared keywords.

### Sorting

Candidate results are sorted by score in descending order. Python's `sort()` uses an efficient comparison-based sorting implementation.

### String similarity

`difflib.SequenceMatcher` produces a ratio between 0 and 1. This helps compare names such as `Casio Scientific Calculator` and `Scientific Calculator`.

### Weighted scoring

The score is out of 100:

- Category: 30
- Item name: 25
- Color: 15
- Location: 15
- Description keywords: 15

These values are heuristic weights, not statistically validated probabilities.

## 9. System Architecture

```text
+-----------------------+
|      Tkinter GUI      |
|        gui.py         |
+-----------+-----------+
            |
     +------+------+
     |             |
     v             v
+---------+   +-----------+
|database |   |  matcher  |
|  .py    |   |   .py     |
+----+----+   +-----------+
     |
     v
+-----------+
| SQLite DB |
| findit.db |
+-----------+

sample_data.py -> database.py
tests/test_matcher.py -> matcher.py
```

The GUI is separated from database and matching logic so the matcher can be tested independently.

## 10. Matching Algorithm

1. Select an active lost report.
2. Retrieve active found reports from SQLite.
3. Normalize text by lowercasing, trimming and removing punctuation.
4. Compare categories for equality.
5. Calculate item-name similarity with `SequenceMatcher`.
6. Compare colors when both values are non-empty.
7. Compare locations using exact match, substring/token overlap and string similarity.
8. Extract meaningful description keywords into sets.
9. Calculate weighted points.
10. Cap the score at 100.
11. Assign a strength label:
   - 75–100: Strong possible match
   - 45–74: Possible match
   - Below 45: Weak match
12. Sort all candidates by score.
13. Show the reasons behind each result.
14. Never automatically declare ownership or reunion.

## 11. Pseudocode

```text
FUNCTION rank_matches(lost_report, found_reports):
    results = empty list

    FOR each found_report:
        score = 0

        IF non-empty categories are equal:
            score += 30

        name_similarity = string_similarity(lost.name, found.name)
        score += name_similarity * 25

        IF non-empty colors are equal:
            score += 15

        location_similarity = location_score(lost.location, found.location)
        score += location_similarity * 15

        lost_words = meaningful_words(lost.description)
        found_words = meaningful_words(found.description)
        overlap = intersection(lost_words, found_words)
        score += overlap_ratio * 15

        append candidate with score and explanation

    SORT results by score descending
    RETURN results
```

## 12. Time and Space Complexity

Let `N` be the number of active found reports and `L` represent the average text length.

- Matching all candidates: approximately `O(N * L)` for the text comparisons.
- Ranking: `O(N log N)` for sorting.
- Keyword sets use space proportional to the number of extracted words.
- Overall practical complexity is dominated by candidate matching and sorting.

For a college-sized local database, this is more than sufficient.

## 13. Database Design

The SQLite database contains one main table: `reports`.

Important columns:

- `id`: primary key
- `report_type`: `lost` or `found`
- `item_name`
- `category`
- `color`
- `location`
- `report_date`
- `description`
- `reporter_name`
- `contact_type`
- `contact_info`
- `status`: `Active`, `Reunited`, or `Closed`
- `created_at`

The database is created automatically on first launch.

## 14. Installation and Execution

Open PowerShell in the project folder:

```powershell
cd FindIt
python --version
python main.py
```

If the `python` command is not available on Windows, try:

```powershell
py main.py
```

No `pip install` command is required.

### VS Code

1. Open the `FindIt` folder in VS Code.
2. Select a Python 3 interpreter.
3. Open the integrated terminal.
4. Run:

```powershell
python main.py
```

The first launch creates `findit.db` automatically.

## 15. Testing Procedure

Run:

```powershell
python -m unittest discover -s tests -v
```

The tests cover:

- Text normalization
- Exact matches
- Partial matches
- Unrelated reports
- Empty optional fields
- Keyword overlap
- Descending ranking

Manual GUI tests should cover:

1. Submit an empty lost form.
2. Enter an invalid date.
3. Save a report without contact information.
4. Load demo data twice.
5. Select a lost report and click Find Matches.
6. Verify results are sorted by score.
7. View a candidate's contact information.
8. Edit a report.
9. Delete a report.
10. Mark a report as reunited and verify it no longer appears in active matching.

## 16. Privacy and Ownership Safeguards

- Contact details are not shown in normal report tables.
- Contact details are shown only through the View Contact action.
- Contact information is local to the computer/database.
- The application does not send email, SMS or WhatsApp messages.
- A score is not proof of ownership.
- Users should verify a private identifying feature before returning an item.
- Reunited status should only be used after the return is actually confirmed.

This is a local single-computer application and does not provide strong security against someone who can access the same computer or database.

## 17. Limitations

- No login/authentication.
- No cloud synchronization.
- No multi-computer collaboration.
- No automatic notifications.
- No GPS/live maps.
- Heuristic matching is not a probability model.
- SQLite is intended here for local college-scale use.
- Contact information is only as accurate as what the reporter enters.

## 18. Future Enhancements

- Optional campus server/database.
- Authentication and role-based access.
- Email notification through a controlled backend.
- Better fuzzy matching.
- Date-distance weighting.
- Image-based item comparison.
- Admin dashboard.
- Audit logs.
- Export to CSV/PDF.
- Campus-wide deployment.

## 19. Conclusion

FindIt converts a common campus problem into a practical DSA application. It combines persistent storage, GUI programming and understandable algorithms. The weighted matching engine demonstrates how data structures and string processing can support a real-world decision-support feature without requiring machine learning or external services.

## Project Structure

```text
FindIt/
├── main.py
├── gui.py
├── matcher.py
├── database.py
├── sample_data.py
├── README.md
├── tests/
│   └── test_matcher.py
└── findit.db          # created automatically after first run
```
