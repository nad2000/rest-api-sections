import sqlite3

def dict_factory(cursor, row):
    return {col[0]: row[idx] for (idx, col) in enumerate(cursor.description)}


__conn = None

def make_conn():
    global __conn
    def opendb():
        global __conn
        __conn = sqlite3.connect("data.db")
        __conn.row_factory = dict_factory
    if __conn is None:
        opendb()
    else:
        try:
            __conn.total_changes
        except sqlite3.ProgrammingError:
            opendb()
    return __conn


class Item:

    @classmethod
    def find_by_name(cls, name):
        conn = make_conn()
        res = make_conn().execute("SELECT * FROM items WHERE name=? LIMIT 1", (name,))
        row = res.fetchone()
        conn.close()
        return row

    @classmethod
    def upsert(cls, name, price):
        conn = make_conn()
        conn.execute(
                "INSERT OR REPLACE INTO items (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        return cls.find_by_name(name)

    @classmethod
    def delete(self, name):
        conn = make_conn()
        conn.execute("DELETE FROM items WHERE name=?", (name,))
        conn.commit()
        conn.close()

class ItemList:
    @classmethod
    def get_items(self):
        conn = make_conn()
        items = conn.execute("SELECT * FROM items").fetchall()
        conn.close()
        return items

