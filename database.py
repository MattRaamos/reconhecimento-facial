import sqlite3

conn = sqlite3.connect('pessoas.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS pessoas
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                profissao TEXT NOT NULL,
                endereco TEXT NOT NULL)''')

conn.commit()
conn.close()

