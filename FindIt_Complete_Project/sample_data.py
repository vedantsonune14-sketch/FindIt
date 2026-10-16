from typing import List, Dict
from database import add_report, get_reports

SAMPLE_REPORTS: List[Dict] = [
    {
        "report_type": "lost", "item_name": "Casio Scientific Calculator",
        "category": "Electronics", "color": "Black", "location": "Computer Laboratory",
        "report_date": "2026-10-10", "description": "Black Casio calculator with a small scratch near the display.",
        "reporter_name": "Aarav Mehta", "contact_type": "email", "contact_info": "aarav.demo@example.com"
    },
    {
        "report_type": "found", "item_name": "Casio Scientific Calculator",
        "category": "Electronics", "color": "Black", "location": "Computer Lab",
        "report_date": "2026-10-11", "description": "Black calculator, small scratch near display, found after lab session.",
        "reporter_name": "Riya Shah", "contact_type": "email", "contact_info": "riya.demo@example.com"
    },
    {
        "report_type": "lost", "item_name": "Blue Water Bottle",
        "category": "Other", "color": "Blue", "location": "Canteen",
        "report_date": "2026-10-09", "description": "Steel blue bottle with a white sticker.",
        "reporter_name": "Kabir Joshi", "contact_type": "phone", "contact_info": "9000000001"
    },
    {
        "report_type": "found", "item_name": "Blue Steel Water Bottle",
        "category": "Other", "color": "Blue", "location": "College Canteen",
        "report_date": "2026-10-09", "description": "Blue steel bottle with a white sticker.",
        "reporter_name": "Neha Patil", "contact_type": "phone", "contact_info": "9000000002"
    },
    {
        "report_type": "lost", "item_name": "Black Laptop Backpack",
        "category": "Bags", "color": "Black", "location": "Library",
        "report_date": "2026-10-08", "description": "Black backpack with laptop sleeve and red keychain.",
        "reporter_name": "Dev Kulkarni", "contact_type": "", "contact_info": ""
    },
    {
        "report_type": "found", "item_name": "Black Backpack",
        "category": "Bags", "color": "Grey", "location": "Library Entrance",
        "report_date": "2026-10-08", "description": "Backpack with laptop sleeve and red keychain.",
        "reporter_name": "Mira Deshmukh", "contact_type": "email", "contact_info": "mira.demo@example.com"
    },
    {
        "report_type": "lost", "item_name": "Wireless Earbuds",
        "category": "Electronics", "color": "White", "location": "Auditorium",
        "report_date": "2026-10-07", "description": "White earbuds in a small charging case.",
        "reporter_name": "Ishaan Verma", "contact_type": "email", "contact_info": "ishaan.demo@example.com"
    },
    {
        "report_type": "found", "item_name": "Earbud Case",
        "category": "Electronics", "color": "Black", "location": "Auditorium",
        "report_date": "2026-10-07", "description": "Small charging case found below a seat.",
        "reporter_name": "Tara Rao", "contact_type": "", "contact_info": ""
    },
    {
        "report_type": "lost", "item_name": "House Keys",
        "category": "Keys", "color": "Silver", "location": "Main Gate",
        "report_date": "2026-10-06", "description": "Three silver keys on a blue key ring.",
        "reporter_name": "Naman Jain", "contact_type": "phone", "contact_info": "9000000003"
    },
    {
        "report_type": "found", "item_name": "Notebook",
        "category": "Stationery", "color": "Green", "location": "Room 204",
        "report_date": "2026-10-05", "description": "Green ruled notebook with mathematics notes.",
        "reporter_name": "Pooja Sen", "contact_type": "email", "contact_info": "pooja.demo@example.com"
    },
    {
        "report_type": "lost", "item_name": "Student ID Card",
        "category": "Documents", "color": "White", "location": "Admin Block",
        "report_date": "2026-10-04", "description": "College identity card in a transparent holder.",
        "reporter_name": "Rohan Das", "contact_type": "email", "contact_info": "rohan.demo@example.com"
    },
    {
        "report_type": "found", "item_name": "Black Umbrella",
        "category": "Other", "color": "Black", "location": "Parking Area",
        "report_date": "2026-10-03", "description": "Foldable black umbrella with curved handle.",
        "reporter_name": "Anika Roy", "contact_type": "phone", "contact_info": "9000000004"
    },
    {
        "report_type": "found", "item_name": "Old Calculator",
        "category": "Electronics", "color": "Black", "location": "Workshop",
        "report_date": "2026-09-30", "description": "Calculator found on a workbench.",
        "reporter_name": "Sameer Khan", "contact_type": "email", "contact_info": "sameer.demo@example.com",
        "status": "Reunited"
    },
]


def load_sample_data() -> int:
    existing = get_reports()
    signatures = {
        (
            r["report_type"], r["item_name"].lower(), r["reporter_name"].lower()
        )
        for r in existing
    }

    inserted = 0
    for report in SAMPLE_REPORTS:
        signature = (
            report["report_type"],
            report["item_name"].lower(),
            report["reporter_name"].lower(),
        )
        if signature not in signatures:
            add_report(report)
            signatures.add(signature)
            inserted += 1
    return inserted
