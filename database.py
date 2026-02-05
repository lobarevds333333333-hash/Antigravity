import aiosqlite
import asyncio

DB_NAME = 'leads.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER,
                name TEXT,
                phone TEXT,
                time TEXT,
                description TEXT,
                status TEXT DEFAULT 'NEW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                policy_accepted BOOLEAN DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_lead(telegram_id, name, phone, time, description, status='NEW'):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO leads (telegram_id, name, phone, time, description, status) VALUES (?, ?, ?, ?, ?, ?)',
            (telegram_id, name, phone, time, description, status)
        )
        await db.commit()

async def update_lead_status(lead_id, new_status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE leads SET status = ? WHERE id = ?',
            (new_status, lead_id)
        )
        await db.commit()

async def set_user_policy(telegram_id, accepted: bool):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO users (telegram_id, policy_accepted) VALUES (?, ?) ON CONFLICT(telegram_id) DO UPDATE SET policy_accepted = ?',
            (telegram_id, accepted, accepted)
        )
        await db.commit()

async def get_user_policy(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT policy_accepted FROM users WHERE telegram_id = ?', (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return bool(row[0]) if row else False
