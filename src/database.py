import sqlite3
from pathlib import Path


DB_PATH = Path("data/support_cases.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            system TEXT NOT NULL,
            category TEXT,
            description TEXT NOT NULL,
            symptoms TEXT,
            attempted_steps TEXT,
            status TEXT NOT NULL DEFAULT 'Abierto',
            cause TEXT,
            resolution TEXT,
            escalation TEXT,
            tags TEXT,
            verified INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def insert_case(case_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cases (
            title,
            system,
            category,
            description,
            symptoms,
            attempted_steps,
            status,
            cause,
            resolution,
            escalation,
            tags,
            verified
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            case_data.get("title"),
            case_data.get("system"),
            case_data.get("category"),
            case_data.get("description"),
            case_data.get("symptoms"),
            case_data.get("attempted_steps"),
            case_data.get("status", "Abierto"),
            case_data.get("cause"),
            case_data.get("resolution"),
            case_data.get("escalation"),
            case_data.get("tags"),
            int(case_data.get("verified", False)),
        ),
    )

    conn.commit()
    case_id = cursor.lastrowid
    conn.close()

    return case_id


def get_all_cases():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM cases
        ORDER BY updated_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_case_by_id(case_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM cases
        WHERE id = ?
        """,
        (case_id,),
    )

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None


def update_case(case_id, case_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE cases
        SET
            title = ?,
            system = ?,
            category = ?,
            description = ?,
            symptoms = ?,
            attempted_steps = ?,
            status = ?,
            cause = ?,
            resolution = ?,
            escalation = ?,
            tags = ?,
            verified = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            case_data.get("title"),
            case_data.get("system"),
            case_data.get("category"),
            case_data.get("description"),
            case_data.get("symptoms"),
            case_data.get("attempted_steps"),
            case_data.get("status"),
            case_data.get("cause"),
            case_data.get("resolution"),
            case_data.get("escalation"),
            case_data.get("tags"),
            int(case_data.get("verified", False)),
            case_id,
        ),
    )

    conn.commit()
    conn.close()


def delete_case(case_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM cases
        WHERE id = ?
        """,
        (case_id,),
    )

    conn.commit()
    conn.close()