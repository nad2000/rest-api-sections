import sqlite3

__conn = None

def make_conn():
    global __conn
    def opendb():
        global __conn
        __conn = sqlite3.connect("data.db")
    if __conn is None:
        opendb()
    else:
        try:
            __conn.total_changes
        except sqlite3.ProgrammingError:
            opendb()
    return __conn


class Item:

    def __init__(self, name, price=None):
        self.name = name
        self.price = price

    def to_dict(self):
        return dict(name=self.name, price=self.price)

    @classmethod
    def find_by_name(cls, name):
        conn = make_conn()
        res = make_conn().execute("SELECT name, price FROM items WHERE name=? LIMIT 1", (name,))
        row = res.fetchone()
        conn.close()
        if row:
            return cls(*row)

    def upsert(self):
        conn = make_conn()
        conn.execute(
                "INSERT OR REPLACE INTO items (name, price) VALUES (?, ?)", (self.name, self.price))
        conn.commit()
        conn.close()

    def delete(self):
        conn = make_conn()
        conn.execute("DELETE FROM items WHERE name=?", (self.name,))
        conn.commit()
        conn.close()

class ItemList:
    @classmethod
    def get_items(self):
        conn = make_conn()
        items = conn.execute("SELECT * FROM items").fetchall()
        conn.close()
        return items

