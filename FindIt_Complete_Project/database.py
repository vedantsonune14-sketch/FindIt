import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "findit.db"

VALID_TYPES = ("lost", "found")
VALID_STATUSES = ("Active", "Reunited", "Closed")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT NOT NULL CHECK(report_type IN ('lost', 'found')),
                item_name TEXT NOT NULL,
                category TEXT NOT NULL,
                color TEXT,
                location TEXT NOT NULL,
                report_date TEXT NOT NULL,
                description TEXT,
                reporter_name TEXT NOT NULL,
                contact_type TEXT,
                contact_info TEXT,
                status TEXT NOT NULL DEFAULT 'Active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def add_report(data: Dict[str, Any]) -> int:
    if data["report_type"] not in VALID_TYPES:
        raise ValueError("Invalid report type.")

    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO reports (
                report_type, item_name, category, color, location,
                report_date, description, reporter_name,
                contact_type, contact_info, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["report_type"], data["item_name"], data["category"],
            data.get("color", ""), data["location"], data["report_date"],
            data.get("description", ""), data["reporter_name"],
            data.get("contact_type", ""), data.get("contact_info", ""),
            data.get("status", "Active")
        ))
        conn.commit()
        return int(cur.lastrowid)


def get_report(report_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM reports WHERE id = ?", (report_id,)
        ).fetchone()
        return dict(row) if row else None


def get_reports(
    report_type: Optional[str] = None,
    search: str = "",
    category: str = "All",
    status: str = "All",
) -> List[Dict[str, Any]]:
    query = "SELECT * FROM reports WHERE 1=1"
    params = []

    if report_type in VALID_TYPES:
        query += " AND report_type = ?"
        params.append(report_type)

    if search.strip():
        term = f"%{search.strip()}%"
        query += """
            AND (
                item_name LIKE ?
                OR description LIKE ?
                OR location LIKE ?
                OR reporter_name LIKE ?
            )
        """
        params.extend([term, term, term, term])

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if status and status != "All":
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        return [dict(row) for row in conn.execute(query, params).fetchall()]


def get_active_found_reports() -> List[Dict[str, Any]]:
    return get_reports(report_type="found", status="Active")


def update_report(report_id: int, data: Dict[str, Any]) -> bool:
    fields = [
        "item_name", "category", "color", "location", "report_date",
        "description", "reporter_name", "contact_type", "contact_info",
        "status"
    ]
    values = [data.get(field, "") for field in fields]
    values.append(report_id)

    with get_connection() as conn:
        cur = conn.execute(f"""
            UPDATE reports
            SET {", ".join(field + " = ?" for field in fields)}
            WHERE id = ?
        """, values)
        conn.commit()
        return cur.rowcount > 0


def delete_report(report_id: int) -> bool:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
        return cur.rowcount > 0


def set_status(report_id: int, status: str) -> bool:
    if status not in VALID_STATUSES:
        raise ValueError("Invalid status.")
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE reports SET status = ? WHERE id = ?",
            (status, report_id)
        )
        conn.commit()
        return cur.rowcount > 0


def dashboard_stats() -> Dict[str, int]:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT
                SUM(CASE WHEN report_type = 'lost' THEN 1 ELSE 0 END) AS lost_count,
                SUM(CASE WHEN report_type = 'found' THEN 1 ELSE 0 END) AS found_count,
                SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) AS active_count,
                SUM(CASE WHEN status = 'Reunited' THEN 1 ELSE 0 END) AS reunited_count
            FROM reports
        """).fetchone()

    return {
        "lost": row["lost_count"] or 0,
        "found": row["found_count"] or 0,
        "active": row["active_count"] or 0,
        "reunited": row["reunited_count"] or 0,
    }


def clear_all_reports() -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM reports")
        conn.commit()
