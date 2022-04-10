from src import database


class BaseRepository:
    def __init__(self, db: database.Db):
        self.db = db

    async def rollback(self):
        await self.db.rollback()
