import csv
import os
import sqlite3

path = 'db.sqlite3'
con = sqlite3.connect(path)
cur = con.cursor()
script_dir = os.path.dirname(__file__)
with open(
    os.path.join(script_dir, 'static/data/users.csv'),
    'r',
    encoding='utf-8'
) as fin:
    dr = csv.DictReader(fin)
    to_db = [(
        i['id'],
        i['username'],
        i['email'],
        i['role'],
        i['bio'],
        i['first_name'],
        i['last_name']) for i in dr]
cur.executemany("INSERT INTO reviews_user"
                "(id, username, email, role,"
                "bio, first_name, last_name, is_superuser,"
                "is_staff, is_active, date_joined)"
                "VALUES (?, ?, ?, ?, ?, ?, ?, false,"
                "false, false, false);", to_db)
con.commit()
print("Запись успешно вставлена в таблицу users_userprofile ", cur.rowcount)
con.close()
