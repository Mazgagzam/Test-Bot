import sqlite3
from prettytable import from_db_cursor

conn = sqlite3.connect("advertising.db")
cur = conn.cursor()


def select(name_table: str, id: int) -> str:
    cur.execute(f"SELECT * FROM {name_table} WHERE id  = {id}")
    return cur.fetchall()[0]

def select_all(name_table: str) -> list:
  cur.execute(f'SELECT * FROM {name_table}')
  return [data[0] for data in cur.fetchall()]


def delete(name_table: str, id: int):
    cur.execute(f"""DELETE from {name_table} where id = {id}""")
    conn.commit()


def count(name_table: str):
    cur.execute(f"SELECT COUNT(*) FROM {name_table}")

    return cur.fetchall()[0][0]


def append(name_table: str, file_id: str, text: str):
    cur.execute(
        f"""INSERT INTO {name_table} VALUES('{count(name_table) + 1}', '{file_id}', '{text}');"""
    )
    conn.commit()


# append('card', 'AgACAgIAAxkBAAIKa2RcqPr8aFTOse0vOCVh9KKfleo0AAJ5xzEbtUHgSqiDdGEiysrjAQADAgADeQADLwQ', 'TEST1')
# append('card', 'AgACAgIAAxkBAAIKa2RcqPr8aFTOse0vOCVh9KKfleo0AAJ5xzEbtUHgSqiDdGEiysrjAQADAgADeQADLwQ', 'TEST2')

cur.execute('SELECT * FROM card')

print(from_db_cursor(cur))

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())
