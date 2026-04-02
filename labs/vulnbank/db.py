import hashlib
import os
import sqlite3

import pymysql
from flask import g, has_request_context

BACKUP_EXPORT_PATH = os.environ.get(
    "DATABASE_BACKUP_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "db_backup.sql"),
)

USE_SQLITE = os.environ.get("USE_SQLITE", "0") == "1" or "MYSQL_HOST" not in os.environ


def _mysql_config():
    return {
        "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "vulnbank"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": False,
    }


def _connect_mysql():
    return pymysql.connect(**_mysql_config())


_SQLITE_PATH = os.environ.get(
    "SQLITE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "vulnbank_test.db"),
)


def _connect_sqlite():
    conn = sqlite3.connect(_SQLITE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _connect():
    if USE_SQLITE:
        return _connect_sqlite()
    return _connect_mysql()


class _Conn:
    def __init__(self, raw, is_sqlite=False):
        self._raw = raw
        self._is_sqlite = is_sqlite

    def execute(self, sql, params=None):
        cur = self._raw.cursor()
        if self._is_sqlite:
            sql = _mysql_to_sqlite(sql)
        if params is None:
            cur.execute(sql)
        else:
            if self._is_sqlite:
                params = tuple(params) if not isinstance(params, tuple) else params
                sql = sql.replace("%s", "?")
            cur.execute(sql, params)
        return _CursorWrapper(cur, self._is_sqlite)

    def commit(self):
        self._raw.commit()

    def close(self):
        self._raw.close()


class _CursorWrapper:
    def __init__(self, cur, is_sqlite):
        self._cur = cur
        self._is_sqlite = is_sqlite

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        if self._is_sqlite:
            return dict(row)
        return row

    def fetchall(self):
        rows = self._cur.fetchall()
        if self._is_sqlite:
            return [dict(r) for r in rows]
        return rows

    @property
    def lastrowid(self):
        return self._cur.lastrowid

    @property
    def rowcount(self):
        return self._cur.rowcount

    def close(self):
        self._cur.close()

    def __iter__(self):
        return iter(self.fetchall())


def _mysql_to_sqlite(sql):
    sql = sql.replace("AUTO_INCREMENT", "")
    sql = sql.replace("ENGINE=InnoDB DEFAULT CHARSET=utf8mb4", "")
    sql = sql.replace("INT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sql = sql.replace("VARCHAR(255)", "TEXT")
    sql = sql.replace("VARCHAR(512)", "TEXT")
    sql = sql.replace("VARCHAR(1024)", "TEXT")
    sql = sql.replace("VARCHAR(64)", "TEXT")
    return sql


def get_db_connection():
    if has_request_context():
        if "db" not in g:
            g.db = _Conn(_connect(), is_sqlite=USE_SQLITE)
        return g.db
    return _Conn(_connect(), is_sqlite=USE_SQLITE)


def init_db():
    conn = _connect()
    is_sqlite = USE_SQLITE
    try:
        cur = conn.cursor()
        if is_sqlite:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    email TEXT,
                    secret_note TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    filename TEXT,
                    filepath TEXT
                )
                """
            )
        else:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(64) DEFAULT 'user',
                    email VARCHAR(255),
                    secret_note TEXT
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS posts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    filename VARCHAR(512),
                    filepath VARCHAR(1024)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        conn.commit()
        cur.execute("SELECT COUNT(*) AS c FROM users")
        row = cur.fetchone()
        count = row["c"] if isinstance(row, dict) else row[0]
        if count == 0:
            users = [
                (
                    "admin",
                    hashlib.md5(b"admin123").hexdigest(),
                    "admin",
                    "admin@seclab.local",
                    "FLAG{admin_secret_note_found}",
                ),
                (
                    "user1",
                    hashlib.md5(b"password1").hexdigest(),
                    "user",
                    "user1@seclab.local",
                    "My personal secret",
                ),
                (
                    "user2",
                    hashlib.md5(b"letmein").hexdigest(),
                    "user",
                    "user2@seclab.local",
                    "Card Number: 4111-1111-1111-1111",
                ),
                (
                    "bob",
                    hashlib.md5(b"bob2024").hexdigest(),
                    "user",
                    "bob@seclab.local",
                    "FLAG{idor_user_data_exposed}",
                ),
            ]
            for u in users:
                if is_sqlite:
                    cur.execute(
                        "INSERT INTO users (username, password, role, email, secret_note) VALUES (?,?,?,?,?)",
                        u,
                    )
                else:
                    cur.execute(
                        "INSERT INTO users (username, password, role, email, secret_note) VALUES (%s,%s,%s,%s,%s)",
                        u,
                    )
            posts = [
                (1, "Welcome to SecBank", "We provide the most secure banking experience."),
                (2, "Great service", "I love the new UI!"),
                (1, "Server maintenance", "Scheduled downtime this weekend."),
            ]
            for p in posts:
                if is_sqlite:
                    cur.execute(
                        "INSERT INTO posts (user_id, title, content) VALUES (?,?,?)",
                        p,
                    )
                else:
                    cur.execute(
                        "INSERT INTO posts (user_id, title, content) VALUES (%s,%s,%s)",
                        p,
                    )
            conn.commit()
        if hasattr(cur, "close"):
            cur.close()
        _write_backup_export(conn, is_sqlite)
    finally:
        conn.close()


def _write_backup_export(conn, is_sqlite=False):
    os.makedirs(os.path.dirname(BACKUP_EXPORT_PATH) or ".", exist_ok=True)
    lines = [
        "-- VulnBank lab export (intentionally exposed via /backup)\n",
        "SET NAMES utf8mb4;\n",
    ]
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT username, role, email, secret_note FROM users ORDER BY id"
        )
        for row in cur.fetchall():
            if is_sqlite:
                row = dict(row)
            u = row["username"].replace("'", "''")
            r = row["role"].replace("'", "''")
            e = (row["email"] or "").replace("'", "''")
            s = (row["secret_note"] or "").replace("'", "''")
            lines.append(
                f"INSERT INTO users (username, role, email, secret_note) "
                f"VALUES ('{u}','{r}','{e}','{s}');\n"
            )
    finally:
        if hasattr(cur, "close"):
            cur.close()
    with open(BACKUP_EXPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
