import os
import sqlite3
from typing import Dict, List, Any

class Database():
    def __init__(self):
        self.BASE = os.path.dirname(__file__)
        self.DB_FILE = os.path.join(self.BASE, "pantry.db")


    def _get_conn(self):
        conn = sqlite3.connect(self.DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn


    def init_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        # users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT,
                font_size TEXT NOT NULL DEFAULT 'Medium',
                dark INTEGER DEFAULT 0,
                allergen_list TEXT
            )
            """
        )
        # inventory table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                allergens TEXT NOT NULL DEFAULT 'None'
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
        
        # volunteers table: shifts/opportunities
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                info TEXT,
                slots INTEGER DEFAULT 1
            )
            """
        )

        # signups table: which username signed up for which shift
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS signups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                shift_id INTEGER,
                UNIQUE(username, shift_id)
            )
            """
        )

        # Seed inventory if empty
        cur.execute("SELECT COUNT(1) as c FROM inventory")
        if cur.fetchone()[0] == 0:
            defaults = [
                ("Rice", 50, "None"),
                ("Beans", 30, "None"),
                ("Canned Corn", 20, "None"),
            ]
            cur.executemany("INSERT INTO inventory (name, stock, allergens) VALUES (?,?,?)", defaults)
        # Seed volunteers with placeholder schedule dates if empty
        cur.execute("SELECT COUNT(1) as c FROM volunteers")
        if cur.fetchone()[0] == 0:
            # info field includes time and a placeholder date
            v_defaults = [
                ("Morning Shift - Mon", "8am-11am | 2026-05-04", 3),
                ("Afternoon Shift - Wed", "1pm-4pm | 2026-05-06", 2),
                ("Evening Shift - Fri", "5pm-8pm | 2026-05-08", 2),
            ]
            cur.executemany("INSERT INTO volunteers (name, info, slots) VALUES (?,?,?)", v_defaults)
        conn.commit()
        conn.close()


    def read_all(self) -> Dict[str, Any]:
        """Return a dict with users, inventory, donors similar to previous JSON API."""
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users")
        users = [ {"username": row[0]} for row in cur.fetchall() ]

        cur.execute("SELECT id, name, stock FROM inventory ORDER BY id")
        inventory = [ {"id": row[0], "name": row[1], "stock": row[2], "allergens": row[3]} for row in cur.fetchall() ]

        cur.execute("SELECT id, name, info FROM donors ORDER BY id")
        donors = [ {"id": row[0], "name": row[1], "info": row[2]} for row in cur.fetchall() ]

        cur.execute("SELECT id, name, info, slots FROM volunteers ORDER BY id")
        volunteers = [ {"id": row[0], "name": row[1], "info": row[2], "slots": row[3]} for row in cur.fetchall() ]


        conn.close()
        return {"users": users, "inventory": inventory, "donors": donors, "volunteers": volunteers}


    def write_all(self, data: Dict[str, Any]):
        """Write a full data snapshot back into the DB (overwrites tables).

        This is a convenience function to keep backward compatibility with
        services that expected write_all().
        """
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()

        # Replace users
        cur.execute("DELETE FROM users")
        for u in data.get("users", []):
            cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (u.get("username"), u.get("password", "")))

        # Replace inventory
        cur.execute("DELETE FROM inventory")
        for it in data.get("inventory", []):
            cur.execute("INSERT INTO inventory (id, name, stock, allergens) VALUES (?,?,?,?)", (it.get("id"), it.get("name"), it.get("stock"), it.get("allergens")))

        # Replace donors
        cur.execute("DELETE FROM donors")
        for d in data.get("donors", []):
            cur.execute("INSERT INTO donors (id, name, info) VALUES (?,?,?)", (d.get("id"), d.get("name"), d.get("info")))

        conn.commit()
        conn.close()


    def add_user(self, username: str, password: str) -> bool:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()


    def check_user(self, username: str, password: str) -> bool:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return False
        return row[0] == password


    def list_volunteers(self) -> List[Dict[str, Any]]:
        """Return all volunteer shifts/opportunities."""
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, info, slots FROM volunteers ORDER BY id")
        res = [ {"id": r[0], "name": r[1], "info": r[2], "slots": r[3]} for r in cur.fetchall() ]
        conn.close()
        return res

    def add_volunteer(self, name: str, info: str, slots: int = 1):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO volunteers (name, info, slots) VALUES (?,?,?)", (name, info, int(slots)))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(str(e))
            return False

    def list_shift_signups(self, shift_id: int) -> List[str]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT username FROM signups WHERE shift_id = ?", (shift_id,))
        res = [ r[0] for r in cur.fetchall() ]
        conn.close()
        return res

    def list_user_signups(self, username: str) -> List[int]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT shift_id FROM signups WHERE username = ?", (username,))
        res = [ r[0] for r in cur.fetchall() ]
        conn.close()
        return res

    def sign_up(self, username: str, shift_id: int):
        """Attempt to sign a user up for a shift. Returns (True, '') on success or (False, reason)."""
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            # check shift exists and slot availability
            cur.execute("SELECT slots FROM volunteers WHERE id = ?", (shift_id,))
            row = cur.fetchone()
            if not row:
                conn.close()
                return False, "Shift not found"
            slots = row[0]
            cur.execute("SELECT COUNT(1) FROM signups WHERE shift_id = ?", (shift_id,))
            used = cur.fetchone()[0]
            if used >= slots:
                conn.close()
                return False, "No slots available"
            # try insert
            cur.execute("INSERT OR IGNORE INTO signups (username, shift_id) VALUES (?,?)", (username, shift_id))
            conn.commit()
            # verify inserted
            cur.execute("SELECT COUNT(1) FROM signups WHERE username = ? AND shift_id = ?", (username, shift_id))
            ok = cur.fetchone()[0] > 0
            conn.close()
            if ok:
                return True, ""
            return False, "Already signed up"
        except Exception as e:
            conn.close()
            return False, str(e)

    def cancel_signup(self, username: str, shift_id: int):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM signups WHERE username = ? AND shift_id = ?", (username, shift_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(str(e))
            return False


    def list_inventory(self) -> List[Dict[str, Any]]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory ORDER BY id")
        res = [ {"id": r[0], "name": r[1], "stock": r[2],  "allergens": r[3]} for r in cur.fetchall() ]
        conn.close()
        return res

    def list_inventory_name(self) -> List[Dict[str, Any]]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory ORDER BY name")
        res = [ {"id": r[0], "name": r[1], "stock": r[2], "allergens": r[3]} for r in cur.fetchall() ]
        conn.close()
        return res

    def list_inventory_stock(self) -> List[Dict[str, Any]]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory ORDER BY stock")
        res = [ {"id": r[0], "name": r[1], "stock": r[2], "allergens": r[3]} for r in cur.fetchall() ]
        conn.close()
        return res

    def list_inventory_allergen(self) -> List[Dict[str, Any]]:
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM inventory ORDER BY stock")
        res = [ {"id": r[0], "name": r[1], "stock": r[2], "allergens": r[3]} for r in cur.fetchall() ]
        conn.close()
        return res

    def change_stock(self, item_id: int, delta: int):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute("SELECT stock FROM inventory WHERE id = ?", (item_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False, "Item not found"
        new = max(0, row[0] + int(delta))
        cur.execute("UPDATE inventory SET stock = ? WHERE id = ?", (new, item_id))
        conn.commit()
        cur.execute("SELECT * FROM inventory WHERE id = ?", (item_id,))
        r = cur.fetchone()
        conn.close()
        return True, {"id": r[0], "name": r[1], "stock": r[2], "allergens": r[3]}


    def get_item(self, name: str):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT id FROM inventory WHERE name = ?", (name,))
            id = cur.fetchone()[0]
            return id
        
        except Exception as e:
            return str(e)


    def add_item(self, name: str, stock: int, allergens: str):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        
        try:
            new_item = (name, stock, allergens)
            cur.execute("INSERT INTO inventory (name, stock, allergens) VALUES (?,?,?)", new_item)
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(str(e))
            return False
        
        
    def remove_item(self, id: int):
        self.init_db()
        conn = self._get_conn()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT * FROM inventory WHERE id = ?", (id,))
            row = cur.fetchone()
            
            if not row:
                conn.close()
                return "Item with that ID does not exist."
            
            else:
                cur.execute("DELETE FROM inventory WHERE id = ?", (id,))
                conn.commit()
                conn.close()
                return True
            
        except Exception as e:
            print(str(e))
            return False