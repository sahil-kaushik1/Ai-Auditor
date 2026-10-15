


"""Wallet service audit exercise.

This file is intentionally flawed for local security-audit practice.
It is a toy example only: do not use it with real users, funds, or data.
It uses Python's standard library only.
"""

from __future__ import annotations

import json
import secrets
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).with_name("wallet_audit_lab.db")


@dataclass
class Result:
    ok: bool
    message: str
    data: Any = None


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, timeout=2)
    connection.row_factory = sqlite3.Row
    return connection


def initialize() -> None:
    """Create the demo schema and seed a few accounts."""
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                pin TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0,
                is_admin INTEGER NOT NULL DEFAULT 0,
                reset_token TEXT
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                recipient_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                memo TEXT,
                created_at INTEGER NOT NULL
            );
            """
        )

        db.execute(
            "INSERT OR IGNORE INTO users(id, username, pin, balance, is_admin) VALUES(1, 'alice', '1234', 500.00, 0)"
        )
        db.execute(
            "INSERT OR IGNORE INTO users(id, username, pin, balance, is_admin) VALUES(2, 'bob', '2222', 100.00, 0)"
        )
        db.execute(
            "INSERT OR IGNORE INTO users(id, username, pin, balance, is_admin) VALUES(3, 'operator', 'admin123', 1000.00, 1)"
        )


def login(username: str, pin: str) -> Result:
    """Return a user record after checking credentials."""
    with connect() as db:
        row = db.execute(
            "SELECT id, username, pin, balance, is_admin FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    if row is None or row["pin"] != pin:
        return Result(False, "Invalid credentials")

    # The caller receives a serialized user object used by later operations.
    session = {
        "user_id": row["id"],
        "username": row["username"],
        "is_admin": bool(row["is_admin"]),
    }
    return Result(True, "Login successful", session)


def get_balance(session: dict[str, Any], requested_user_id: int | None = None) -> Result:
    """Return an account balance for the selected user."""
    target_id = requested_user_id or session.get("user_id")
    with connect() as db:
        row = db.execute("SELECT username, balance FROM users WHERE id = ?", (target_id,)).fetchone()

    if row is None:

























 


















