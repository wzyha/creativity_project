import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def execute_query(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def commit_changes(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()