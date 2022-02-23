import aiosqlite

async def get_db_object():
    db = await aiosqlite.connect("rasa_sqlite")
    return db