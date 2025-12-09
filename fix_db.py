import asyncio
from sqlalchemy import text
from app.db.session import engine

async def fix_doctors_table():
    print("Connecting to database...")
    async with engine.begin() as conn:
        print("Adding missing columns to 'doctors' table...")
        
        # 1. Add email column
        await conn.execute(text("ALTER TABLE doctors ADD COLUMN IF NOT EXISTS email VARCHAR"))
        
        # 2. Add contact_number column
        await conn.execute(text("ALTER TABLE doctors ADD COLUMN IF NOT EXISTS contact_number VARCHAR"))
        
    print("SUCCESS: Columns added! You can now hire doctors.")

if __name__ == "__main__":
    asyncio.run(fix_doctors_table())