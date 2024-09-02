import sqlite3


class Stik():
    def __init__(self):
        self.newstih = None
        self.stih = None


    def get_stih(self, newstih):
        with sqlite3.connect('stik.db') as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS stih (newstih TEXT PRIMARY KEY, stih TEXT)')
            cursor.execute('SELECT stih FROM stih WHERE newstih = ?', (newstih,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    
    def get_newstih(self):
        with sqlite3.connect('stik.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT newstih FROM stih')
            return cursor.fetchall()
    
    def new_stih(self, newstih, stih):
        with sqlite3.connect('stik.db') as db:
            c = db.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS stih (
                    newstih TEXT PRIMARY KEY,
                    stih TEXT
                )
            """)
            c.execute("INSERT OR REPLACE INTO stih VALUES (?, ?)", (newstih, stih))
            db.commit()