import sqlite3
import datetime

import config


class Admin_sending_messages:
    def __init__(self, user_id):
        self.user_id = user_id
        self.text = None
def first_join(user_id, name):
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    if len(row) == 0:
        cursor.execute(
            f'INSERT INTO users VALUES ("{user_id}", "{name}", "{datetime.datetime.now()}")')
        conn.commit()

    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM messages WHERE bio = "{config.bio}"').fetchall()

    if len(row) == 0:
        cursor.execute(
            f'INSERT INTO messages VALUES ("{config.bio}", "{config.status}")')
        conn.commit()

def admin_info():
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[2][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[2][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = '❕ Информация:\n\n' \
          f'❕ За все время - {amount_user_all}\n' \
          f'❕ За день - {amount_user_day}\n' \
          f'❕ За час - {amount_user_hour}'

    return msg

'''def edit_bio():
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM messages WHERE bio = "{config.bio}"').fetchall()

    if len(row) == 0:
        cursor.execute(
            f'INSERT INTO messages VALUES ("{config.bio}", "{config.status}", "{datetime.datetime.now()}")')
        conn.commit()'''

def get_bio():
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM messages').fetchone()

    result = cursor.fetchone()
    if row:
        return row[0]


def get_status():
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM messages').fetchone()

    result = cursor.fetchone()
    if row:
        return row[1]



