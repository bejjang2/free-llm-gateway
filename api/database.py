import sqlite3; from pathlib import Path; from loguru import logger

_db_path = None

def init_database(db_path):
    global _db_path
    _db_path = Path(db_path)
    _db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.commit()
    logger.info("DB initialized: {}", _db_path)
    return conn

def get_connection():
    if _db_path is None:
        raise RuntimeError("DB not initialized")
    conn = sqlite3.connect(str(_db_path))
    conn.row_factory = sqlite3.Row
    return conn
