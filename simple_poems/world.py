# WARNING: Python code ahead

from .database import Database
from .schemas import Poem

database = Database()

async def listPoems() -> list[Poem]:
    lists = []

    async with database.inner.execute("SELECT * FROM poems") as cursor:
        async for row in cursor:
            lists.append(Poem(**row))
            
    return lists

async def insertPoem(poem: Poem):
    await database.inner.execute(f"INSERT INTO poems (title, content, author) values (?, ?, ?)", (poem.title, poem.content, poem.author))
    await database.inner.commit()