# Telegram Simple Betting Bot

A Telegram bot that lets users in a **group chat** gamble virtual "units" for fun—place bets, check balances, and roll for free units. Built with **python-telegram-bot v21**, **SQLAlchemy**, **PostgreSQL**, and **AsyncIO**.

> **Status:** Proof-of-concept / hobby project. Works, but not hardened for production.

***To test it locally remember to change .env variables and install PostgreSQL !***

---

## Features

| Command / Action | Description |
| ---------------- | ----------- |
| `/start` | DM or group: introduction message |
| `/roll` | Receive a random number of units *(cool-down currently 5 s)* |
| `/bet <amount>` | Deduct `<amount>` from your balance and publish an **Join Bet** inline button |
| `/balance` | Show your current balance |
| Inline query (`@<BOT_TAG>`) | Shows the above commands in inline form: **Bet 5**, **Balance**, **Roll**. Writing a number changes the bet amount. |


---

## Tech Stack

- Python 3.11+
- python-telegram-bot v21 (async API)
- PostgreSQL (tested with 15)
  - SQLAlchemy 2
  - psycopg2-binary
- python-dotenv
- AsyncIO

---

## Project Layout

```text
telegram-simple-betting-bot/
├── .env.placeholder
├── main.py
├── create_db.py
├── delete_db.py
├── database.py
├── models.py
└── utils/
    ├── command_handlers.py
    ├── callback_handlers.py
    ├── generic_handlers.py
    ├── inline_result_handlers.py
    ├── db_utils.py
    └── generic.py
