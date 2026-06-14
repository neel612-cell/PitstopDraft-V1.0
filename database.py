import sqlite3
from datetime import datetime

DB_NAME = "pitstop.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token INTEGER UNIQUE,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        dob TEXT NOT NULL,
        join_time TEXT NOT NULL,
        status TEXT DEFAULT 'WAITING'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        queue_paused INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO settings (id, queue_paused)
    VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


def get_next_token():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(token) FROM participants")
    result = cursor.fetchone()[0]

    conn.close()

    if result is None:
        return 1

    return result + 1


def add_participant(name, phone, dob):
    token = get_next_token()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO participants (
        token,
        name,
        phone,
        dob,
        join_time,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        token,
        name,
        phone,
        dob,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "WAITING"
    ))

    conn.commit()
    conn.close()

    return token


def get_all_participants():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM participants
    ORDER BY token ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_waiting_participants():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM participants
    WHERE status='WAITING'
    ORDER BY token ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_current_rider():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM participants
    WHERE status='ON_TRACK'
    LIMIT 1
    """)

    rider = cursor.fetchone()
    conn.close()

    return rider


def set_status(token, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE participants
    SET status=?
    WHERE token=?
    """, (status, token))

    conn.commit()
    conn.close()


def get_participant_by_token(token):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM participants
    WHERE token=?
    """, (token,))

    result = cursor.fetchone()
    conn.close()

    return result


def get_queue_position(token):
    waiting = get_waiting_participants()

    for index, participant in enumerate(waiting, start=1):
        if participant[1] == token:
            return index

    return None


def get_queue_length():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM participants
    WHERE status='WAITING'
    """)

    count = cursor.fetchone()[0]
    conn.close()

    return count


def pause_queue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE settings
    SET queue_paused=1
    WHERE id=1
    """)

    conn.commit()
    conn.close()


def resume_queue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE settings
    SET queue_paused=0
    WHERE id=1
    """)

    conn.commit()
    conn.close()


def is_queue_paused():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT queue_paused
    FROM settings
    WHERE id=1
    """)

    status = cursor.fetchone()[0]
    conn.close()

    return bool(status)