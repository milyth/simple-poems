from aiosqlite import Connection, connect, Row
from pathlib import Path

# Just a wrapper, why should I care?

class Database:
    def __init__(self) -> None:
        self.inner: Connection
    
    async def connect(self, path: Path | str):
        self.inner = await connect(path)
        


    async def setup(self):
        self.inner.row_factory = Row
        await self.inner.execute(f"""
        CREATE TABLE IF NOT EXISTS poems 
         (
            title   text primary key,
            content text not null,
            author  text
         );
        """)

    async def close(self):
        await self.inner.close()

    