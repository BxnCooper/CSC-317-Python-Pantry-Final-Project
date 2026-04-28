import os
import sqlite3
from typing import Dict, List, Any

BASE = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE, "pantry.db")


def _get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    cur = conn.cursor()
    # users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """
    )
    # inventory table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    # donors table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            info TEXT
        )
        """
    )

    # Seed inventory if empty
    cur.execute("SELECT COUNT(1) as c FROM inventory")
    if cur.fetchone()[0] == 0:
        defaults = [
            ("Rice", 50),
            ("Beans", 30),
            ("Canned Corn", 20),
        ]
        cur.executemany("INSERT INTO inventory (name, stock) VALUES (?,?)", defaults)

    conn.commit()
    conn.close()


def read_all() -> Dict[str, Any]:
    """Return a dict with users, inventory, donors similar to previous JSON API."""
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    users = [ {"username": row[0]} for row in cur.fetchall() ]

    cur.execute("SELECT id, name, stock FROM inventory ORDER BY id")
    inventory = [ {"id": row[0], "name": row[1], "stock": row[2]} for row in cur.fetchall() ]

    cur.execute("SELECT id, name, info FROM donors ORDER BY id")
    donors = [ {"id": row[0], "name": row[1], "info": row[2]} for row in cur.fetchall() ]

    conn.close()
    return {"users": users, "inventory": inventory, "donors": donors}


def write_all(data: Dict[str, Any]):
    """Write a full data snapshot back into the DB (overwrites tables).

    This is a convenience function to keep backward compatibility with
    services that expected write_all().
    """
    init_db()
    conn = _get_conn()
    cur = conn.cursor()

    # Replace users
    cur.execute("DELETE FROM users")
    for u in data.get("users", []):
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (u.get("username"), u.get("password", "")))

    # Replace inventory
    cur.execute("DELETE FROM inventory")
    for it in data.get("inventory", []):
        cur.execute("INSERT INTO inventory (id, name, stock) VALUES (?,?,?)", (it.get("id"), it.get("name"), it.get("stock")))

    # Replace donors
    cur.execute("DELETE FROM donors")
    for d in data.get("donors", []):
        cur.execute("INSERT INTO donors (id, name, info) VALUES (?,?,?)", (d.get("id"), d.get("name"), d.get("info")))

    conn.commit()
    conn.close()


def add_user(username: str, password: str) -> bool:
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()


def check_user(username: str, password: str) -> bool:
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return row[0] == password


def list_inventory() -> List[Dict[str, Any]]:
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, stock FROM inventory ORDER BY id")
    res = [ {"id": r[0], "name": r[1], "stock": r[2]} for r in cur.fetchall() ]
    conn.close()
    return res


def change_stock(item_id: int, delta: int):
    init_db()
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT stock FROM inventory WHERE id = ?", (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Item not found"
    new = max(0, row[0] + int(delta))
    cur.execute("UPDATE inventory SET stock = ? WHERE id = ?", (new, item_id))
    conn.commit()
    cur.execute("SELECT id, name, stock FROM inventory WHERE id = ?", (item_id,))
    r = cur.fetchone()
    conn.close()
    return True, {"id": r[0], "name": r[1], "stock": r[2]}

