# 🔎 FindIt — Smart Lost-and-Found Matcher

A Python desktop application that helps college students manage lost and found belongings by automatically ranking potential matches using a weighted text-similarity algorithm.

## 📌 Overview

Finding lost belongings on a college campus can be difficult and time-consuming. **FindIt** provides a simple desktop-based solution where users can report lost and found items, search existing reports, and discover potential matches.

The application uses Python, Tkinter, and SQLite, with a custom matching algorithm that compares item names, categories, colors, locations, and descriptions to rank possible matches.

> **Note:** Match scores are heuristic rankings, not probabilities or proof of ownership.

## ✨ Features

- 📝 **Lost Item Reporting** — Submit details about lost belongings.
- 📦 **Found Item Reporting** — Record items that have been found.
- 🔍 **Smart Matching** — Rank potential matches automatically.
- 📊 **Match Scores** — View scores and explanations for candidate matches.
- 🔎 **Search and Filters** — Find reports using available search and filtering options.
- 💾 **Persistent Storage** — Save reports using an SQLite database.
- ✏️ **Report Management** — Edit and delete reports.
- ✅ **Item Status Tracking** — Mark items as reunited or closed.
- 🔐 **Contact Privacy** — View reporter contact details through a dedicated action.
- 🧪 **Automated Tests** — Test the matching logic using Python's `unittest` framework.
- 🖥️ **Desktop Interface** — Use the application through a Tkinter GUI.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core application logic |
| Tkinter / ttk | Desktop graphical interface |
| SQLite | Local database storage |
| `sqlite3` | Python database connectivity |
| `difflib` | String similarity comparison |
| Dictionaries | Record and result lookups |
| Sets | Description keyword comparison |
| `unittest` | Automated testing |

**Dependencies:** The project uses Python's standard library and does not require third-party packages.

## 🧠 Matching Algorithm

FindIt uses a weighted heuristic scoring algorithm to rank active found-item reports against a selected lost-item report.

### Scoring criteria

| Attribute | Maximum Score |
|---|---:|
| Category match | 30 |
| Item name similarity | 25 |
| Color match | 15 |
| Location similarity | 15 |
| Description keyword overlap | 15 |
| **Total** | **100** |

### How matching works

1. Select an active lost-item report.
2. Retrieve active found-item reports from the database.
3. Normalize text by converting it to lowercase and removing punctuation.
4. Compare categories and item names.
5. Compare colors and locations where information is available.
6. Extract meaningful keywords from descriptions and compare them using sets.
7. Calculate the weighted score for each candidate.
8. Sort candidates by score in descending order.
9. Display candidate rankings with explanations.

### Match strength

| Score | Classification |
|---|---|
| 75–100 | Strong possible match |
| 45–74 | Possible match |
| Below 45 | Weak match |

These thresholds are configurable heuristic rules, not statistically validated confidence levels.

## 📋 Requirements

- Windows 10 or Windows 11
- Python 3
- Visual Studio Code or another Python IDE
- Git (optional, for cloning the repository)

No external database server or third-party Python package is required.

## 🚀 Installation and Setup

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPOSITORY` with your repository name.

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Open the project folder

Open the extracted or cloned project folder in Visual Studio Code.

### 3. Verify Python

Open the VS Code integrated terminal using **Terminal → New Terminal**.

Run:

```powershell
py --version
```

If the command is unavailable, install Python from [python.org](https://www.python.org/downloads/windows/).

### 4. Run the application

From the directory containing `main.py`, execute:

```powershell
py main.py
```

Alternatively:

```powershell
python main.py
```

The application should open in a separate desktop window.

The SQLite database is initialized automatically when the application starts.

## 🧪 Running Tests

Run the automated test suite from the project root:

```powershell
py -m unittest discover -s tests -v
```

The tests cover matching-related functionality, including text normalization, similarity, keyword overlap, and candidate ranking.

## 📁 Project Structure

```text
FindIt/
├── main.py              # Application entry point
├── gui.py               # Tkinter desktop interface
├── database.py          # SQLite database operations
├── matcher.py           # Matching and scoring algorithm
├── sample_data.py       # Fictional demonstration data
├── README.md            # Project documentation
├── tests/
│   └── test_matcher.py  # Automated matcher tests
└── findit.db            # Generated local database
```

`findit.db` is created automatically during initialization and may not exist until the application is run.

## 🗄️ Database Design

The application stores reports in an SQLite table named `reports`.

Key fields include:

- `id` — Unique report identifier
- `report_type` — Lost or found
- `item_name` — Name of the item
- `category` — Item category
- `color` — Item color
- `location` — Lost or found location
- `report_date` — Relevant report date
- `description` — Additional identifying details
- `reporter_name` — Name of the reporter
- `contact_type` and `contact_info` — Contact details
- `status` — Active, Reunited, or Closed
- `created_at` — Record creation timestamp

The database is intended for local, single-computer use.

## 🔒 Privacy and Limitations

- Contact details are displayed through the application's dedicated contact-viewing action rather than normal report tables.
- Data is stored locally and is not synchronized across computers.
- The application does not provide authentication or strong database access controls.
- Email, SMS, WhatsApp, and push notifications are not implemented.
- Matching is based on manually defined weights and text similarity; it does not use machine learning.
- A high score does not establish ownership. Verify identifying details before returning an item.

Avoid committing a database containing real names, phone numbers, or other personal information to a public repository.

## 🔮 Future Enhancements

Potential improvements include:

- User authentication and role-based access
- Campus-wide deployment with a shared database
- Email notifications for potential matches
- Improved fuzzy matching and date-based scoring
- Image-based item comparison
- Administrative dashboard
- CSV and PDF report export
- Audit logs and stronger privacy controls

## 🎯 Learning Outcomes

This project demonstrates practical applications of:

- Python programming and modular design
- GUI development using Tkinter
- Relational database operations using SQLite
- Data structures such as dictionaries and sets
- String processing and similarity comparison
- Weighted scoring and sorting algorithms
- Unit testing and software validation

## 🏁 Conclusion

FindIt demonstrates how Python, database management, and fundamental data structures and algorithms can be combined to solve a practical campus problem. Its matching engine helps users identify promising lost-and-found candidates while keeping the final ownership decision with the user.

---

**Developed as a college project using Python, Tkinter, SQLite, and fundamental DSA concepts.**
