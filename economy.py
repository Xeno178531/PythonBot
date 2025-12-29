import sqlite3 as sq
import os
import config
from discord import app_commands
import time

ecDbFile = os.path.join(config.DATABASE_DIR,'EconomySystem.db')

ec = sq.connect(ecDbFile)
c = ec.cursor()

items = {
    "vip": 1000,
    "miecz": 500,
    "luckybox": 300
}

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)")
c.execute("CREATE TABLE IF NOT EXISTS cooldowns (user_id INTEGER, command TEXT, last_used INTEGER, PRIMARY KEY (user_id, command))")
ec.commit()

def get_item_choices():
    return [
        app_commands.Choice(
            name=f"{name} - {price}💰",
            value=name
        )
        for name, price in items.items()
    ]

def get_or_create_user_ec(user_id: int):
    c.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    ec.commit()

def add_money(user_id: int, amount: int):
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    if result:
        new_balance = result[0] + amount
        c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    else:
        c.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, amount))

    ec.commit()

def remove_money(user_id: int, amount: int):
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    if result:
        new_balance = result[0] - amount
        c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    else:
        c.execute("INSERT INTO users (user_id, balance) VALUES (?, ?)", (user_id, amount))

    ec.commit()

def get_balance(user_id: int):
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    if result:
        return result[0]
    else:
        return 0

def get_leaderboard(limit=10):
    c.execute("SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?", (limit,))
    return c.fetchall()

def return_items():
    return items

def check_cooldown(user_id, command, seconds):
    now = int(time.time())

    c.execute(
        "SELECT last_used FROM cooldowns WHERE user_id=? AND command=?",
        (user_id, command)
    )
    row = c.fetchone()

    if not row:
        return 0  # brak cool downu

    diff = now - row[0]
    if diff < seconds:
        return seconds - diff

    return 0

def set_cooldown(user_id, command):
    now = int(time.time())

    c.execute(
        "REPLACE INTO cooldowns (user_id, command, last_used) VALUES (?, ?, ?)",
        (user_id, command, now)
    )
    ec.commit()


        
