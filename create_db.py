import sqlite3

# создаем файл бд и подключаемся:
con = sqlite3.connect('patterns.sqlite')
cur = con.cursor()
# добавляем в бд записи о создании таблиц:
with open('create_tables_script.sql') as f:
    script = f.read()
cur.executescript(script)
cur.close()
con.close()

