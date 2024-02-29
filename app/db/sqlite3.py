# db.py

import sqlite3
import numpy as np

class SQLiteHandler:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
    def get_text_and_vector(self, id):
            self.cursor.execute("SELECT text, vector FROM qa_vectors WHERE id=?", (id,))
            result = self.cursor.fetchone()
            if result:
                text, vector_blob = result
                # 将字节转换回numpy数组
                vector = np.frombuffer(vector_blob, dtype=np.float32)
                return text, vector
            else:
                return None, None
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS qa_vectors
                             (id INTEGER PRIMARY KEY, text TEXT, vector BLOB)''')
        self.conn.commit()

    def insert_vector(self, id, text, vector):
        # 替换已存在的记录
        self.cursor.execute("REPLACE INTO qa_vectors (id, text, vector) VALUES (?, ?, ?)", (id, text, vector))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
