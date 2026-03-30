import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import DB_PATH


def _get_db_path():
    """Resolve DB path relative to backend directory if relative."""
    p = Path(DB_PATH)
    if not p.is_absolute():
        backend_dir = Path(__file__).resolve().parent
        p = backend_dir / p
    return str(p)


@contextmanager
def get_connection():
    conn = sqlite3.connect(_get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Create conversations and messages tables if they do not exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        """)
        conn.commit()


def save_message(conversation_id: str, role: str, content: str) -> int:
    """Insert a message and return its id. Creates conversation if needed."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO conversations (id, created_at) VALUES (?, datetime('now'))",
            (conversation_id,),
        )
        cur = conn.execute(
            "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
            (conversation_id, role, content),
        )
        return cur.lastrowid


def get_history(conversation_id: str, limit: int = 50):
    """Return recent messages for a conversation, oldest first."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, conversation_id, role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (conversation_id, limit),
        ).fetchall()
    return [dict(row) for row in rows]
