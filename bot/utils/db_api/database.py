import aiomysql
from environs import Env

env = Env()
env.read_env()


class Database:

    def __init__(self):
        self.pool = None

    async def create(self):
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=env.str('MYSQL_DB_HOST'),
                port=env.int('MYSQL_DB_PORT'),
                user=env.str('MYSQL_DB_USER'),
                password=env.str('MYSQL_DB_PASSWORD'),
                db=env.str('MYSQL_DB_NAME'),
                autocommit=True,
                charset='utf8mb4',
            )

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def execute(self, query: str, args: tuple = (), fetchone: bool = False, fetchall: bool = False):
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, args)
                if fetchone:
                    return await cursor.fetchone()
                if fetchall:
                    return await cursor.fetchall()

    async def get_employees(self):
        sql = "SELECT tg_id, language, employee, eco_branch, fullname, phone, inn, created_at FROM eco_branch_employees"
        return await self.execute(sql, fetchall=True)

    async def admin_get_language(self, tg_id):
        sql = "SELECT language FROM admins WHERE tg_id = %s"
        return await self.execute(sql, (tg_id,), fetchone=True)

    async def admin_set_language(self, tg_id, language: str):
        if not await self.admin_get_language(tg_id):
            sql = "INSERT INTO admins (tg_id, language) VALUES (%s, %s)"
            await self.execute(sql, (tg_id, language))
        else:
            sql = "UPDATE admins SET language = %s WHERE tg_id = %s"
            await self.execute(sql, (language, tg_id))






























