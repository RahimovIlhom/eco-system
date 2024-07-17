import aiomysql
from environs import Env

env = Env()
env.read_env()


class Database:

    def __init__(self):
        self.pool = None
        self.connection = None

    async def create(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=env.str('MYSQL_DB_HOST'),
                port=env.int('MYSQL_DB_PORT'),
                user=env.str('MYSQL_DB_USER'),
                password=env.str('MYSQL_DB_PASSWORD'),
                db=env.str('MYSQL_DB_NAME'),
                charset='utf8mb4',
                autocommit=True
            )
        await self.connect()

    async def connect(self):
        self.connection = await self.pool.acquire()

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def execute(self, query: str, args: tuple = (), fetchone: bool = False, fetchall: bool = False):
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, args)
            if fetchone:
                return await cursor.fetchone()
            if fetchall:
                return await cursor.fetchall()

    async def get_employees(self):
        sql = "SELECT tg_id, language, employee, eco_branch, fullname, phone, inn, created_at FROM eco_branch_employees"
        return await self.execute(sql, fetchall=True)






























